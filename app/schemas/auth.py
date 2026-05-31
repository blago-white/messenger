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



