from fastapi import Depends
from app.auth.auth import verify_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,OAuth2PasswordBearer
from app.auth.auth import verify_access_token, is_token_blacklisted
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.database import get_db
import app.db.models as models
from dotenv import load_dotenv
import os
from jwt import ExpiredSignatureError, InvalidTokenError



load_dotenv()  # 이거 꼭 해줘야 함

SECRET_KEY = os.getenv("SECRET_KEY")  # 이건 .env에 설정하거나 Railway에 입력
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 현재 사용자 정보를 가져오는 함수
# 이 함수는 인증 헤더에서 토큰을 추출하고, 토큰을 검증하여 사용자 ID를 반환합니다.
# 만약 토큰이 블랙리스트에 있다면 예외를 발생시킵니다.
from fastapi import Request

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="토큰이 없습니다.")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="토큰에 사용자 정보가 없습니다.")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="사용자가 존재하지 않습니다.")
    return user





security = HTTPBearer()

# 🚫 로그아웃된 토큰인지 검사하고, 정상이면 user_id 반환
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if await is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="로그아웃된 토큰입니다.")

    user_id = verify_access_token(token)
    return user_id