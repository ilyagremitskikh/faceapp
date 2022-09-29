from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, LargeBinary

from app.models.database import Base


class PornstarOrm(Base):
    __tablename__ = "pornstars"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    name = Column(String, nullable=False)
    image = Column(LargeBinary)


class PornstarModel(BaseModel):
    id: int = Field(description="Model Database ID", example="1")
    name: str = Field(description="Model Name", example="Mia Malkova")
    image: bytes = Field(description="Model Image bytes")
    distance: Optional[Decimal] = Field(description="Distance to target image", example="0.29124142")
    similarity: Optional[float] = Field(description="Similarity percentage", example=77)

    class Config:
        orm_mode = True
