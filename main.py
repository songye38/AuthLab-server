from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI()

@app.on_event("startup")
async def test_db_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ DB 연결 성공:", result.scalar())
    except Exception as e:
        print("❌ DB 연결 실패:", e)
