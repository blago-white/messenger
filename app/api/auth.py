from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas import UserResponse
from app.schemas.auth import (
    RegisterRequest,
    TokenResponse,
)

from app.core.security import get_user_id_from_refresh_token
from app.services.auth import AuthService
from app.services.user import UserService
from app.schemas import RefreshTokenRequest

router = APIRouter()


def get_auth_service(
    db: AsyncSession = Depends(get_db),
) -> AuthService:
    return AuthService(db)


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    return UserService(db)


@router.post(
    "/register",
    response_model=TokenResponse
)
async def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(
        get_auth_service
    )
):
    try:
        user = await auth_service.register(
            username=data.username,
            name=data.name,
            phone=data.phone,
        )

        access_token, refresh_token = (
            create_access_token(user.id),
            create_refresh_token(user.id)
        )

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
    return {
        "id": str(user.id),
        "username": user.username,
        "name": user.name,
    }


@router.post("/refresh")
async def refresh_token(
    data: RefreshTokenRequest,
    user_service: UserService = Depends(
        get_user_service
    )
):
    try:
        user_id = (
            get_user_id_from_refresh_token(
                data.refresh_token
            )
        )

        print(f"UID: {user_id}")

        user = (
            await user_service.get_by_id(
                user_id,
            )
        )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found",
            )

        access_token, refresh_token = (
            create_access_token(user.id),
            create_refresh_token(user.id)
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    except Exception as e:
        print(str(e))
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )
