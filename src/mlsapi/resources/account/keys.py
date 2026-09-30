from __future__ import annotations

from typing import Any, Dict, List

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient


class KeysResource:
    """Synchronous API key lifecycle and zero-downtime rotation."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> List[Dict[str, Any]]:
        """List active and grace-period expiring API keys."""
        data = self._http.get("/api/keys")
        return data.get("keys", [])

    def create(self, name: str, env: str = "test") -> Dict[str, Any]:
        """Create a new live or test API key."""
        return self._http.post("/api/keys", json={"name": name, "env": env})

    def rotate(self, key_id: str, grace_hours: int = 24) -> Dict[str, Any]:
        """Rotate key with a 24-hour grace overlap window."""
        return self._http.post(f"/api/keys/{key_id}/rotate", json={"graceHours": grace_hours})


class AsyncKeysResource:
    """Asynchronous API key lifecycle and zero-downtime rotation."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list(self) -> List[Dict[str, Any]]:
        """List active and grace-period expiring API keys."""
        data = await self._http.get("/api/keys")
        return data.get("keys", [])

    async def create(self, name: str, env: str = "test") -> Dict[str, Any]:
        """Create a new live or test API key."""
        return await self._http.post("/api/keys", json={"name": name, "env": env})

    async def rotate(self, key_id: str, grace_hours: int = 24) -> Dict[str, Any]:
        """Rotate key with a 24-hour grace overlap window."""
        return await self._http.post(f"/api/keys/{key_id}/rotate", json={"graceHours": grace_hours})
