from __future__ import annotations

import random
import time
from typing import Any, Dict, Optional

import httpx

from mlsapi.config import ClientConfig
from mlsapi.errors import (
    AuthenticationError,
    InsufficientCreditsError,
    InvalidRequestError,
    MlsApiError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
)


def _handle_error_response(response: httpx.Response) -> None:
    status = response.status_code
    try:
        body = response.json()
    except Exception:
        body = {"message": response.text}

    msg = body.get("error", {})
    if isinstance(msg, dict):
        message = msg.get("message") or str(body)
        code = msg.get("code", "API_ERROR")
    else:
        message = str(msg) if msg else body.get("message", response.text or "Unknown error")
        code = body.get("code", "API_ERROR")

    if status == 401:
        raise AuthenticationError(message, status_code=status, code=code, raw_response=body)
    elif status == 402:
        raise InsufficientCreditsError(message, status_code=status, code=code, raw_response=body)
    elif status == 403:
        raise PermissionDeniedError(message, status_code=status, code=code, raw_response=body)
    elif status == 404:
        raise NotFoundError(message, status_code=status, code=code, raw_response=body)
    elif status == 400:
        raise InvalidRequestError(message, status_code=status, code=code, raw_response=body)
    elif status == 429:
        retry_after = None
        if "retry-after" in response.headers:
            try:
                retry_after = float(response.headers["retry-after"])
            except ValueError:
                pass
        raise RateLimitError(
            message,
            status_code=status,
            code=code,
            retry_after_seconds=retry_after,
            raw_response=body,
        )
    else:
        raise MlsApiError(message, status_code=status, code=code, raw_response=body)


class HttpClient:
    """Synchronous HTTP transport engine with automatic retries and exponential backoff."""

    def __init__(self, config: ClientConfig) -> None:
        self.config = config
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "x-api-key": config.api_key,
            "User-Agent": "mlsapi-python/0.1.0",
            "Accept": "application/json",
        }
        self._client = httpx.Client(
            base_url=config.base_url,
            headers=headers,
            timeout=config.timeout_seconds,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def request(
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
                response = self._client.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    files=files,
                    data=data,
                )

                if response.status_code in (429, 500, 502, 503, 504) and attempts <= max_retries:
                    # Exponential backoff with jitter
                    backoff = (2 ** (attempts - 1)) * 0.5 + random.uniform(0.1, 0.4)
                    time.sleep(backoff)
                    continue

                if response.is_error:
                    _handle_error_response(response)

                if response.status_code == 204:
                    return None

                return response.json()

            except (httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout) as exc:
                if attempts <= max_retries:
                    backoff = (2 ** (attempts - 1)) * 0.5 + random.uniform(0.1, 0.4)
                    time.sleep(backoff)
                    continue
                raise MlsApiError(f"Network error during {method} {url}: {exc}") from exc

    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("GET", path, params=params)

    def post(
        self,
        path: str,
        *,
        json: Optional[Any] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        return self.request("POST", path, json=json, files=files, data=data, params=params)

    def put(self, path: str, *, json: Optional[Any] = None) -> Any:
        return self.request("PUT", path, json=json)

    def delete(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("DELETE", path, params=params)
