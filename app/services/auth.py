from uuid import UUID

import jwt
from sqlalchemy import select

from app.core.security import decode_token
from app.exceptions.auth import InvalidTokenError, UserNotFoundError
from app.models.user import User
from app.services.base import BaseService
from app.services.user import UserService


class AuthService(BaseService):
    def __init__(self, *args, user_service: UserService = None, **kwargs):
        super().__init__(*args, **kwargs)

        self._user_service = user_service or UserService(self._db)

    async def register(
        self,
        username: str,
        name: str,
        phone: str,
    ) -> User:
        if await self._check_unique_by_username(
            username
        ):
            raise ValueError("Username already exists")

        if await self._check_unique_by_phone(
            phone
        ):
            raise ValueError("Phone already exists")

        user = User(
            username=username,
            name=name,
            phone=phone,
        )

        self._db.add(user)

        await self._db.commit()

        await self._db.refresh(user)

        return user

    async def get_user_from_access_token(
        self,
        access_token: str,
    ) -> User:
        try:

            payload = decode_token(
                access_token
            )

            if payload.get("type") != "access":
                raise InvalidTokenError()

            user_id = UUID(
                payload["sub"]
            )

        except (
            jwt.PyJWTError,
            ValueError,
            KeyError,
        ):
            raise InvalidTokenError()

        user = await self._user_service.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return user

    async def _check_unique_by_phone(
        self,
        phone: str,
    ) -> bool:
        stmt = select(User).where(User.phone == phone)

        result = await self._db.execute(stmt)

        return result.scalar_one_or_none() is not None

    async def _check_unique_by_username(
        self,
        username: str,
    ) -> bool:

        stmt = select(User).where(User.username == username)

        result = await self._db.execute(stmt)

        return result.scalar_one_or_none() is not None
