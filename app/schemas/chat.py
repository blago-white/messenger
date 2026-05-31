from uuid import UUID

from app.schemas.base import BaseSchema


class ChatListItem(BaseSchema):
    id: UUID

    companion_name: str
    companion_username: str
    unread_count: int

    companion_avatar: str | None
    last_message: str | None


class CreateChatRequest(BaseSchema):
    user_id: UUID
