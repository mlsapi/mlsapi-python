from __future__ import annotations

from typing import Callable, Optional

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.studio import ArchitecturalRenderResult, StudioJob
from pymlsapi.resources._params import compact, resolve_alias
from pymlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource

ARCHITECTURAL_PATH = "/v1/studio/render/architectural"


class RenderResource:
    """Synchronous architectural visualization rendering (CAD / Sketch / SketchUp to photorealism)."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def architectural(
        self,
        source_image_url: str,
        style: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        render_type: Optional[str] = None,
        lighting_environment: Optional[str] = None,
        weather: Optional[str] = None,
        season: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> StudioJob:
        """Turn a CAD/sketch/3D viewport into a photoreal render. ``POST /v1/studio/render/architectural``.

        ``prompt`` is a deprecated alias for ``custom_instructions``.
        """
        custom_instructions = resolve_alias(
            "custom_instructions", custom_instructions, "prompt", prompt
        )
        payload = compact(
            source_image_url=source_image_url,
            render_type=render_type,
            style=style,
            lighting_environment=lighting_environment,
            weather=weather,
            season=season,
            custom_instructions=custom_instructions,
            webhook_url=webhook_url,
        )
        data = self._http.post(ARCHITECTURAL_PATH, json=payload)
        return StudioJob.model_validate(data)

    def architectural_and_wait(
        self,
        source_image_url: str,
        style: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        render_type: Optional[str] = None,
        lighting_environment: Optional[str] = None,
        weather: Optional[str] = None,
        season: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> ArchitecturalRenderResult:
        job = self.architectural(
            source_image_url,
            style=style,
            custom_instructions=custom_instructions,
            webhook_url=webhook_url,
            render_type=render_type,
            lighting_environment=lighting_environment,
            weather=weather,
            season=season,
            prompt=prompt,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ArchitecturalRenderResult.model_validate(completed.result or {})


class AsyncRenderResource:
    """Asynchronous architectural visualization rendering (CAD / Sketch / SketchUp to photorealism)."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def architectural(
        self,
        source_image_url: str,
        style: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        render_type: Optional[str] = None,
        lighting_environment: Optional[str] = None,
        weather: Optional[str] = None,
        season: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> StudioJob:
        """Turn a CAD/sketch/3D viewport into a photoreal render. ``POST /v1/studio/render/architectural``.

        ``prompt`` is a deprecated alias for ``custom_instructions``.
        """
        custom_instructions = resolve_alias(
            "custom_instructions", custom_instructions, "prompt", prompt
        )
        payload = compact(
            source_image_url=source_image_url,
            render_type=render_type,
            style=style,
            lighting_environment=lighting_environment,
            weather=weather,
            season=season,
            custom_instructions=custom_instructions,
            webhook_url=webhook_url,
        )
        data = await self._http.post(ARCHITECTURAL_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def architectural_and_wait(
        self,
        source_image_url: str,
        style: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        render_type: Optional[str] = None,
        lighting_environment: Optional[str] = None,
        weather: Optional[str] = None,
        season: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> ArchitecturalRenderResult:
        job = await self.architectural(
            source_image_url,
            style=style,
            custom_instructions=custom_instructions,
            webhook_url=webhook_url,
            render_type=render_type,
            lighting_environment=lighting_environment,
            weather=weather,
            season=season,
            prompt=prompt,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ArchitecturalRenderResult.model_validate(completed.result or {})
