import pytest

from app.services.chat import ChatService
from app.services.message import MessageService


async def test_create_private_chat(
    db,
    user_factory,
):
    user1 = await user_factory()
    user2 = await user_factory()

    service = ChatService(db)

    chat = await service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    assert chat.id is not None

    assert await service.is_chat_participant(
        chat.id,
        user1.id,
    )

    assert await service.is_chat_participant(
        chat.id,
        user2.id,
    )


async def test_get_existing_private_chat(
    db,
    user_factory,
):
    user1 = await user_factory()
    user2 = await user_factory()

    service = ChatService(db)

    chat1 = await service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    chat2 = await service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    assert chat1.id == chat2.id


async def test_create_chat_with_yourself(
    db,
    user_factory,
):
    user = await user_factory()

    service = ChatService(db)

    with pytest.raises(
        ValueError,
        match="Cannot create chat with yourself",
    ):
        await service.get_or_create_private_chat(
            user.id,
            user.id,
        )


async def test_get_user_chats(
    db,
    user_factory,
):
    user1 = await user_factory(
        username="user1",
        name="User One",
    )

    user2 = await user_factory(
        username="user2",
        name="User Two",
    )

    user3 = await user_factory(
        username="user3",
        name="User Three",
    )

    service = ChatService(db)

    chat1 = await service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    chat2 = await service.get_or_create_private_chat(
        user1.id,
        user3.id,
    )

    chats = await service.get_chat_list(
        user1.id
    )

    assert len(chats) == 2

    chat_map = {
        chat.id: chat
        for chat in chats
    }

    assert chat1.id in chat_map
    assert chat2.id in chat_map

    first_chat = chat_map[chat1.id]

    assert first_chat.companion_username == "user2"
    assert first_chat.companion_name == "User Two"
    assert first_chat.unread_count == 0
    assert first_chat.last_message is None

    second_chat = chat_map[chat2.id]

    assert second_chat.companion_username == "user3"
    assert second_chat.companion_name == "User Three"
    assert second_chat.unread_count == 0
    assert second_chat.last_message is None


async def test_get_user_chats_empty(
    db,
    user_factory,
):
    user = await user_factory()

    service = ChatService(db)

    chats = await service.get_chat_list(
        user.id
    )

    assert chats == []


async def test_get_user_chats_contains_last_message(
    db,
    user_factory,
):
    user1 = await user_factory()
    user2 = await user_factory()

    chat_service = ChatService(db)
    message_service = MessageService(db)

    chat = await chat_service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    await message_service.send_message(
        chat.id,
        user1.id,
        "Hello",
    )

    chats = await chat_service.get_chat_list(
        user1.id
    )

    assert len(chats) == 1
    assert chats[0].last_message == "Hello"


async def test_is_chat_participant_true(
    db,
    user_factory,
):
    user1 = await user_factory()
    user2 = await user_factory()

    service = ChatService(db)

    chat = await service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    result = await service.is_chat_participant(
        chat.id,
        user1.id,
    )

    assert result is True


async def test_is_chat_participant_false(
    db,
    user_factory,
):
    user1 = await user_factory()
    user2 = await user_factory()
    outsider = await user_factory()

    service = ChatService(db)

    chat = await service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    result = await service.is_chat_participant(
        chat.id,
        outsider.id,
    )

    assert result is False
