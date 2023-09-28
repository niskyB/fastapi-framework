from sqlalchemy import (
    Integer,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import mapped_column, Mapped


class BaseModel:
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
