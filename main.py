
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId

load_dotenv()  # 이거 꼭 해줘야 함

app = FastAPI()

# MongoDB URI는 Railway 변수에서 불러오기
MONGO_URL = os.getenv("MONGO_URL")  # 이건 .env에 설정하거나 Railway에 입력

client = AsyncIOMotorClient(MONGO_URL)
db = client["myexperimentarchive"]  # 원하는 데이터베이스 이름
tags_collection = db["tags"]

print("MONGO_URL:", MONGO_URL)


origins = [
    "http://localhost:5173",  # React 개발서버 주소
    "https://myexperimentarchive.vercel.app",  # 필요하면 프로덕션 주소도 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인들
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메서드 허용 (GET, POST 등)
    allow_headers=["*"],  # 모든 헤더 허용
)
