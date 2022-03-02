from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from falcon.testing import TestClient


def test_successful_get(client: "TestClient") -> None:
    # GIVEN
    retailer_slug = "test-slug"
    expected_response = [f"mocked-{retailer_slug}-active-campaign"]

    # WHEN
    resp = client.simulate_get(f"/bpl/campaigns/{retailer_slug}/active-campaign-slugs")

    # THEN
    assert resp.status_code == 200
    assert resp.json == expected_response
