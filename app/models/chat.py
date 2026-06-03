from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.testing.schema import mapped_column

from .base import BaseModel


class Chat(BaseModel):
    __tablename__ = "chats"

    participants = relationship(
        "ChatParticipant",
        back_populates="chat",
        cascade="all, delete-orphan"
    )

    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan"
    )

    is_group: Mapped[bool] = mapped_column(
        default=False
    )
