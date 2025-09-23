# 🛡️ 보이스 피싱 탐지 시스템 - Docker 버전

AI 기반 보이스 피싱 탐지 시스템을 Docker로 실행하는 방법입니다.

## 🚀 빠른 시작

### 1. 사전 요구사항
- Docker Desktop 설치
- Oracle Database 실행 중 (로컬 또는 원격)

### 2. 실행 방법

```bash
# 1. 프로젝트 디렉토리로 이동
cd hackerthon/ai_school_ht

# 2. Docker 컨테이너 빌드 및 실행
docker-compose up --build

# 또는 백그라운드 실행
docker-compose up -d --build
```

### 3. 접속 주소
- **프론트엔드 (Streamlit)**: http://localhost:8501
- **백엔드 API (FastAPI)**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 🔧 환경 설정

### Oracle Database 연결 설정
`docker-compose.yml` 파일에서 Oracle DB 연결 정보를 수정하세요:

```yaml
environment:
  - ORACLE_USER=your_username
  - ORACLE_PASSWORD=your_password  
  - ORACLE_HOST=host.docker.internal  # Windows/Mac Docker Desktop
  - ORACLE_PORT=1521
  - ORACLE_SERVICE=xe
```

### Linux에서 실행하는 경우
`docker-compose.yml`에서 `ORACLE_HOST`를 다음과 같이 변경:
```yaml
- ORACLE_HOST=172.17.0.1  # Linux Docker 기본 게이트웨이
```

## 📋 주요 기능

1. **📞 전화번호 검색**: 보이스피싱 신고 DB에서 즉시 검색
2. **🎙️ 통화 분석**: AI가 녹음 파일을 분석하여 보이스피싱 여부 판단
3. **📊 실시간 결과**: 분석 결과를 시각적으로 표시

## 🛠️ 개발 모드

### 로그 확인
```bash
docker-compose logs -f
```

### 특정 서비스 로그만 확인
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 컨테이너 중지
```bash
docker-compose down
```

### 컨테이너 및 볼륨 완전 삭제
```bash
docker-compose down -v --rmi all
```

## 🔍 트러블슈팅

### Oracle 연결 오류
1. Oracle Database가 실행 중인지 확인
2. 방화벽에서 1521 포트 허용 확인
3. Oracle 사용자 권한 확인

### 포트 충돌
다른 애플리케이션이 8000 또는 8501 포트를 사용 중인 경우:
```yaml
ports:
  - "8080:8000"  # 백엔드 포트 변경
  - "8502:8501"  # 프론트엔드 포트 변경
```

### 파일 업로드 문제
uploads 디렉토리 권한 확인:
```bash
chmod 755 online_hackathon_backend/uploads
```

## 📁 프로젝트 구조

```
ai_school_ht/
├── docker-compose.yml
├── online_hackathon_backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   └── uploads/
└── online_hackathon_frontend/
    ├── Dockerfile
    ├── app.py
    ├── requirements.txt
    └── pages/
        ├── home.py
        ├── phone_page.py
        ├── analysis_page.py
        └── result_page.py
```

## 🔒 보안 주의사항

- 프로덕션 환경에서는 `.env` 파일로 민감한 정보 관리
- Oracle 패스워드를 기본값에서 변경
- CORS 설정을 프로덕션에 맞게 제한