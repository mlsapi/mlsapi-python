from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import ExteriorEnhanceResult, StudioJob, UpscaleResult
from mlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource


class EnhanceResource:
    """Synchronous exterior curb appeal and 4K upscaling operations."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def exterior(
        self,
        photo_url: str,
        enhancements: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if enhancements:
            payload["enhancements"] = enhancements
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/enhance/exterior", json=payload)
        return StudioJob.model_validate(data)

    def exterior_and_wait(
        self,
        photo_url: str,
        enhancements: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ExteriorEnhanceResult:
        job = self.exterior(photo_url, enhancements=enhancements, webhook_url=webhook_url)
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ExteriorEnhanceResult.model_validate(completed.result or {})

    def upscale(
        self,
        image_url: str,
        scale_factor: int = 4,
        enhance_details: bool = True,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "image_url": image_url,
            "scale_factor": scale_factor,
            "enhance_details": enhance_details,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/enhance/upscale", json=payload)
        return StudioJob.model_validate(data)

    def upscale_and_wait(
        self,
        image_url: str,
        scale_factor: int = 4,
        enhance_details: bool = True,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> UpscaleResult:
        job = self.upscale(
            image_url,
            scale_factor=scale_factor,
            enhance_details=enhance_details,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return UpscaleResult.model_validate(completed.result or {})


class AsyncEnhanceResource:
    """Asynchronous exterior curb appeal and 4K upscaling operations."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def exterior(
        self,
        photo_url: str,
        enhancements: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if enhancements:
            payload["enhancements"] = enhancements
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/enhance/exterior", json=payload)
        return StudioJob.model_validate(data)

    async def exterior_and_wait(
        self,
        photo_url: str,
        enhancements: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ExteriorEnhanceResult:
        job = await self.exterior(photo_url, enhancements=enhancements, webhook_url=webhook_url)
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ExteriorEnhanceResult.model_validate(completed.result or {})

    async def upscale(
        self,
        image_url: str,
        scale_factor: int = 4,
        enhance_details: bool = True,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "image_url": image_url,
            "scale_factor": scale_factor,
            "enhance_details": enhance_details,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/enhance/upscale", json=payload)
        return StudioJob.model_validate(data)

    async def upscale_and_wait(
        self,
        image_url: str,
        scale_factor: int = 4,
        enhance_details: bool = True,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> UpscaleResult:
        job = await self.upscale(
            image_url,
            scale_factor=scale_factor,
            enhance_details=enhance_details,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return UpscaleResult.model_validate(completed.result or {})
