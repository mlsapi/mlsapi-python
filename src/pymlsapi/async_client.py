from __future__ import annotations

from typing import Optional

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.config import (
    DEFAULT_JOB_TIMEOUT_SECONDS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_POLL_INTERVAL_SECONDS,
    DEFAULT_TIMEOUT_SECONDS,
    ClientConfig,
)
from pymlsapi.resources.account import AsyncAccountResource
from pymlsapi.resources.content import AsyncContentResource
from pymlsapi.resources.intelligence import AsyncIntelligenceResource
from pymlsapi.resources.listings import AsyncListingsResource
from pymlsapi.resources.studio import AsyncStudioResource


class AsyncMlsApiClient:
    """Official asynchronous Python client for mlsapi.dev.

    High-concurrency asyncio client for real-time MLS listings, property intelligence,
    marketing copy, and the complete suite of Studio Visual AI generative tools.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        environment: str = "live",
        base_url: Optional[str] = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_retries: int = DEFAULT_MAX_RETRIES,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
        job_timeout_seconds: float = DEFAULT_JOB_TIMEOUT_SECONDS,
    ) -> None:
        self.config = ClientConfig.create(
            api_key=api_key,
            environment=environment,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            poll_interval=poll_interval,
            job_timeout_seconds=job_timeout_seconds,
        )
        self._http = AsyncHttpClient(self.config)

        # Namespaced resources
        self.listings = AsyncListingsResource(self._http)
        self.intelligence = AsyncIntelligenceResource(self._http)
        self.content = AsyncContentResource(self._http)
        self.studio = AsyncStudioResource(self._http)
        self.account = AsyncAccountResource(self._http)

    async def close(self) -> None:
        """Close the underlying HTTP client transport."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncMlsApiClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()


# Convenient alias
AsyncMLS = AsyncMlsApiClient
