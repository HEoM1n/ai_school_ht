from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 로컬 SQLite 데이터베이스 설정
DATABASE_URL = "sqlite:///./hackathon.db"

# SQLAlchemy 엔진 생성
# connect_args는 SQLite에서만 필요합니다 (thread-safe 설정)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()