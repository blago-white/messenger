from uuid import uuid4

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


@pytest_asyncio.fixture
async def user_factory(
    db: AsyncSession,
):
    async def create_user(
        username: str | None = None,
        name: str = "Test User",
        phone: str | None = None,
    ) -> User:

        user = User(
            username=username or f"user_{uuid4().hex[:8]}",
            name=name,
            phone=phone or f"+7999{uuid4().int % 10000000:07d}",
        )

        db.add(user)

        await db.flush()

        await db.refresh(user)

        return user

    return create_user
