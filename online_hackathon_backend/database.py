from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import cx_Oracle
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# Oracle DB 연결 설정
ORACLE_USER = os.getenv("ORACLE_USER", "SCOTT")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "TIGER")
ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
ORACLE_SID = os.getenv("ORACLE_SID", "xepdb1")

# # Oracle Instant Client 경로 설정 (필요한 경우)
# ORACLE_CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH", "")
# if ORACLE_CLIENT_PATH:
#     cx_Oracle.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)

# SQLAlchemy 연결 문자열
# DSN (Data Source Name)을 직접 만들어 가장 안정적인 방법으로 연결합니다.
dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={ORACLE_HOST})(PORT={ORACLE_PORT}))(CONNECT_DATA=(SERVICE_NAME={ORACLE_SID})))"
DATABASE_URL = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{dsn}"
# -----------------------------------------------------------

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
