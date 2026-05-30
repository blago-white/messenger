from datetime import datetime
from datetime import UTC

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Enum

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import BaseModel
from .enums import MessageStatus


class Message(BaseModel):
    __tablename__ = "messages"

    chat_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chats.id", ondelete="CASCADE")
    )

    sender_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE")
    )

    text: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True
    )

    status: Mapped[MessageStatus] = mapped_column(
        Enum(MessageStatus),
        default=MessageStatus.SENT
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    chat = relationship(
        "Chat",
        back_populates="messages"
    )

    sender = relationship("User")

    attachments = relationship(
        "Attachment",
        back_populates="message",
        cascade="all, delete-orphan"
    )
