import pytest

from app.services.auth import (
    AuthService,
    InvalidTokenError,
)


async def test_register_user(
    db,
):
    auth_service = AuthService(
        db
    )

    user = await auth_service.register(
        username="admin",
        name="Administrator",
        phone="+79991234567",
    )

    assert user.id is not None
    assert user.username == "admin"
    assert user.name == "Administrator"
    assert user.phone == "+79991234567"


async def test_register_duplicate_username(
    db,
    user_factory,
):
    auth_service = AuthService(
        db
    )

    await user_factory(
        username="admin"
    )

    with pytest.raises(
        ValueError,
        match="Username already exists",
    ):
        await auth_service.register(
            username="admin",
            name="Another User",
            phone="+79990000001",
        )


async def test_register_duplicate_phone(
    db,
    user_factory,
):
    auth_service = AuthService(
        db
    )

    await user_factory(
        phone="+79991234567"
    )

    with pytest.raises(
        ValueError,
        match="Phone already exists",
    ):
        await auth_service.register(
            username="another_user",
            name="Another User",
            phone="+79991234567",
        )


async def test_get_user_from_access_token(
    db,
    auth_user,
):
    user, token = auth_user

    auth_service = AuthService(
        db
    )

    current_user = (
        await auth_service.get_user_from_access_token(
            token
        )
    )

    assert current_user.id == user.id


async def test_invalid_access_token(
    db,
):
    auth_service = AuthService(
        db
    )

    with pytest.raises(
        InvalidTokenError
    ):
        await auth_service.get_user_from_access_token(
            "invalid_token"
        )
