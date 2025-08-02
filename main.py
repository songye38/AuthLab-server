from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base
from schemas import UserCreate, UserOut
from crud import create_user
import models

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