from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
)
from utils import camel_case_to_snake_case


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_case_to_snake_case(cls.__name__)

    id: Mapped[int] = mapped_column(primary_key=True)
