from sqlalchemy import Column, Integer, String
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    cid = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)