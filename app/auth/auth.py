
# 이 파일은 JWT 토큰을 생성하고 검증하는 기능을 제공합니다.     
# FastAPI에서 인증 및 권한 부여를 구현할 때 사용됩니다.

from dotenv import load_dotenv
import os
import jwt as pyjwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import redis

load_dotenv()  # 이거 꼭 해줘야 함

SECRET_KEY = os.getenv("SECRET_KEY")  # 이건 .env에 설정하거나 Railway에 입력
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30분 유효



# JWT 토큰 생성 함수
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = pyjwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# JWT 토큰 검증 함수
def verify_access_token(token: str):
    try:
        payload = pyjwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except pyjwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    

 # 토큰이 블랙리스트에 있는지 확인
async def is_token_blacklisted(token: str) -> bool:
    value = await redis.get(token)
    return value == "blacklisted"
