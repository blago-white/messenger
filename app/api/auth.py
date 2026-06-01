from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.security import create_access_token, create_refresh_token
from app.db.database import get_db
from app.models.user import User
from app.schemas import UserResponse
from app.schemas.auth import (
    RegisterRequest,
    TokenResponse,
)
from app.services.auth import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse
)
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await AuthService.register(
            db=db,
            username=data.username,
            name=data.name,
            phone=data.phone,
        )

        access_token = create_access_token(user.id)

        refresh_token = create_refresh_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
async def me(
    user: User = Depends(get_current_user)
):
    print("@@@")
    return {
        "id": str(user.id),
        "username": user.username,
        "name": user.name,
    }
