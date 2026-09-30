from __future__ import annotations

import asyncio
import random
from typing import Any, Dict, Optional

import httpx

from mlsapi.config import ClientConfig
from mlsapi.errors import MlsApiError
from mlsapi.http import _handle_error_response


class AsyncHttpClient:
    """Asynchronous HTTP transport engine with automatic retries and exponential backoff."""

    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "x-api-key": config.api_key,
            "User-Agent": "mlsapi-python/0.1.0",
            "Accept": "application/json",
        }
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            headers=headers,
            timeout=config.timeout_seconds,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = path if path.startswith("http") else path.lstrip("/")
        attempts = 0
        max_retries = self.config.max_retries

        while True:
            attempts += 1
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    files=files,
                    data=data,
                )

                if response.status_code in (429, 500, 502, 503, 504) and attempts <= max_retries:
                    backoff = (2 ** (attempts - 1)) * 0.5 + random.uniform(0.1, 0.4)
                    await asyncio.sleep(backoff)
                    continue

                if response.is_error:
                    _handle_error_response(response)

                if response.status_code == 204:
                    return None

                return response.json()

            except (httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout) as exc:
                if attempts <= max_retries:
                    backoff = (2 ** (attempts - 1)) * 0.5 + random.uniform(0.1, 0.4)
                    await asyncio.sleep(backoff)
                    continue
                raise MlsApiError(f"Network error during {method} {url}: {exc}") from exc

    async def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        json: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return await self.request("POST", path, json=json, files=files, data=data, params=params)

    async def put(self, path: str, *, json: Optional[Any] = None) -> Any:
        return await self.request("PUT", path, json=json)

    async def delete(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return await self.request("DELETE", path, params=params)
