from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.auth import (
    get_auth_service,
    get_user_service,
)
from app.api.dependencies import (
    get_current_user,
)
from app.main import app
from app.models.user import User


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_overrides():
    app.dependency_overrides.clear()

    yield

    app.dependency_overrides.clear()


def test_register_success(client):
    user = User(
        id=uuid4(),
        username="admin",
        name="Administrator",
        phone="+79991234567",
    )

    auth_service = AsyncMock()
    auth_service.register.return_value = user

    app.dependency_overrides[
        get_auth_service
    ] = lambda: auth_service

    response = client.post(
        "/auth/register",
        json={
            "username": "admin",
            "name": "Administrator",
            "phone": "+79991234567",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "Bearer"


def test_register_duplicate_username(client):
    auth_service = AsyncMock()

    auth_service.register.side_effect = (
        ValueError(
            "Username already exists"
        )
    )

    app.dependency_overrides[
        get_auth_service
    ] = lambda: auth_service

    response = client.post(
        "/auth/register",
        json={
            "username": "admin",
            "name": "Administrator",
            "phone": "+79991234567",
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Username already exists"
    }


def test_me_success(client):
    user = User(
        id=uuid4(),
        username="admin",
        name="Administrator",
        phone="+79991234567",
    )

    app.dependency_overrides[
        get_current_user
    ] = lambda: user

    response = client.get("/auth/me")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == str(user.id)
    assert body["username"] == "admin"
    assert body["name"] == "Administrator"


def test_refresh_success(client):
    user = User(
        id=uuid4(),
        username="admin",
        name="Administrator",
        phone="+79991234567",
    )

    user_service = AsyncMock()
    user_service.get_by_id.return_value = user

    app.dependency_overrides[
        get_user_service
    ] = lambda: user_service

    client.post(
        "/auth/refresh",
        json={
            "refresh_token": "fake_token"
        },
    )
