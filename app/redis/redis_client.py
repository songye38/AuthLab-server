
# redis 클라이언트 세팅

import aioredis
from dotenv import load_dotenv
import os

load_dotenv()  # 이거 꼭 해줘야 함

REDIS_URL = os.getenv("REDIS_URL")
redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)