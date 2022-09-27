import pytest

from falcon import testing

from luna import create_app


@pytest.fixture(scope="session")
def client() -> testing.TestClient:
    return testing.TestClient(create_app())
