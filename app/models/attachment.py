from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class Attachment(BaseModel):
    __tablename__ = "attachments"

    message_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="CASCADE")
    )

    file_path: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )

    message = relationship(
        "Message",
        back_populates="attachments"
    )
