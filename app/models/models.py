from decimal import Decimal
from typing import Optional

from app.models.database import Base
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, LargeBinary, String


class PornstarOrm(Base):
    __tablename__ = "pornstars"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=False)
    name = Column(String, nullable=False)
    image = Column(LargeBinary)


class PornstarModelBase(BaseModel):
    id: int = Field(description="Model Database ID", example="1")

    class Config:
        orm_mode = True


class PornstarModelTwins(PornstarModelBase):
    distance: Optional[float] = Field(
        description="Distance to target image", example="0.29124142"
    )
    similarity: Optional[float] = Field(description="Similarity percentage", example=77)


class PornstarModelFull(PornstarModelTwins):
    name: str = Field(description="Model Name", example="Mia Malkova")
    image: bytes = Field(description="Model Image bytes")
