from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.message import CreateMessageRequest
from app.services.message import MessageService

router = APIRouter()


def get_message_service(
    db: AsyncSession = Depends(get_db),
) -> MessageService:
    return MessageService(db)


@router.post("/chats/{chat_id}/messages")
async def send_message(
    chat_id: str,
    data: CreateMessageRequest,
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service),
):
    try:
        message = await message_service.send_message(
            chat_id=chat_id,
            sender_id=current_user.id,
            text=data.text,
        )

        return {
            "id": message.id,
            "chat_id": message.chat_id,
            "sender_id": message.sender_id,
            "text": message.text,
            "status": message.status,
            "created_at": message.created_at,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/chats/{chat_id}/messages")
async def get_messages(
    chat_id: str,
    current_user: User = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service),
    limit: int = Query(default=50, le=100),
):
    try:
        messages = await message_service.get_chat_messages(
            chat_id=chat_id,
            user_id=current_user.id,
            limit=limit,
        )

        return [
            {
                "id": msg.id,
                "chat_id": msg.chat_id,
                "sender_id": msg.sender_id,
                "text": msg.text,
                "status": msg.status,
                "created_at": msg.created_at,
            }
            for msg in messages
        ]

    except ValueError as e:
        raise HTTPException(
            status_code=403,
            detail=str(e),
        )
