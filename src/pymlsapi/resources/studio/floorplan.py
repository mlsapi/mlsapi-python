from __future__ import annotations

from typing import Callable, List, Optional

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.studio import FloorPlanAnalysisResponse, Render3dResult, StudioJob
from pymlsapi.resources._params import compact
from pymlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource

ANALYZE_PATH = "/v1/studio/floorplan/analyze"
RENDER_3D_PATH = "/v1/studio/floorplan/render-3d"


class FloorPlanResource:
    """Synchronous 2D floor plan blueprint analysis and 3D isometric dollhouse rendering."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def analyze(
        self,
        floorplan_image_url: str,
        style: Optional[str] = None,
        mls_id: Optional[str] = None,
        generate_3d_render: Optional[bool] = None,
    ) -> FloorPlanAnalysisResponse:
        """Analyze 2D floorplan geometry, detect rooms, and generate design prompts."""
        payload = compact(
            floorplan_image_url=floorplan_image_url,
            style=style,
            mls_id=mls_id,
            generate_3d_render=generate_3d_render,
        )
        data = self._http.post(ANALYZE_PATH, json=payload)
        return FloorPlanAnalysisResponse.model_validate(data)

    def render_3d(
        self,
        floorplan_image_url: str,
        style: Optional[str] = None,
        include_room_closeups: Optional[bool] = None,
        target_rooms: Optional[List[str]] = None,
        custom_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        """Trigger asynchronous 3D isometric dollhouse cutaway model rendering."""
        payload = compact(
            floorplan_image_url=floorplan_image_url,
            style=style,
            include_room_closeups=include_room_closeups,
            target_rooms=target_rooms,
            custom_prompt=custom_prompt,
            webhook_url=webhook_url,
        )
        data = self._http.post(RENDER_3D_PATH, json=payload)
        return StudioJob.model_validate(data)

    def render_3d_and_wait(
        self,
        floorplan_image_url: str,
        style: Optional[str] = None,
        include_room_closeups: Optional[bool] = None,
        target_rooms: Optional[List[str]] = None,
        custom_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> Render3dResult:
        """Render 3D isometric dollhouse and auto-poll until complete."""
        job = self.render_3d(
            floorplan_image_url,
            style=style,
            include_room_closeups=include_room_closeups,
            target_rooms=target_rooms,
            custom_prompt=custom_prompt,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return Render3dResult.model_validate(completed.result or {})


class AsyncFloorPlanResource:
    """Asynchronous 2D floor plan blueprint analysis and 3D isometric dollhouse rendering."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def analyze(
        self,
        floorplan_image_url: str,
        style: Optional[str] = None,
        mls_id: Optional[str] = None,
        generate_3d_render: Optional[bool] = None,
    ) -> FloorPlanAnalysisResponse:
        """Analyze 2D floorplan geometry, detect rooms, and generate design prompts."""
        payload = compact(
            floorplan_image_url=floorplan_image_url,
            style=style,
            mls_id=mls_id,
            generate_3d_render=generate_3d_render,
        )
        data = await self._http.post(ANALYZE_PATH, json=payload)
        return FloorPlanAnalysisResponse.model_validate(data)

    async def render_3d(
        self,
        floorplan_image_url: str,
        style: Optional[str] = None,
        include_room_closeups: Optional[bool] = None,
        target_rooms: Optional[List[str]] = None,
        custom_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        """Trigger asynchronous 3D isometric dollhouse cutaway model rendering."""
        payload = compact(
            floorplan_image_url=floorplan_image_url,
            style=style,
            include_room_closeups=include_room_closeups,
            target_rooms=target_rooms,
            custom_prompt=custom_prompt,
            webhook_url=webhook_url,
        )
        data = await self._http.post(RENDER_3D_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def render_3d_and_wait(
        self,
        floorplan_image_url: str,
        style: Optional[str] = None,
        include_room_closeups: Optional[bool] = None,
        target_rooms: Optional[List[str]] = None,
        custom_prompt: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> Render3dResult:
        """Render 3D isometric dollhouse and auto-poll until complete."""
        job = await self.render_3d(
            floorplan_image_url,
            style=style,
            include_room_closeups=include_room_closeups,
            target_rooms=target_rooms,
            custom_prompt=custom_prompt,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return Render3dResult.model_validate(completed.result or {})
