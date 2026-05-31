from pydantic import Field

from app.schemas.base import BaseSchema


class SendCodeRequest(BaseSchema):
    phone: str = Field(
        min_length=6,
        max_length=20
    )


class VerifyCodeRequest(BaseSchema):
    phone: str

    code: str = Field(
        min_length=4,
        max_length=10
    )


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RegisterRequest(BaseSchema):
    username: str = Field(
        min_length=3,
        max_length=32
    )

    name: str = Field(
        min_length=1,
        max_length=64
    )

    phone: str = Field(
        min_length=6,
        max_length=20
    )
