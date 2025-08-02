
# sqlalchemy 모델 정의
# 이 파일은 데이터베이스 테이블 구조를 정의합니다.




from sqlalchemy import Column, Integer, String
from app.db.database import Base


# User 모델 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
