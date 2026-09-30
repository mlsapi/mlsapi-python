from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import (
    HouseTourResult,
    StudioJob,
    VideoEnhanceResult,
    VideoTransitionResult,
    VideoWalkthroughResult,
)
from mlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource


class VideoResource:
    """Synchronous video walkthrough, speech mastering, and tour automation."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def enhance(
        self,
        video_url: str,
        features: Optional[Dict[str, bool]] = None,
        subtitle_style: Optional[Dict[str, Any]] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "video_url": video_url,
            "features": features
            or {"studio_voice": True, "animated_subtitles": True, "smart_reframe": True},
        }
        if subtitle_style:
            payload["subtitle_style"] = subtitle_style
        if export_aspect_ratios:
            payload["export_aspect_ratios"] = export_aspect_ratios
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/video/enhance", json=payload)
        return StudioJob.model_validate(data)

    def enhance_and_wait(
        self,
        video_url: str,
        features: Optional[Dict[str, bool]] = None,
        subtitle_style: Optional[Dict[str, Any]] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> VideoEnhanceResult:
        job = self.enhance(
            video_url,
            features=features,
            subtitle_style=subtitle_style,
            export_aspect_ratios=export_aspect_ratios,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoEnhanceResult.model_validate(completed.result or {})

    def walkthrough(
        self,
        photos: Optional[List[str]] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {}
        if photos:
            payload["photos"] = photos
        if mls_id:
            payload["mls_id"] = mls_id
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/video/walkthrough", json=payload)
        return StudioJob.model_validate(data)

    def walkthrough_and_wait(
        self,
        photos: Optional[List[str]] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> VideoWalkthroughResult:
        job = self.walkthrough(photos=photos, mls_id=mls_id, webhook_url=webhook_url)
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoWalkthroughResult.model_validate(completed.result or {})

    def transition(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: float = 3.0,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "start_image_url": start_image_url,
            "end_image_url": end_image_url,
            "duration_seconds": duration_seconds,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/video/transition", json=payload)
        return StudioJob.model_validate(data)

    def transition_and_wait(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: float = 3.0,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> VideoTransitionResult:
        job = self.transition(
            start_image_url,
            end_image_url,
            duration_seconds=duration_seconds,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoTransitionResult.model_validate(completed.result or {})

    def tour(
        self,
        ordered_photos: List[str],
        music_mood: Optional[str] = "luxurious",
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "ordered_photos": ordered_photos,
            "music_mood": music_mood,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/video/tour", json=payload)
        return StudioJob.model_validate(data)

    def tour_and_wait(
        self,
        ordered_photos: List[str],
        music_mood: Optional[str] = "luxurious",
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> HouseTourResult:
        job = self.tour(
            ordered_photos=ordered_photos, music_mood=music_mood, webhook_url=webhook_url
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return HouseTourResult.model_validate(completed.result or {})


class AsyncVideoResource:
    """Asynchronous video walkthrough, speech mastering, and tour automation."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def enhance(
        self,
        video_url: str,
        features: Optional[Dict[str, bool]] = None,
        subtitle_style: Optional[Dict[str, Any]] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "video_url": video_url,
            "features": features
            or {"studio_voice": True, "animated_subtitles": True, "smart_reframe": True},
        }
        if subtitle_style:
            payload["subtitle_style"] = subtitle_style
        if export_aspect_ratios:
            payload["export_aspect_ratios"] = export_aspect_ratios
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/video/enhance", json=payload)
        return StudioJob.model_validate(data)

    async def enhance_and_wait(
        self,
        video_url: str,
        features: Optional[Dict[str, bool]] = None,
        subtitle_style: Optional[Dict[str, Any]] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> VideoEnhanceResult:
        job = await self.enhance(
            video_url,
            features=features,
            subtitle_style=subtitle_style,
            export_aspect_ratios=export_aspect_ratios,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoEnhanceResult.model_validate(completed.result or {})

    async def walkthrough(
        self,
        photos: Optional[List[str]] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {}
        if photos:
            payload["photos"] = photos
        if mls_id:
            payload["mls_id"] = mls_id
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/video/walkthrough", json=payload)
        return StudioJob.model_validate(data)

    async def walkthrough_and_wait(
        self,
        photos: Optional[List[str]] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> VideoWalkthroughResult:
        job = await self.walkthrough(photos=photos, mls_id=mls_id, webhook_url=webhook_url)
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoWalkthroughResult.model_validate(completed.result or {})

    async def transition(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: float = 3.0,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "start_image_url": start_image_url,
            "end_image_url": end_image_url,
            "duration_seconds": duration_seconds,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/video/transition", json=payload)
        return StudioJob.model_validate(data)

    async def transition_and_wait(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: float = 3.0,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> VideoTransitionResult:
        job = await self.transition(
            start_image_url,
            end_image_url,
            duration_seconds=duration_seconds,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoTransitionResult.model_validate(completed.result or {})

    async def tour(
        self,
        ordered_photos: List[str],
        music_mood: Optional[str] = "luxurious",
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "ordered_photos": ordered_photos,
            "music_mood": music_mood,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/video/tour", json=payload)
        return StudioJob.model_validate(data)

    async def tour_and_wait(
        self,
        ordered_photos: List[str],
        music_mood: Optional[str] = "luxurious",
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> HouseTourResult:
        job = await self.tour(
            ordered_photos=ordered_photos, music_mood=music_mood, webhook_url=webhook_url
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return HouseTourResult.model_validate(completed.result or {})
