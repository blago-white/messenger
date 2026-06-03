from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseSchema


class CreateChatRequest(BaseSchema):
    username: str = Field(
        min_length=3,
        max_length=32,
    )


class ChatListItem(BaseSchema):
    id: UUID

    companion_name: str
    companion_username: str

    unread_count: int = 0

    companion_avatar: str | None = None
    last_message: str | None = None
