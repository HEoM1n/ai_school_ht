from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import os
import uuid
import shutil
import httpx  # 🔥 추가
from pathlib import Path
from typing import Optional
from datetime import datetime

# 로컬 import
from database import get_db, engine, Base
from models import PhoneReport

app = FastAPI(title="Voice Phishing Detection Server")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드 디렉토리 생성
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 🔥 클라우드 설정 추가
CLOUD_UPLOAD_URL = "http://223.130.128.36:8080/upload"
CLOUD_ANALYZE_URL = "http://223.130.128.36:8080/analyze"

# 🔥 모델 추가
class AnalysisRequest(BaseModel):
    file_path: str

# 응답 모델 
class UploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    content_type: str
    message: str

class AnalysisResponse(BaseModel):
    file_path: str
    cloud_path: str
    analysis_result: dict

class PhoneCheckRequest(BaseModel):
    phone_number: str

class PhoneCheckResponse(BaseModel):
    phone_number: str
    is_phishing: bool
    confidence: float
    message: str
    details: Optional[dict] = None

# 🔥 헬퍼 함수 추가
def extract_keywords(reason_text: str) -> list:
    keywords = []
    risk_words = ["긴급", "계좌이체", "확인", "카드", "은행"]
    for word in risk_words:
        if word in reason_text:
            keywords.append(word)
    return keywords

def calculate_sentiment(risk_score: int) -> float:
    return -1.0 + (2.0 * (100 - risk_score) / 100)

def determine_urgency(risk_score: int) -> str:
    if risk_score >= 70:
        return "high"
    elif risk_score >= 40:
        return "medium"
    else:
        return "low"

# 전화번호 검색 엔드포인트
@app.post("/check-phone", response_model=PhoneCheckResponse)
async def check_phone_number(request: PhoneCheckRequest, db: Session = Depends(get_db)):
    """전화번호 보이스피싱 DB 검색"""
    
    phone_number = request.phone_number.strip()
    clean_number = phone_number.replace("-", "").replace(" ", "")
    
    phishing_record = db.query(PhoneReport).filter(
        PhoneReport.phone_number == clean_number
    ).first()
    
    if phishing_record:
        return PhoneCheckResponse(
            phone_number=phone_number,
            is_phishing=int(phishing_record.is_phishing),
            confidence=0.95,
            message="⚠️ 이 번호는 보이스피싱 의심 번호로 신고된 이력이 있습니다!",
            details={
                "spam_type": phishing_record.spam_type,
                "description": phishing_record.description,
                "report_count": phishing_record.report_count
            }
        )
    else:
        return PhoneCheckResponse(
            phone_number=phone_number,
            is_phishing=0,
            confidence=0.8,
            message="✅ 이 번호는 보이스피싱 DB에서 발견되지 않았습니다.",
            details=None
        )

# 보이스피싱 번호 신고 엔드포인트
@app.post("/report-phone")
async def report_phone_number(
    phone_number: str,
    reporter_name: str = "익명",
    description: str = "",
    db: Session = Depends(get_db)
):
    """보이스피싱 번호 신고"""
    
    clean_number = phone_number.replace("-", "").replace(" ", "")
    
    # 이미 존재하는지 확인
    existing = db.query(PhoneReport).filter(  # 🔥 수정
        PhoneReport.phone_number == clean_number
    ).first()
    
    if existing:
        return {"message": "이미 신고된 번호입니다.", "status": "exists"}
    
    # 새로운 신고 추가
    new_report = PhoneReport(  # 🔥 수정
        phone_number=clean_number,
        reporter_name=reporter_name,
        description=description,
        is_confirmed=False  # 관리자 확인 필요
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return {"message": "신고가 접수되었습니다.", "status": "success", "id": new_report.id}

# 기존 파일 업로드 엔드포인트
@app.post("/upload", response_model=UploadResponse)
async def upload_audio_file(file: UploadFile = File(...)):
    """음성 파일 업로드 및 로컬 저장"""
    
    # 파일 타입 검증
    allowed_types = ["audio/wav", "audio/mpeg", "audio/mp3", "audio/ogg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"지원하지 않는 파일 형식입니다. 지원 형식: {allowed_types}"
        )
    
    # 파일명 중복 방지를 위한 UUID 생성
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 파일 크기 계산
        file_size = os.path.getsize(file_path)
        
        return UploadResponse(
            filename=unique_filename,
            file_path=str(file_path),
            file_size=file_size,
            content_type=file.content_type,
            message="파일이 성공적으로 업로드되었습니다."
        )
    
    except Exception as e:
        # 업로드 실패 시 파일 삭제
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")

# 🔥 분석 요청 엔드포인트 수정 (클라우드 업로드 + 경로 전달)
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_audio(request: AnalysisRequest):
    """파일을 클라우드에 업로드하고 분석 요청"""
    
    file_path = request.file_path
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    try:
        async with httpx.AsyncClient() as client:
            
            # 🔥 1단계: 클라우드에 파일 업로드
            with open(file_path, 'rb') as audio_file:
                files = {
                    "audio": (
                        os.path.basename(file_path),
                        audio_file,
                        "audio/wav"
                    )
                }
                
                upload_response = await client.post(
                    CLOUD_UPLOAD_URL,
                    files=files,
                    timeout=60
                )
                
            if upload_response.status_code != 200:
                raise HTTPException(500, f"클라우드 업로드 실패: {upload_response.status_code}")
            
            upload_result = upload_response.json()
            cloud_file_path = upload_result.get("file_path")
            
            # 🔥 2단계: 클라우드 경로로 분석 요청
            analyze_response = await client.post(
                CLOUD_ANALYZE_URL,
                json={
                    "file_path": cloud_file_path,
                    "analysis_type": "voice_phishing"
                },
                timeout=120
            )
            
            if analyze_response.status_code == 200:
                ai_result = analyze_response.json()
                
                # 프론트엔드 형식으로 변환
                analysis_result = {
                    "is_phishing": ai_result.get("decision") == "보이스피싱",
                    "confidence": ai_result.get("risk_score", 0) / 100.0,
                    "deepfake_probability": 0.0,
                    "content_analysis": {
                        "risk_keywords": extract_keywords(ai_result.get("reason", "")),
                        "sentiment_score": calculate_sentiment(ai_result.get("risk_score", 50)),
                        "urgency_level": determine_urgency(ai_result.get("risk_score", 50))
                    },
                    "audio_features": {
                        "transcribed_text": ai_result.get("transcribed_text", ""),
                        "duration": ai_result.get("duration", 0),
                        "sample_rate": 16000,
                        "channels": 1,
                        "processing_time": ai_result.get("processing_time", 0)
                    },
                    "model_details": {
                        "decision": ai_result.get("decision", "알 수 없음"),
                        "risk_score": ai_result.get("risk_score", 0),
                        "reason": ai_result.get("reason", ""),
                        "type": ai_result.get("type", "unknown")
                    }
                }
                
                return AnalysisResponse(
                    file_path=file_path,
                    cloud_path=cloud_file_path,
                    analysis_result=analysis_result
                )
            else:
                raise HTTPException(500, f"AI 분석 실패: {analyze_response.status_code}")
                
    except Exception as e:
        raise HTTPException(500, f"분석 실패: {str(e)}")

# 기존 엔드포인트들
@app.get("/files")
async def list_uploaded_files():
    """업로드된 파일 목록 반환"""
    files = []
    for file_path in UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            files.append({
                "filename": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "created": file_path.stat().st_mtime
            })
    return {"files": files}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "upload_dir": str(UPLOAD_DIR),
        "upload_dir_exists": UPLOAD_DIR.exists()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)