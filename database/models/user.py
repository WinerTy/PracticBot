from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .base import BaseModel


class User(BaseModel):
    phone: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    chat_id: Mapped[int]
