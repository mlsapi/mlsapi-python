from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.listings import BaseListing, IngestJob
from pymlsapi.poller import poll_job_async, poll_job_sync


class ListingsResource:
    """Synchronous MLS listings and ingestion operations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, mls_id: str) -> Union[BaseListing, IngestJob]:
        """Lookup an MLS listing. If not cached, returns an IngestJob in progress."""
        data = self._http.get(f"/v1/listing/{mls_id}")
        if "status" in data and data["status"] in ("processing", "queued"):
            return IngestJob.model_validate(data)
        return BaseListing.model_validate(data)

    def get_and_wait(
        self,
        mls_id: str,
        timeout_seconds: float = 60.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[IngestJob], None]] = None,
    ) -> BaseListing:
        """Fetch listing and automatically poll until ingestion completes."""
        initial = self.get(mls_id)
        if isinstance(initial, BaseListing):
            return initial

        job_id = initial.job_id or (getattr(initial, "job_id", None) or mls_id)

        def fetch_job() -> IngestJob:
            data = self._http.get(f"/jobs/{job_id}")
            return IngestJob.model_validate(data)

        def is_done(job: IngestJob) -> bool:
            return job.status == "completed"

        def is_failed(job: IngestJob) -> bool:
            return job.status == "failed"

        poll_job_sync(
            fetch_fn=fetch_job,
            is_done_fn=is_done,
            is_failed_fn=is_failed,
            timeout_seconds=timeout_seconds,
            initial_interval=poll_interval,
            on_progress=on_progress,
        )

        # After completed, fetch normalized listing
        data = self._http.get(f"/v1/listing/{mls_id}")
        return BaseListing.model_validate(data)

    def enqueue(
        self,
        mls_id: str,
        download_photos: bool = True,
        upload_to_r2: bool = True,
        save_local: bool = False,
        photos_concurrency: Optional[int] = None,
        webhook_url: Optional[str] = None,
    ) -> IngestJob:
        """Explicitly enqueue background MLS scraping and photo downloading."""
        payload: Dict[str, Any] = {
            "mlsId": mls_id,
            "downloadPhotos": download_photos,
            "uploadToR2": upload_to_r2,
            "saveLocal": save_local,
        }
        if photos_concurrency is not None:
            payload["photosConcurrency"] = photos_concurrency
        if webhook_url:
            payload["webhookUrl"] = webhook_url

        data = self._http.post("/jobs", json=payload)
        return IngestJob.model_validate(data)

    def get_job(self, job_id: str) -> IngestJob:
        """Get live ingestion progress and status."""
        data = self._http.get(f"/jobs/{job_id}")
        return IngestJob.model_validate(data)

    def list_jobs(self, limit: int = 20) -> List[IngestJob]:
        """List recent background ingestion jobs."""
        data = self._http.get("/jobs", params={"limit": limit})
        jobs = data.get("jobs", [])
        return [IngestJob.model_validate(j) for j in jobs]


class AsyncListingsResource:
    """Asynchronous MLS listings and ingestion operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(self, mls_id: str) -> Union[BaseListing, IngestJob]:
        """Lookup an MLS listing. If not cached, returns an IngestJob in progress."""
        data = await self._http.get(f"/v1/listing/{mls_id}")
        if "status" in data and data["status"] in ("processing", "queued"):
            return IngestJob.model_validate(data)
        return BaseListing.model_validate(data)

    async def get_and_wait(
        self,
        mls_id: str,
        timeout_seconds: float = 60.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[IngestJob], None]] = None,
    ) -> BaseListing:
        """Fetch listing and automatically poll until ingestion completes."""
        initial = await self.get(mls_id)
        if isinstance(initial, BaseListing):
            return initial

        job_id = initial.job_id or mls_id

        async def fetch_job() -> IngestJob:
            data = await self._http.get(f"/jobs/{job_id}")
            return IngestJob.model_validate(data)

        def is_done(job: IngestJob) -> bool:
            return job.status == "completed"

        def is_failed(job: IngestJob) -> bool:
            return job.status == "failed"

        await poll_job_async(
            fetch_fn=fetch_job,
            is_done_fn=is_done,
            is_failed_fn=is_failed,
            timeout_seconds=timeout_seconds,
            initial_interval=poll_interval,
            on_progress=on_progress,
        )

        data = await self._http.get(f"/v1/listing/{mls_id}")
        return BaseListing.model_validate(data)

    async def enqueue(
        self,
        mls_id: str,
        download_photos: bool = True,
        upload_to_r2: bool = True,
        save_local: bool = False,
        photos_concurrency: Optional[int] = None,
        webhook_url: Optional[str] = None,
    ) -> IngestJob:
        """Explicitly enqueue background MLS scraping and photo downloading."""
        payload: Dict[str, Any] = {
            "mlsId": mls_id,
            "downloadPhotos": download_photos,
            "uploadToR2": upload_to_r2,
            "saveLocal": save_local,
        }
        if photos_concurrency is not None:
            payload["photosConcurrency"] = photos_concurrency
        if webhook_url:
            payload["webhookUrl"] = webhook_url

        data = await self._http.post("/jobs", json=payload)
        return IngestJob.model_validate(data)

    async def get_job(self, job_id: str) -> IngestJob:
        """Get live ingestion progress and status."""
        data = await self._http.get(f"/jobs/{job_id}")
        return IngestJob.model_validate(data)

    async def list_jobs(self, limit: int = 20) -> List[IngestJob]:
        """List recent background ingestion jobs."""
        data = await self._http.get("/jobs", params={"limit": limit})
        jobs = data.get("jobs", [])
        return [IngestJob.model_validate(j) for j in jobs]
