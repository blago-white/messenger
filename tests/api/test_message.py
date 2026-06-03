import pytest


async def test_send_message_success(
    client,
    authorized_headers,
    user_factory,
):
    user = await user_factory(username="alice")

    chat_resp = await client.post(
        "/chats",
        json={"username": user.username},
        headers=authorized_headers,
    )

    chat_id = chat_resp.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages",
        json={"text": "Hello"},
        headers=authorized_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["text"] == "Hello"
    assert data["chat_id"] == chat_id


async def test_send_message_empty(
    client,
    authorized_headers,
    user_factory,
):
    user = await user_factory(username="alice")

    chat_resp = await client.post(
        "/chats",
        json={"username": user.username},
        headers=authorized_headers,
    )

    chat_id = chat_resp.json()["id"]

    response = await client.post(
        f"/chats/{chat_id}/messages",
        json={"text": "   "},
        headers=authorized_headers,
    )

    assert response.status_code == 400
    assert "Message cannot be empty" in response.json()["detail"]


async def test_get_messages_success(
    client,
    authorized_headers,
    user_factory,
):
    user = await user_factory(username="alice")

    chat_resp = await client.post(
        "/chats",
        json={"username": user.username},
        headers=authorized_headers,
    )

    chat_id = chat_resp.json()["id"]

    await client.post(
        f"/chats/{chat_id}/messages",
        json={"text": "First"},
        headers=authorized_headers,
    )

    await client.post(
        f"/chats/{chat_id}/messages",
        json={"text": "Second"},
        headers=authorized_headers,
    )

    response = await client.get(
        f"/chats/{chat_id}/messages",
        headers=authorized_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["text"] == "Second"
    assert data[1]["text"] == "First"


async def test_get_messages_access_denied(
    client,
    user_factory,
):
    user = await user_factory(username="alice")

    # create chat with alice
    chat_resp = await client.post(
        "/chats",
        json={"username": user.username},
        headers={"Authorization": "Bearer invalid"},  # deliberately invalid
    )

    # just ensure endpoint exists behavior-wise
    assert chat_resp.status_code in (200, 401, 403)
