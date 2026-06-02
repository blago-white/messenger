import uuid
from datetime import UTC, datetime

import jwt

from app.core import security as sec
from app.core.config import settings


def make_user_id():
    return uuid.uuid4()


def decode_without_verify(token: str):
    return jwt.decode(
        token,
        options={"verify_signature": False, "verify_exp": False},
    )


def test_create_access_token_contains_correct_payload():
    user_id = make_user_id()

    token = sec.create_access_token(user_id)
    payload = decode_without_verify(token)

    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"
    assert "exp" in payload


def test_create_refresh_token_contains_correct_payload():
    user_id = make_user_id()

    token = sec.create_refresh_token(user_id)
    payload = decode_without_verify(token)

    assert payload["sub"] == str(user_id)
    assert payload["type"] == "refresh"


def test_access_token_expiration_math():
    user_id = make_user_id()

    token = sec.create_access_token(user_id)
    payload = decode_without_verify(token)

    exp = datetime.fromtimestamp(payload["exp"], tz=UTC)

    delta = exp - datetime.now(UTC)

    assert abs(delta.total_seconds() - settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60) < 5


def test_refresh_token_expiration_math():
    user_id = make_user_id()

    token = sec.create_refresh_token(user_id)
    payload = decode_without_verify(token)

    exp = datetime.fromtimestamp(payload["exp"], tz=UTC)

    delta = exp - datetime.now(UTC)

    assert abs(delta.days - settings.REFRESH_TOKEN_EXPIRE_DAYS) <= 1


def test_decode_token_valid():
    user_id = make_user_id()

    token = sec.create_access_token(user_id)
    payload = sec.decode_token(token)

    assert payload["sub"] == str(user_id)


def test_get_user_id_from_access_token_success():
    user_id = make_user_id()

    token = sec.create_access_token(user_id)
    result = sec.get_user_id_from_access_token(token)

    assert result == user_id


def test_get_user_id_from_access_token_wrong_type():
    user_id = make_user_id()

    token = sec.create_refresh_token(user_id)

    import pytest
    with pytest.raises(ValueError, match="Invalid token type"):
        sec.get_user_id_from_access_token(token)


def test_get_user_id_from_refresh_token_success():
    user_id = make_user_id()

    token = sec.create_refresh_token(user_id)
    result = sec.get_user_id_from_refresh_token(token)

    assert result == user_id


def test_get_user_id_from_refresh_token_wrong_type():
    user_id = make_user_id()

    token = sec.create_access_token(user_id)

    import pytest
    with pytest.raises(ValueError, match="Invalid token type"):
        sec.get_user_id_from_refresh_token(token)
