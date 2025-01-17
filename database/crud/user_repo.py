from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User

from logger import logger


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_phone(self, phone: str) -> User | None:
        result = await self.session.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()

    async def create_user(self, phone: str, full_name: str, chat_id: int) -> User:
        new_user = User(phone=phone, full_name=full_name, chat_id=chat_id)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
