import pytest_asyncio

from app.core.security import (
    create_access_token,
    create_refresh_token,
)


@pytest_asyncio.fixture
async def access_token(
    user_factory,
) -> str:

    user = await user_factory()

    return create_access_token(
        user.id
    )


@pytest_asyncio.fixture
async def refresh_token(
    user_factory,
) -> str:

    user = await user_factory()

    return create_refresh_token(
        user.id
    )


@pytest_asyncio.fixture
async def auth_user(
    user_factory,
):

    user = await user_factory()

    token = create_access_token(
        user.id
    )

    return user, token


@pytest_asyncio.fixture
async def authorized_headers(
    auth_user,
):
    _, token = auth_user

    return {
        "Authorization": f"Bearer {token}"
    }
