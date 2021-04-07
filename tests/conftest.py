import pytest

from falcon import testing

from app import create_app


@pytest.fixture(scope="session")
def client() -> testing.TestClient:
    return testing.TestClient(create_app())
