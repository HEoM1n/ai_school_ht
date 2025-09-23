from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

# 로컬 import
# from database import get_db, engine, Base
# from models import PhoneReport

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
# Base.metadata.create_all(bind=engine)

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

# 전화번호 검색 엔드포인트 (가짜 데이터 사용)
@app.post("/check-phone", response_model=PhoneCheckResponse)
async def check_phone_number(request: PhoneCheckRequest):
    """전화번호 보이스피싱 DB 검색 (가짜 데이터)"""
    
    phone_number = request.phone_number.strip()
    
    # 특정 번호("1234" 포함)에 대해 '피싱'으로 응답하는 가짜 로직
    if "1234" in phone_number:
        return PhoneCheckResponse(
            phone_number=phone_number,
            is_phishing=True,
            confidence=0.95,
            message="⚠️ [가짜 데이터] 이 번호는 보이스피싱 의심 번호로 신고된 이력이 있습니다!",
            details={
                "spam_type": "User Reported",
                "description": "가짜 데이터: 고액 알바를 빙자한 금융 사기 시도",
                "report_count": 3,
                "reported_date": "2024-05-15",
                "reporter_name": "김*민"
            }
        )
    else:
        return PhoneCheckResponse(
            phone_number=phone_number,
            is_phishing=False,
            confidence=0.99,
            message="✅ [가짜 데이터] 이 번호는 보이스피싱 DB에서 발견되지 않았습니다.",
            details=None
        )

# # 보이스피싱 번호 신고 엔드포인트
# @app.post("/report-phone")
# async def report_phone_number(
#     phone_number: str,
#     reporter_name: str = "익명",
#     description: str = "",
#     db: Session = Depends(get_db)
# ):
#     """보이스피싱 번호 신고"""
    
#     clean_number = phone_number.replace("-", "").replace(" ", "")
    
#     # 이미 존재하는지 확인
#     existing = db.query(PhoneReport).filter(
#         PhoneReport.phone_number == clean_number
#     ).first()
    
#     if existing:
#         # 이미 존재하면 report_count를 1 증가
#         existing.report_count += 1
#         db.commit()
#         db.refresh(existing)
#         return {"message": "신고 횟수가 1 증가했습니다.", "status": "updated", "id": existing.id}
    
#     # 새로운 신고 추가
#     new_report = PhoneReport(
#         phone_number=clean_number,
#         is_phishing=True,  # 신고된 것은 피싱으로 간주
#         spam_type="User Reported", # 신고 유형
#         description=description,
#         report_count=1
#     )
    
#     db.add(new_report)
#     db.commit()
#     db.refresh(new_report)
    
#     return {"message": "신고가 접수되었습니다.", "status": "success", "id": new_report.id}

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

class AnalyzeRequest(BaseModel):
    file_path: str

# 분석 요청 엔드포인트
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_audio(request: AnalyzeRequest):
    """파일 경로를 받아 분석 요청"""
    
    # 파일 존재 여부 확인
    if not os.path.exists(request.file_path):
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다.")
    
    # 클라우드 경로 모킹
    cloud_path = f"gs://voice-analysis-bucket/{os.path.basename(request.file_path)}"
    
    # 분석 결과 모킹 (실제로는 AI 모델 분석 결과)
    mock_analysis_result = {
        "is_phishing": True,
        "confidence": 0.87,
        "content_analysis": {
            "risk_keywords": ["긴급", "계좌이체", "확인"],
            "sentiment_score": -0.65,
            "urgency_level": "high"
        },
        "audio_features": {
            "duration": 45.2,
            "sample_rate": 16000,
            "channels": 1
        },
        "processing_time": 2.3
    }
    
    return AnalysisResponse(
        file_path=request.file_path,
        cloud_path=cloud_path,
        analysis_result=mock_analysis_result
    )

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
