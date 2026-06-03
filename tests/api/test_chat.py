import pytest


async def test_create_chat_success(
    client,
    authorized_headers,
    user_factory,
):
    user = await user_factory(username="alice")

    response = await client.post(
        "/chats",
        json={"username": user.username},
        headers=authorized_headers,
    )

    assert response.status_code == 200
    data = response.json()

    assert "id" in data


async def test_create_chat_user_not_found(
    client,
    authorized_headers,
):
    response = await client.post(
        "/chats",
        json={"username": "does_not_exist"},
        headers=authorized_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


async def test_get_chats_empty(
    client,
    authorized_headers,
):
    response = await client.get(
        "/chats",
        headers=authorized_headers,
    )

    assert response.status_code == 200
    assert response.json() == []
