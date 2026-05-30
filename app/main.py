import dotenv

dotenv.load_dotenv()

import asyncio

from app.db.init_db import create_tables

asyncio.run(create_tables())

# from models.base import Base
#
# print(Base.metadata.tables.keys())
