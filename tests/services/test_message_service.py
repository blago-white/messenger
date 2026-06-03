import pytest

from app.services.chat import ChatService
from app.services.message import MessageService


async def test_send_message(
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

    message = await message_service.send_message(
        chat.id,
        user1.id,
        "Hello",
    )

    assert message.id is not None
    assert message.chat_id == chat.id
    assert message.sender_id == user1.id
    assert message.text == "Hello"


async def test_send_empty_message(
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

    with pytest.raises(
        ValueError,
        match="Message cannot be empty",
    ):
        await message_service.send_message(
            chat.id,
            user1.id,
            "   ",
        )


async def test_send_message_access_denied(
    db,
    user_factory,
):
    user1 = await user_factory()
    user2 = await user_factory()
    outsider = await user_factory()

    chat_service = ChatService(db)
    message_service = MessageService(db)

    chat = await chat_service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    with pytest.raises(
        ValueError,
        match="Access denied",
    ):
        await message_service.send_message(
            chat.id,
            outsider.id,
            "Hello",
        )


async def test_get_chat_messages(
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
        "First",
    )

    await message_service.send_message(
        chat.id,
        user2.id,
        "Second",
    )

    messages = await message_service.get_chat_messages(
        chat.id,
        user1.id,
    )

    assert len(messages) == 2

    # DESC order by created_at
    assert messages[0].text == "Second"
    assert messages[1].text == "First"


async def test_get_chat_messages_limit(
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

    for i in range(5):
        await message_service.send_message(
            chat.id,
            user1.id,
            f"Message {i}",
        )

    messages = await message_service.get_chat_messages(
        chat.id,
        user1.id,
        limit=3,
    )

    assert len(messages) == 3


async def test_get_chat_messages_access_denied(
    db,
    user_factory,
):
    user1 = await user_factory()
    user2 = await user_factory()
    outsider = await user_factory()

    chat_service = ChatService(db)
    message_service = MessageService(db)

    chat = await chat_service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    with pytest.raises(
        ValueError,
        match="Access denied",
    ):
        await message_service.get_chat_messages(
            chat.id,
            outsider.id,
        )


async def test_get_chat_messages_empty_chat(
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

    messages = await message_service.get_chat_messages(
        chat.id,
        user1.id,
    )

    assert messages == []
