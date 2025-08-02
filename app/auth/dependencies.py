from fastapi import Depends, Header
from app.auth.auth import verify_access_token
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth import verify_access_token, is_token_blacklisted


# 현재 사용자 정보를 가져오는 함수
# 이 함수는 인증 헤더에서 토큰을 추출하고, 토큰을 검증하여 사용자 ID를 반환합니다.
# 만약 토큰이 블랙리스트에 있다면 예외를 발생시킵니다.
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