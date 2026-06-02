from collections.abc import AsyncGenerator

import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.db.database import get_db


@pytest.fixture
def client(db):
    async def override_get_db() -> AsyncGenerator:
        yield db

    app.dependency_overrides[get_db] = (
        override_get_db
    )

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
