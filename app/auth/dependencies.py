from fastapi import Depends, Header
from app.auth.auth import verify_access_token
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth import verify_access_token
from app.auth.auth import is_token_blacklisted



async def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]  # Bearer 토큰에서 토큰만 분리
    user_id = verify_access_token(token)
    # 여기서 DB 조회해 user 정보 반환해도 됨
    return user_id


security = HTTPBearer()

# 🚫 로그아웃된 토큰인지 검사하고, 정상이면 user_id 반환
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if await is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="로그아웃된 토큰입니다.")

    user_id = verify_access_token(token)
    return user_id