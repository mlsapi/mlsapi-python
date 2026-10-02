from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_LIVE_URL = "https://mlsapi.dev"
DEFAULT_TEST_URL = "https://mlsapi.dev"  # same host; the environment is sent as `x-key-env`
DEFAULT_TIMEOUT_SECONDS = 60.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_POLL_INTERVAL_SECONDS = 2.0
DEFAULT_JOB_TIMEOUT_SECONDS = 90.0


@dataclass
class ClientConfig:
    """Configuration options for the MLS API Client."""

    api_key: str
    environment: str = "live"
    base_url: str = DEFAULT_LIVE_URL
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    max_retries: int = DEFAULT_MAX_RETRIES
    poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS
    job_timeout_seconds: float = DEFAULT_JOB_TIMEOUT_SECONDS

    @classmethod
    def create(
        cls,
        api_key: Optional[str] = None,
        environment: str = "live",
        base_url: Optional[str] = None,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_retries: int = DEFAULT_MAX_RETRIES,
        poll_interval: float = DEFAULT_POLL_INTERVAL_SECONDS,
        job_timeout_seconds: float = DEFAULT_JOB_TIMEOUT_SECONDS,
    ) -> ClientConfig:
        resolved_key = api_key or os.environ.get("MLSAPI_KEY")
        if not resolved_key:
            raise ValueError(
                "MLS API key is required. Pass `api_key` to client or set MLSAPI_KEY environment variable."
            )

        if base_url is None:
            base_url = DEFAULT_LIVE_URL if environment == "live" else DEFAULT_TEST_URL

        # Strip trailing slashes
        base_url = base_url.rstrip("/")

        return cls(
            api_key=resolved_key,
            environment=environment,
            base_url=base_url,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            poll_interval=poll_interval,
            job_timeout_seconds=job_timeout_seconds,
        )
