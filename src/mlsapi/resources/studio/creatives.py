from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import AdCreativesResult, StudioJob
from mlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource


class CreativesResource:
    """Synchronous branded real estate multi-placement ad creative generation."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def generate(
        self,
        mls_id: str,
        trigger: str = "just_listed",
        direction: str = "magazine",
        placements: Optional[List[str]] = None,
        brand_kit: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "mls_id": mls_id,
            "trigger": trigger,
            "direction": direction,
            "placements": placements or ["feed_portrait", "square", "link", "flyer"],
        }
        if brand_kit:
            payload["brand_kit"] = brand_kit
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/creatives/generate", json=payload)
        return StudioJob.model_validate(data)

    def generate_and_wait(
        self,
        mls_id: str,
        trigger: str = "just_listed",
        direction: str = "magazine",
        placements: Optional[List[str]] = None,
        brand_kit: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> AdCreativesResult:
        job = self.generate(
            mls_id=mls_id,
            trigger=trigger,
            direction=direction,
            placements=placements,
            brand_kit=brand_kit,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return AdCreativesResult.model_validate(completed.result or {})


class AsyncCreativesResource:
    """Asynchronous branded real estate multi-placement ad creative generation."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def generate(
        self,
        mls_id: str,
        trigger: str = "just_listed",
        direction: str = "magazine",
        placements: Optional[List[str]] = None,
        brand_kit: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "mls_id": mls_id,
            "trigger": trigger,
            "direction": direction,
            "placements": placements or ["feed_portrait", "square", "link", "flyer"],
        }
        if brand_kit:
            payload["brand_kit"] = brand_kit
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/creatives/generate", json=payload)
        return StudioJob.model_validate(data)

    async def generate_and_wait(
        self,
        mls_id: str,
        trigger: str = "just_listed",
        direction: str = "magazine",
        placements: Optional[List[str]] = None,
        brand_kit: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> AdCreativesResult:
        job = await self.generate(
            mls_id=mls_id,
            trigger=trigger,
            direction=direction,
            placements=placements,
            brand_kit=brand_kit,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return AdCreativesResult.model_validate(completed.result or {})
