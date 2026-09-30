import httpx
import respx

from mlsapi import MlsApiClient


@respx.mock
def test_billing_overview_and_checkout(mock_api_key):
    respx.get("https://mlsapi.dev/api/billing/overview").mock(
        return_value=httpx.Response(
            200,
            json={
                "tier": "Pro",
                "monthly_credits_total": 5000,
                "credits_remaining": 4200,
            },
        )
    )
    respx.post("https://mlsapi.dev/api/billing/checkout").mock(
        return_value=httpx.Response(
            200, json={"checkoutUrl": "https://checkout.stripe.com/session_123"}
        )
    )
    respx.post("https://mlsapi.dev/api/billing/portal").mock(
        return_value=httpx.Response(
            200, json={"portalUrl": "https://billing.stripe.com/portal_123"}
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        overview = client.account.get_billing_overview()
        assert overview["tier"] == "Pro"
        assert overview["credits_remaining"] == 4200

        checkout = client.account.billing.create_checkout_session(plan_id="Pro")
        assert "checkout.stripe.com" in checkout["checkoutUrl"]

        portal = client.account.billing.create_portal_session()
        assert "billing.stripe.com" in portal["portalUrl"]


@respx.mock
def test_keys_list_create_rotate(mock_api_key):
    respx.get("https://mlsapi.dev/api/keys").mock(
        return_value=httpx.Response(
            200,
            json={"keys": [{"id": "key_1", "name": "Production Key", "env": "live"}]},
        )
    )
    respx.post("https://mlsapi.dev/api/keys").mock(
        return_value=httpx.Response(200, json={"id": "key_2", "secret": "sk_test_newsecret123"})
    )
    respx.post("https://mlsapi.dev/api/keys/key_1/rotate").mock(
        return_value=httpx.Response(
            200, json={"oldKeyGraceExpiresAt": "2026-10-01T12:00:00Z", "newKey": {"id": "key_3"}}
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        keys = client.account.keys.list()
        assert len(keys) == 1
        assert keys[0]["id"] == "key_1"

        new_key = client.account.keys.create(name="Staging Key", env="test")
        assert new_key["id"] == "key_2"

        rotated = client.account.keys.rotate("key_1", grace_hours=24)
        assert "oldKeyGraceExpiresAt" in rotated
