from __future__ import annotations

from typing import Optional

from pymlsapi.config import (
    DEFAULT_JOB_TIMEOUT_SECONDS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_POLL_INTERVAL_SECONDS,
    DEFAULT_TIMEOUT_SECONDS,
    ClientConfig,
)
from pymlsapi.http import HttpClient
from pymlsapi.resources.account import AccountResource
from pymlsapi.resources.content import ContentResource
from pymlsapi.resources.intelligence import IntelligenceResource
from pymlsapi.resources.listings import ListingsResource
from pymlsapi.resources.studio import StudioResource


class MlsApiClient:
    """Official synchronous Python client for mlsapi.dev.

    Access real-time MLS listings, property intelligence, marketing copy,
    and the complete suite of Studio Visual AI generative tools.
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
        self._http = HttpClient(self.config)

        # Namespaced resources
        self.listings = ListingsResource(self._http)
        self.intelligence = IntelligenceResource(self._http)
        self.content = ContentResource(self._http)
        self.studio = StudioResource(self._http)
        self.account = AccountResource(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client transport."""
        self._http.close()

    def __enter__(self) -> MlsApiClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


# Convenient alias
MLS = MlsApiClient
