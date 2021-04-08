import uuid

from time import perf_counter
from typing import TYPE_CHECKING

import pytest

from app.resources import PolarisEnrolCallback

if TYPE_CHECKING:
    from falcon.testing import TestClient


@pytest.fixture(scope="module")
def callback_payload() -> dict:
    return {"UUID": str(uuid.uuid4())}


def test_successful_callback(client: "TestClient") -> None:
    resp = client.simulate_post("/enrol/callback/success")
    assert resp.status_code == 200


def test_error_callback(client: "TestClient") -> None:
    resp = client.simulate_post("/enrol/callback/error")
    assert resp.status_code == 500


def test_timeout_callback(client: "TestClient") -> None:
    requested_timeout = 2  # seconds
    start = perf_counter()
    resp = client.simulate_post("/enrol/callback/timeout-%d" % requested_timeout)
    assert requested_timeout == int(perf_counter() - start)
    assert resp.status_code == 200


def test_retry_callback(client: "TestClient", callback_payload: dict) -> None:
    requested_failures = 2

    for i in range(requested_failures, 0, -1):
        resp = client.simulate_post("/enrol/callback/retry-%d" % requested_failures, json=callback_payload)
        assert resp.status_code == 200 if i == 0 else 500

    resp = client.simulate_post("/enrol/callback/retry", json={})
    assert resp.status_code == 422


def test_get_secondary_param() -> None:
    route = "test-%d"
    default_value = 5
    max_val = 10
    min_val = 3

    test_value = 8
    result = PolarisEnrolCallback._get_secondary_param(route % test_value, default_value, max_val, min_val)
    assert result == test_value

    test_value = 11
    result = PolarisEnrolCallback._get_secondary_param(route % test_value, default_value, max_val, min_val)
    assert result == default_value

    test_value = 2
    result = PolarisEnrolCallback._get_secondary_param(route % test_value, default_value, max_val, min_val)
    assert result == default_value

    route = "retry"
    result = PolarisEnrolCallback._get_secondary_param(route, default_value, max_val, min_val)
    assert result == default_value
