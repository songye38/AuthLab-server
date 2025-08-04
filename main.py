
# 제일 첫번째 진입점에서 FastAPI 앱을 설정하고 라우팅을 정의합니다.
# 이 파일은 서버를 실행할 때 가장 먼저 실행되는 파일입니다.


from fastapi import FastAPI, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.db.models import Base
from app.db.schemas import UserCreate, UserOut
from app.db.crud import create_user
import app.db.models as models
from app.auth.dependencies import verify_token  # 이 경로는 실제 구조에 맞게 조정
from app.db.crud import get_user_by_email, verify_password
from app.auth.auth import create_access_token
from app.db.schemas import UserCreate, UserOut, UserLogin, TokenOut
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth import ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.dependencies import get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 프론트 도메인 명확히 넣기
    allow_credentials=True,  # 이게 핵심!
    allow_methods=["*"],
    allow_headers=["*"],
)

# 사용자 회원가입 처리 API 엔드포인트
@app.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)): #의존성 주입 방식
    # 이메일 중복 확인
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일이에요.")
    new_user = create_user(db, email=user.email, password=user.password)
    return new_user


@app.get("/protected")
async def protected_route(user_id: str = Depends(verify_token)):
    return {"message": f"안녕하세요, {user_id}님! 인증된 사용자입니다."}


@app.post("/login", response_model=TokenOut) #리턴 데이터 타입 정의 
async def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 틀렸습니다.")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 틀렸습니다.")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    # 쿠키에 토큰 세팅
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # HTTPS면 True로 바꿔야 함
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    # JSON 응답도 원하면 이렇게
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {"email": current_user.email, "id": current_user.id}