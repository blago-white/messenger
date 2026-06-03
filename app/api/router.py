from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.message import router as msg_router
from app.api.chat import router as chat_router

api_router = APIRouter()

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"]
)

api_router.include_router(
    msg_router,
    tags=["Message"]
)

api_router.include_router(
    chat_router,
    tags=["Chat"]
)
