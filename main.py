
# 제일 첫번째 진입점에서 FastAPI 앱을 설정하고 라우팅을 정의합니다.
# 이 파일은 서버를 실행할 때 가장 먼저 실행되는 파일입니다.


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.db.models import Base
from app.db.schemas import UserCreate, UserOut
from app.db.crud import create_user
import app.db.models as models
from app.auth.dependencies import verify_token  # 이 경로는 실제 구조에 맞게 조정

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일이에요.")
    new_user = create_user(db, email=user.email, password=user.password)
    return new_user


@app.get("/protected")
async def protected_route(user_id: str = Depends(verify_token)):
    return {"message": f"안녕하세요, {user_id}님! 인증된 사용자입니다."}