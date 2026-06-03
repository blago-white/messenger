import pytest

from app.services.chat import ChatService


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
    user1 = await user_factory()
    user2 = await user_factory()
    user3 = await user_factory()

    service = ChatService(db)

    chat1 = await service.get_or_create_private_chat(
        user1.id,
        user2.id,
    )

    chat2 = await service.get_or_create_private_chat(
        user1.id,
        user3.id,
    )

    chats = await service.get_user_chats(
        user1.id
    )

    chat_ids = {
        chat.id
        for chat in chats
    }

    assert len(chats) == 2

    assert chat1.id in chat_ids
    assert chat2.id in chat_ids


async def test_get_user_chats_empty(
    db,
    user_factory,
):
    user = await user_factory()

    service = ChatService(db)

    chats = await service.get_user_chats(
        user.id
    )

    assert chats == []


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
