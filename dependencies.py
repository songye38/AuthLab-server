from fastapi import Depends, Header
from auth import verify_access_token

async def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]  # Bearer 토큰에서 토큰만 분리
    user_id = verify_access_token(token)
    # 여기서 DB 조회해 user 정보 반환해도 됨
    return user_id