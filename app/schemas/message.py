from uuid import UUID
from datetime import datetime

from app.schemas.base import BaseSchema


class MessageResponse(BaseSchema):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    status: str
    created_at: datetime

    text: str | None


class MessageDetailResponse(BaseSchema):
    id: UUID
    chat_id: UUID
    sender_id: UUID
    status: str
    created_at: datetime
    attachments: list[AttachmentResponse]

    text: str | None


class CreateMessageRequest(BaseSchema):
    text: str | None = Field(
        default=None,
        max_length=1024
    )
