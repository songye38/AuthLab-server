from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
import app.db.models as models
from app.db.schemas import UserCreate, UserOut, UserLogin, TokenOut
from app.db.crud import create_user, get_user_by_email, verify_password
from app.auth.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.dependencies import verify_token, get_current_user
from app.db.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일이에요.")
    new_user = create_user(db, email=user.email, password=user.password)
    return new_user


@router.post("/login", response_model=TokenOut)
async def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 틀렸습니다.")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="인증된 사용자가 없습니다")
    return {"email": current_user.email, "id": current_user.id}


@router.get("/protected")
async def protected_route(user_id: str = Depends(verify_token)):
    return {"message": f"안녕하세요, {user_id}님! 인증된 사용자입니다."}
