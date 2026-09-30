import httpx
import pytest
import respx

from mlsapi import (
    AuthenticationError,
    InsufficientCreditsError,
    InvalidRequestError,
    MlsApiClient,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)


@respx.mock
def test_401_authentication_error(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/A123").mock(
        return_value=httpx.Response(
            401, json={"error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}}
        )
    )
    with MlsApiClient(api_key=mock_api_key) as client:
        with pytest.raises(AuthenticationError) as exc:
            client.listings.get("A123")
        assert exc.value.status_code == 401
        assert "Invalid API key" in str(exc.value)


@respx.mock
def test_402_insufficient_credits_error(mock_api_key):
    respx.post("https://mlsapi.dev/v1/studio/staging/furnish").mock(
        return_value=httpx.Response(
            402, json={"error": {"code": "INSUFFICIENT_CREDITS", "message": "Top up required"}}
        )
    )
    with MlsApiClient(api_key=mock_api_key) as client:
        with pytest.raises(InsufficientCreditsError) as exc:
            client.studio.staging.stage(photo_url="https://img.jpg")
        assert exc.value.status_code == 402


@respx.mock
def test_403_permission_denied_error(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/A123").mock(
        return_value=httpx.Response(
            403, json={"error": {"code": "FORBIDDEN", "message": "Plan upgrade required"}}
        )
    )
    with MlsApiClient(api_key=mock_api_key) as client:
        with pytest.raises(PermissionDeniedError) as exc:
            client.listings.get("A123")
        assert exc.value.status_code == 403


@respx.mock
def test_404_not_found_error(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/UNKNOWN").mock(
        return_value=httpx.Response(
            404, json={"error": {"code": "NOT_FOUND", "message": "Listing not found"}}
        )
    )
    with MlsApiClient(api_key=mock_api_key) as client:
        with pytest.raises(NotFoundError) as exc:
            client.listings.get("UNKNOWN")
        assert exc.value.status_code == 404


@respx.mock
def test_400_invalid_request_error(mock_api_key):
    respx.post("https://mlsapi.dev/v1/studio/staging/furnish").mock(
        return_value=httpx.Response(
            400, json={"error": {"code": "BAD_REQUEST", "message": "Missing photo_url"}}
        )
    )
    with MlsApiClient(api_key=mock_api_key) as client:
        with pytest.raises(InvalidRequestError) as exc:
            client.studio.staging.stage(photo_url="")
        assert exc.value.status_code == 400


@respx.mock
def test_429_rate_limit_error_with_header(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/A123").mock(
        return_value=httpx.Response(
            429,
            headers={"retry-after": "5"},
            json={"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests"}},
        )
    )
    with MlsApiClient(api_key=mock_api_key, max_retries=0) as client:
        with pytest.raises(RateLimitError) as exc:
            client.listings.get("A123")
        assert exc.value.status_code == 429
        assert exc.value.retry_after_seconds == 5.0
