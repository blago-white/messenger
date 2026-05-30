from app.models.base import Base
from app.db.database import engine

import app.models


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

