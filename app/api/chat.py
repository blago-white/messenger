from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.chat import CreateChatRequest
from app.services.chat import ChatService
from app.services.user import UserService

router = APIRouter()


def get_chat_service(
    db: AsyncSession = Depends(get_db),
) -> ChatService:
    return ChatService(db)


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    return UserService(db)


@router.post("/chats")
async def create_chat(
    data: CreateChatRequest,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
    user_service: UserService = Depends(get_user_service),
):
    target_user = await user_service.get_by_username(data.username)

    if target_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    try:
        chat = await chat_service.get_or_create_private_chat(
            current_user.id,
            target_user.id,
        )

        return {"id": chat.id}

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/chats")
async def get_chats(
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service),
):
    chats = await chat_service.get_chat_list(current_user.id)

    return chats
