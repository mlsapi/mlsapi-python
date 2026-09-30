from __future__ import annotations

from typing import Callable, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import StudioJob
from mlsapi.poller import poll_job_async, poll_job_sync


class StudioJobsResource:
    """Synchronous tracking and polling for Studio AI background jobs."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, job_id: str) -> StudioJob:
        """Fetch current status and progress of a Studio job."""
        data = self._http.get(f"/v1/studio/jobs/{job_id}")
        return StudioJob.model_validate(data)

    def wait_for(
        self,
        job_id: str,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> StudioJob:
        """Poll job until completion, returning final StudioJob with result."""

        def fetch_job() -> StudioJob:
            return self.get(job_id)

        def is_done(job: StudioJob) -> bool:
            return job.status == "completed"

        def is_failed(job: StudioJob) -> bool:
            return job.status == "failed"

        return poll_job_sync(
            fetch_fn=fetch_job,
            is_done_fn=is_done,
            is_failed_fn=is_failed,
            timeout_seconds=timeout_seconds,
            initial_interval=poll_interval,
            on_progress=on_progress,
        )


class AsyncStudioJobsResource:
    """Asynchronous tracking and polling for Studio AI background jobs."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self, job_id: str) -> StudioJob:
        """Fetch current status and progress of a Studio job."""
        data = await self._http.get(f"/v1/studio/jobs/{job_id}")
        return StudioJob.model_validate(data)

    async def wait_for(
        self,
        job_id: str,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> StudioJob:
        """Poll job until completion, returning final StudioJob with result."""

        async def fetch_job() -> StudioJob:
            return await self.get(job_id)

        def is_done(job: StudioJob) -> bool:
            return job.status == "completed"

        def is_failed(job: StudioJob) -> bool:
            return job.status == "failed"

        return await poll_job_async(
            fetch_fn=fetch_job,
            is_done_fn=is_done,
            is_failed_fn=is_failed,
            timeout_seconds=timeout_seconds,
            initial_interval=poll_interval,
            on_progress=on_progress,
        )
