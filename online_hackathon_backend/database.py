from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cx_Oracle
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# Oracle DB 연결 설정
ORACLE_USER = os.getenv("ORACLE_USER", "system")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "password")
ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
ORACLE_SERVICE = os.getenv("ORACLE_SERVICE", "xe")

# Oracle Instant Client 경로 설정 (필요한 경우)
ORACLE_CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH", "")
if ORACLE_CLIENT_PATH:
    cx_Oracle.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)

# SQLAlchemy 연결 문자열
DATABASE_URL = f"oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
