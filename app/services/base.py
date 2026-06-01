from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, db: AsyncSession):
        self._db = db
