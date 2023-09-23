from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def is_valid_uuid():
    def wrapped(uuid_to_test):
        try:
            uuid_obj = UUID(uuid_to_test, version=4)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test

    return wrapped
