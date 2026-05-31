from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class AuthService:
    @staticmethod
    async def register(
        db: AsyncSession,
        username: str,
        name: str,
        phone: str,
    ) -> User:

        stmt = select(User).where(
            User.username == username
        )

        result = await db.execute(stmt)

        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise ValueError(
                "Username already exists"
            )

        user = User(
            username=username,
            name=name,
            phone=phone,
        )

        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user
