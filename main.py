from motor.motor_asyncio import AsyncIOMotorClient
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





# ObjectId를 문자열로 바꾸는 헬퍼 함수
def serialize_item(item):
    item["_id"] = str(item["_id"])
    return item


@app.get("/items")
async def get_items():
    items = await db["tags"].find().to_list(100)
    return [serialize_item(item) for item in items]



# 🔸 request body 스키마
class TagRequest(BaseModel):
    parentId: str
    content: str

# 🔸 POST: 태그 추가
@app.post("/api/save-description")
async def add_tag(request: TagRequest):
    try:
        obj_id = ObjectId(request.parentId)

        result = await tags_collection.update_one(
            {"_id": obj_id},
            {"$push": {"tags": request.content}}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="문서를 찾을 수 없음")

        return {"message": "태그가 성공적으로 추가되었습니다."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")