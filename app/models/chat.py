from sqlalchemy.orm import relationship

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
