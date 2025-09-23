from database import engine, Base
from models import PhoneReport

def init_database():
    print("데이터베이스 테이블을 초기화합니다...")
    try:
        # 기존 테이블을 먼저 삭제합니다 (오류가 나도 무시).
        print("기존 테이블을 삭제합니다...")
        Base.metadata.drop_all(bind=engine)
        
        # 새로운 테이블을 생성합니다.
        print("새로운 테이블을 생성합니다...")
        Base.metadata.create_all(bind=engine)
        
        print("테이블 초기화가 성공적으로 완료되었습니다.")
    except Exception as e:
        print(f"테이블 초기화 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    init_database()