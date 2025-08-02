from fastapi import FastAPI
from sqlalchemy import text
from database import engine
from models import Base  # ✅ User 모델 만들었으면 이걸 가져와야 해

app = FastAPI()

@app.on_event("startup")
async def startup():
    # ✅ DB 연결 테스트
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ DB 연결 성공:", result.scalar())
    except Exception as e:
        print("❌ DB 연결 실패:", e)

    # ✅ 테이블 생성
    try:
        Base.metadata.create_all(bind=engine)
        print("📦 테이블 생성 완료 또는 이미 존재함")
    except Exception as e:
        print("❌ 테이블 생성 실패:", e)
