from uuid import UUID

from app.schemas.base import BaseSchema


class AttachmentResponse(BaseSchema):
    id: UUID

    file_path: str
