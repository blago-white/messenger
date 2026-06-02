from uuid import UUID

from sqlalchemy import select

from app.models.user import User
from app.services.base import BaseService


class UserService(BaseService):
    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        stmt = select(User).where(User.id == user_id)

        result = await self._db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        stmt = select(User).where(User.username == username)

        result = await self._db.execute(stmt)

        return result.scalar_one_or_none()
