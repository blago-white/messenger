from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseSchema

__all__ = ["UserResponse", "UserUpdate"]


class UserResponse(BaseSchema):
    id: UUID
    username: str
    name: str
    avatar: str | None = None


class UserUpdate(BaseSchema):
    name: str | None = Field(
        default=None,
        max_length=64
    )

    avatar: str | None = None
