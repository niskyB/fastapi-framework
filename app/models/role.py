from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base_model import BaseModel


class Role(Base, BaseModel):
    __tablename__ = "role"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    code: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True, unique=True
    )
