import pytest

from mlsapi import MLS, AsyncMlsApiClient, MlsApiClient


def test_client_init(mock_api_key):
    client = MlsApiClient(api_key=mock_api_key)
    assert client.config.api_key == mock_api_key
    assert client.config.environment == "live"
    assert client.config.base_url == "https://mlsapi.dev"
    client.close()


def test_client_env_var(monkeypatch, mock_api_key):
    monkeypatch.setenv("MLSAPI_KEY", mock_api_key)
    client = MLS()
    assert client.config.api_key == mock_api_key
    client.close()


def test_client_missing_key(monkeypatch):
    monkeypatch.delenv("MLSAPI_KEY", raising=False)
    with pytest.raises(ValueError, match="MLS API key is required"):
        MlsApiClient()


def test_async_client_context(mock_api_key):
    async def run():
        async with AsyncMlsApiClient(api_key=mock_api_key) as client:
            assert client.config.api_key == mock_api_key

    import asyncio

    asyncio.run(run())


def test_resources_exist(mock_api_key):
    with MlsApiClient(api_key=mock_api_key) as client:
        assert hasattr(client, "listings")
        assert hasattr(client, "intelligence")
        assert hasattr(client, "content")
        assert hasattr(client, "studio")
        assert hasattr(client.studio, "staging")
        assert hasattr(client.studio, "enhance")
        assert hasattr(client.studio, "floorplan")
        assert hasattr(client.studio, "render")
        assert hasattr(client.studio, "creatives")
        assert hasattr(client.studio, "social")
        assert hasattr(client.studio, "video")
        assert hasattr(client.studio, "custom")
        assert hasattr(client.studio, "upload")
        assert hasattr(client.studio, "jobs")
        assert hasattr(client, "account")
