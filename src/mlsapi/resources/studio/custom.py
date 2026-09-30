from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import CustomStudioResult, StudioJob
from mlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource


class CustomResource:
    """Synchronous custom multimodal generative studio prompt."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def generate(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"prompt": prompt}
        if image_urls:
            payload["image_urls"] = image_urls
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/custom", json=payload)
        return StudioJob.model_validate(data)

    def generate_and_wait(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> CustomStudioResult:
        job = self.generate(
            prompt, image_urls=image_urls, negative_prompt=negative_prompt, webhook_url=webhook_url
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return CustomStudioResult.model_validate(completed.result or {})


class AsyncCustomResource:
    """Asynchronous custom multimodal generative studio prompt."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def generate(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"prompt": prompt}
        if image_urls:
            payload["image_urls"] = image_urls
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/custom", json=payload)
        return StudioJob.model_validate(data)

    async def generate_and_wait(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> CustomStudioResult:
        job = await self.generate(
            prompt, image_urls=image_urls, negative_prompt=negative_prompt, webhook_url=webhook_url
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return CustomStudioResult.model_validate(completed.result or {})
