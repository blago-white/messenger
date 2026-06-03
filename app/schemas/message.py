from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.models.enums import MessageStatus
from app.schemas.base import BaseSchema

from .attachment import AttachmentResponse


class CreateMessageRequest(BaseSchema):
    text: str = Field(
        min_length=1,
        max_length=1024,
    )


class MessageResponse(BaseSchema):
    id: UUID
    chat_id: UUID
    sender_id: UUID

    status: MessageStatus
    created_at: datetime

    text: str | None


class MessageDetailResponse(BaseSchema):
    id: UUID
    chat_id: UUID
    sender_id: UUID

    status: MessageStatus
    created_at: datetime

    attachments: list[AttachmentResponse]

    text: str | None
