from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.chat import Chat
from app.models.chat_participant import ChatParticipant
from app.schemas import ChatListItem

from .base import BaseService


class ChatService(BaseService):
    async def get_or_create_private_chat(
        self,
        user1_id: UUID,
        user2_id: UUID,
    ) -> Chat:

        if user1_id == user2_id:
            raise ValueError(
                "Cannot create chat with yourself"
            )

        existing_chat = (
            await self._find_private_chat(
                user1_id,
                user2_id,
            )
        )

        if existing_chat is not None:
            return existing_chat

        chat = Chat()

        self._db.add(chat)

        await self._db.flush()

        self._db.add_all(
            [
                ChatParticipant(
                    chat_id=chat.id,
                    user_id=user1_id,
                ),
                ChatParticipant(
                    chat_id=chat.id,
                    user_id=user2_id,
                ),
            ]
        )

        await self._db.commit()

        await self._db.refresh(chat)

        return chat

    # async def get_user_chats(
    #     self,
    #     user_id: UUID,
    # ) -> list[Chat]:
    #
    #     stmt = (
    #         select(Chat)
    #         .join(ChatParticipant)
    #         .where(
    #             ChatParticipant.user_id == user_id
    #         )
    #         .order_by(
    #             Chat.created_at.desc()
    #         )
    #     )
    #
    #     result = await self._db.execute(
    #         stmt
    #     )
    #
    #     return list(
    #         result.scalars().unique().all()
    #     )

    async def get_chat_list(
        self,
        user_id: UUID,
    ) -> list[ChatListItem]:

        stmt = (
            select(Chat)
            .join(ChatParticipant)
            .where(
                ChatParticipant.user_id == user_id
            )
            .options(
                selectinload(Chat.participants)
                .selectinload(ChatParticipant.user),
                selectinload(Chat.messages),
            )
            .order_by(
                Chat.created_at.desc()
            )
        )

        result = await self._db.execute(stmt)

        chats = result.scalars().unique().all()

        items = []

        for chat in chats:
            companion = next(
                (
                    participant.user
                    for participant in chat.participants
                    if participant.user_id != user_id
                ),
                None,
            )

            if companion is None:
                continue

            last_message = None

            if chat.messages:
                last_message = max(
                    chat.messages,
                    key=lambda m: m.created_at,
                ).text

            items.append(
                ChatListItem(
                    id=chat.id,
                    companion_name=companion.name,
                    companion_username=companion.username,
                    companion_avatar=companion.avatar,
                    unread_count=0,
                    last_message=last_message,
                )
            )

        return items


    async def is_chat_participant(
        self,
        chat_id: UUID,
        user_id: UUID,
    ) -> bool:

        stmt = (
            select(ChatParticipant)
            .where(
                ChatParticipant.chat_id == chat_id,
                ChatParticipant.user_id == user_id,
            )
        )

        result = await self._db.execute(
            stmt
        )

        return (
            result.scalar_one_or_none()
            is not None
        )

    async def _find_private_chat(
        self,
        user1_id: UUID,
        user2_id: UUID,
    ) -> Chat | None:

        stmt = (
            select(Chat)
            .join(ChatParticipant)
            .where(
                ChatParticipant.user_id.in_(
                    [user1_id, user2_id]
                )
            )
            .group_by(Chat.id)
            .having(
                func.count(
                    ChatParticipant.user_id
                ) == 2
            )
        )

        result = await self._db.execute(
            stmt
        )

        return result.scalar_one_or_none()
