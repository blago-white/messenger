from datetime import UTC
from datetime import datetime
from datetime import timedelta
from uuid import UUID

import jwt

from app.core.config import settings


def get_user_id_from_access_token(
    token: str,
) -> UUID:

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise ValueError(
            "Invalid token type"
        )

    return UUID(payload["sub"])


def create_access_token(user_id: UUID) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: UUID) -> str:
    expire = datetime.now(UTC) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )


def get_user_id_from_refresh_token(
    refresh_token: str,
) -> UUID:

    payload = decode_token(
        refresh_token
    )

    if payload.get("type") != "refresh":
        raise ValueError(
            "Invalid token type"
        )

    return UUID(payload["sub"])
