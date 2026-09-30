from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import ArchitecturalRenderResult, StudioJob
from mlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource


class RenderResource:
    """Synchronous architectural visualization rendering (CAD / Sketch / SketchUp to photorealism)."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def architectural(
        self,
        source_image_url: str,
        style: Optional[str] = "modern",
        prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"source_image_url": source_image_url, "style": style}
        if prompt:
            payload["prompt"] = prompt
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/render/architectural", json=payload)
        return StudioJob.model_validate(data)

    def architectural_and_wait(
        self,
        source_image_url: str,
        style: Optional[str] = "modern",
        prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ArchitecturalRenderResult:
        job = self.architectural(
            source_image_url, style=style, prompt=prompt, webhook_url=webhook_url
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ArchitecturalRenderResult.model_validate(completed.result or {})


class AsyncRenderResource:
    """Asynchronous architectural visualization rendering."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def architectural(
        self,
        source_image_url: str,
        style: Optional[str] = "modern",
        prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"source_image_url": source_image_url, "style": style}
        if prompt:
            payload["prompt"] = prompt
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/render/architectural", json=payload)
        return StudioJob.model_validate(data)

    async def architectural_and_wait(
        self,
        source_image_url: str,
        style: Optional[str] = "modern",
        prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ArchitecturalRenderResult:
        job = await self.architectural(
            source_image_url, style=style, prompt=prompt, webhook_url=webhook_url
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ArchitecturalRenderResult.model_validate(completed.result or {})
