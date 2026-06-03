from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_participant import (
    ChatParticipant,
)
from app.models.message import Message

from .base import BaseService


class MessageService(BaseService):
    async def send_message(
        self,
        chat_id: UUID,
        sender_id: UUID,
        text: str,
    ) -> Message:
        if not text.strip():
            raise ValueError("Message cannot be empty")

        if not await self._is_participant(
            chat_id,
            sender_id,
        ):
            raise ValueError("Access denied")

        message = Message(
            chat_id=chat_id,
            sender_id=sender_id,
            text=text,
        )

        self._db.add(message)

        await self._db.commit()

        await self._db.refresh(message)

        return message

    async def get_chat_messages(
        self,
        chat_id: UUID,
        user_id: UUID,
        limit: int = 50,
    ) -> list[Message]:
        if not await self._is_participant(
            chat_id,
            user_id,
        ):
            raise ValueError("Access denied")

        stmt = (
            select(Message)
            .where(
                Message.chat_id == chat_id
            )
            .order_by(
                Message.created_at.desc()
            )
            .limit(limit)
        )

        result = await self._db.execute(stmt)

        return list(result.scalars().all())

    async def _is_participant(
        self,
        chat_id: UUID,
        user_id: UUID,
    ) -> bool:
        stmt = select(
            ChatParticipant
        ).where(
            ChatParticipant.chat_id == chat_id,
            ChatParticipant.user_id == user_id,
        )

        result = await self._db.execute(stmt)

        return result.scalar_one_or_none() is not None
