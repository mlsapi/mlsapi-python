from __future__ import annotations

from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Union

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.requests import HouseTourRoomItem, SubtitleStyle, VideoEnhanceFeatures
from pymlsapi.models.studio import (
    HouseTourResult,
    StudioJob,
    VideoEnhanceResult,
    VideoTransitionResult,
    VideoWalkthroughResult,
)
from pymlsapi.resources._params import compact, warn_deprecated
from pymlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource

ENHANCE_PATH = "/v1/studio/video/enhance"
WALKTHROUGH_PATH = "/v1/studio/video/walkthrough"
TRANSITION_PATH = "/v1/studio/video/transition"
TOUR_PATH = "/v1/studio/video/tour"


def _walkthrough_body(
    photo_url: Any,
    mls_id: Optional[str],
    webhook_url: Optional[str],
    motion: Optional[str],
    duration_seconds: Optional[int],
    custom_motion_prompt: Optional[str],
    aspect_ratio: Optional[str],
    photo_urls: Optional[List[str]],
    voice_id: Optional[str],
    music_mood: Optional[str],
    photos: Optional[List[str]],
) -> Dict[str, Any]:
    if isinstance(photo_url, (list, tuple)):
        # 0.1.0 took a list of photos as the first positional argument.
        warn_deprecated("passing a list as the first argument", "photo_urls=[...]", stacklevel=4)
        if photo_urls is None:
            photo_urls = list(photo_url)
        photo_url = None
    if photos is not None:
        warn_deprecated("photos", "photo_urls", stacklevel=4)
        if photo_urls is None:
            photo_urls = photos
    return compact(
        photo_url=photo_url,
        motion=motion,
        duration_seconds=duration_seconds,
        custom_motion_prompt=custom_motion_prompt,
        aspect_ratio=aspect_ratio,
        mls_id=mls_id,
        photo_urls=photo_urls,
        voice_id=voice_id,
        music_mood=music_mood,
        webhook_url=webhook_url,
    )


def _tour_body(
    ordered_photos: Sequence[Union[HouseTourRoomItem, Mapping[str, Any], str]],
    duration_seconds: Optional[int],
    auto_script: Optional[bool],
    shot_script: Optional[str],
    aspect_ratio: Optional[str],
    music_genre: Optional[str],
    webhook_url: Optional[str],
    music_mood: Optional[str],
) -> Dict[str, Any]:
    photos: List[Dict[str, Any]] = []
    warned_strings = False
    for idx, item in enumerate(ordered_photos):
        if isinstance(item, str):
            if not warned_strings:
                warn_deprecated(
                    "ordered_photos as a list of URLs",
                    "a list of {'room_name': ..., 'photo_url': ...} dicts",
                    stacklevel=4,
                )
                warned_strings = True
            photos.append({"room_name": f"Room {idx + 1}", "photo_url": item})
        else:
            photos.append(dict(item))
    if music_mood is not None:
        warn_deprecated("music_mood", "music_genre", stacklevel=4)
    return compact(
        ordered_photos=photos,
        duration_seconds=duration_seconds,
        auto_script=auto_script,
        shot_script=shot_script,
        aspect_ratio=aspect_ratio,
        music_genre=music_genre,
        webhook_url=webhook_url,
    )


class VideoResource:
    """Synchronous video walkthrough, speech mastering, and tour automation."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    # -- Enhance -------------------------------------------------------------

    def enhance(
        self,
        video_url: str,
        features: Optional[VideoEnhanceFeatures] = None,
        subtitle_style: Optional[SubtitleStyle] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        *,
        mls_id: Optional[str] = None,
    ) -> StudioJob:
        """Studio voice, animated subtitles, smart reframe. ``POST /v1/studio/video/enhance``."""
        payload = compact(
            video_url=video_url,
            features=features,
            subtitle_style=subtitle_style,
            export_aspect_ratios=export_aspect_ratios,
            mls_id=mls_id,
            webhook_url=webhook_url,
        )
        data = self._http.post(ENHANCE_PATH, json=payload)
        return StudioJob.model_validate(data)

    def enhance_and_wait(
        self,
        video_url: str,
        features: Optional[VideoEnhanceFeatures] = None,
        subtitle_style: Optional[SubtitleStyle] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        mls_id: Optional[str] = None,
    ) -> VideoEnhanceResult:
        job = self.enhance(
            video_url,
            features=features,
            subtitle_style=subtitle_style,
            export_aspect_ratios=export_aspect_ratios,
            webhook_url=webhook_url,
            mls_id=mls_id,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoEnhanceResult.model_validate(completed.result or {})

    # -- Walkthrough ---------------------------------------------------------

    def walkthrough(
        self,
        photo_url: Optional[str] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        motion: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        custom_motion_prompt: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        photo_urls: Optional[List[str]] = None,
        voice_id: Optional[str] = None,
        music_mood: Optional[str] = None,
        photos: Optional[List[str]] = None,
    ) -> StudioJob:
        """Animate a listing photo into a short camera-motion clip. ``POST /v1/studio/video/walkthrough``.

        Spec fields: ``photo_url``, ``motion`` (``orbit_left``, ``orbit_right``, ``pan_left``,
        ``pan_right``, ``slow_zoom_in``, ``dolly_out``, ``shifting_daylight``,
        ``add_subtle_people``), ``duration_seconds`` (5 or 10), ``custom_motion_prompt``,
        ``aspect_ratio``. ``mls_id``, ``photo_urls``, ``voice_id`` and ``music_mood`` mirror the
        JS SDK. ``photos`` is a deprecated alias for ``photo_urls``.
        """
        payload = _walkthrough_body(
            photo_url,
            mls_id,
            webhook_url,
            motion,
            duration_seconds,
            custom_motion_prompt,
            aspect_ratio,
            photo_urls,
            voice_id,
            music_mood,
            photos,
        )
        data = self._http.post(WALKTHROUGH_PATH, json=payload)
        return StudioJob.model_validate(data)

    def walkthrough_and_wait(
        self,
        photo_url: Optional[str] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        motion: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        custom_motion_prompt: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        photo_urls: Optional[List[str]] = None,
        voice_id: Optional[str] = None,
        music_mood: Optional[str] = None,
        photos: Optional[List[str]] = None,
    ) -> VideoWalkthroughResult:
        job = self.walkthrough(
            photo_url,
            mls_id=mls_id,
            webhook_url=webhook_url,
            motion=motion,
            duration_seconds=duration_seconds,
            custom_motion_prompt=custom_motion_prompt,
            aspect_ratio=aspect_ratio,
            photo_urls=photo_urls,
            voice_id=voice_id,
            music_mood=music_mood,
            photos=photos,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoWalkthroughResult.model_validate(completed.result or {})

    # -- Transition ----------------------------------------------------------

    def transition(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: Optional[int] = None,
        webhook_url: Optional[str] = None,
        *,
        transition_style: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
    ) -> StudioJob:
        """Before/after morph video. ``POST /v1/studio/video/transition``.

        ``duration_seconds`` must be 5 or 10 (server default 5).
        """
        payload = compact(
            start_image_url=start_image_url,
            end_image_url=end_image_url,
            duration_seconds=duration_seconds,
            transition_style=transition_style,
            aspect_ratio=aspect_ratio,
            webhook_url=webhook_url,
        )
        data = self._http.post(TRANSITION_PATH, json=payload)
        return StudioJob.model_validate(data)

    def transition_and_wait(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: Optional[int] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        transition_style: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
    ) -> VideoTransitionResult:
        job = self.transition(
            start_image_url,
            end_image_url,
            duration_seconds=duration_seconds,
            webhook_url=webhook_url,
            transition_style=transition_style,
            aspect_ratio=aspect_ratio,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoTransitionResult.model_validate(completed.result or {})

    # -- House tour ----------------------------------------------------------

    def tour(
        self,
        ordered_photos: Sequence[Union[HouseTourRoomItem, Mapping[str, Any], str]],
        *,
        duration_seconds: Optional[int] = None,
        auto_script: Optional[bool] = None,
        shot_script: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        music_genre: Optional[str] = None,
        webhook_url: Optional[str] = None,
        music_mood: Optional[str] = None,
    ) -> StudioJob:
        """Multi-room house tour reel. ``POST /v1/studio/video/tour``.

        ``ordered_photos`` is a list of ``{"room_name", "photo_url", "highlight"?}`` dicts.
        Plain URL strings and ``music_mood`` are deprecated.
        """
        payload = _tour_body(
            ordered_photos,
            duration_seconds,
            auto_script,
            shot_script,
            aspect_ratio,
            music_genre,
            webhook_url,
            music_mood,
        )
        data = self._http.post(TOUR_PATH, json=payload)
        return StudioJob.model_validate(data)

    def tour_and_wait(
        self,
        ordered_photos: Sequence[Union[HouseTourRoomItem, Mapping[str, Any], str]],
        *,
        duration_seconds: Optional[int] = None,
        auto_script: Optional[bool] = None,
        shot_script: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        music_genre: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        music_mood: Optional[str] = None,
    ) -> HouseTourResult:
        job = self.tour(
            ordered_photos,
            duration_seconds=duration_seconds,
            auto_script=auto_script,
            shot_script=shot_script,
            aspect_ratio=aspect_ratio,
            music_genre=music_genre,
            webhook_url=webhook_url,
            music_mood=music_mood,
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

    # -- Enhance -------------------------------------------------------------

    async def enhance(
        self,
        video_url: str,
        features: Optional[VideoEnhanceFeatures] = None,
        subtitle_style: Optional[SubtitleStyle] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        *,
        mls_id: Optional[str] = None,
    ) -> StudioJob:
        """Studio voice, animated subtitles, smart reframe. ``POST /v1/studio/video/enhance``."""
        payload = compact(
            video_url=video_url,
            features=features,
            subtitle_style=subtitle_style,
            export_aspect_ratios=export_aspect_ratios,
            mls_id=mls_id,
            webhook_url=webhook_url,
        )
        data = await self._http.post(ENHANCE_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def enhance_and_wait(
        self,
        video_url: str,
        features: Optional[VideoEnhanceFeatures] = None,
        subtitle_style: Optional[SubtitleStyle] = None,
        export_aspect_ratios: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        mls_id: Optional[str] = None,
    ) -> VideoEnhanceResult:
        job = await self.enhance(
            video_url,
            features=features,
            subtitle_style=subtitle_style,
            export_aspect_ratios=export_aspect_ratios,
            webhook_url=webhook_url,
            mls_id=mls_id,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoEnhanceResult.model_validate(completed.result or {})

    # -- Walkthrough ---------------------------------------------------------

    async def walkthrough(
        self,
        photo_url: Optional[str] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        motion: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        custom_motion_prompt: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        photo_urls: Optional[List[str]] = None,
        voice_id: Optional[str] = None,
        music_mood: Optional[str] = None,
        photos: Optional[List[str]] = None,
    ) -> StudioJob:
        """Animate a listing photo into a short camera-motion clip. ``POST /v1/studio/video/walkthrough``.

        Spec fields: ``photo_url``, ``motion`` (``orbit_left``, ``orbit_right``, ``pan_left``,
        ``pan_right``, ``slow_zoom_in``, ``dolly_out``, ``shifting_daylight``,
        ``add_subtle_people``), ``duration_seconds`` (5 or 10), ``custom_motion_prompt``,
        ``aspect_ratio``. ``mls_id``, ``photo_urls``, ``voice_id`` and ``music_mood`` mirror the
        JS SDK. ``photos`` is a deprecated alias for ``photo_urls``.
        """
        payload = _walkthrough_body(
            photo_url,
            mls_id,
            webhook_url,
            motion,
            duration_seconds,
            custom_motion_prompt,
            aspect_ratio,
            photo_urls,
            voice_id,
            music_mood,
            photos,
        )
        data = await self._http.post(WALKTHROUGH_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def walkthrough_and_wait(
        self,
        photo_url: Optional[str] = None,
        mls_id: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        motion: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        custom_motion_prompt: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        photo_urls: Optional[List[str]] = None,
        voice_id: Optional[str] = None,
        music_mood: Optional[str] = None,
        photos: Optional[List[str]] = None,
    ) -> VideoWalkthroughResult:
        job = await self.walkthrough(
            photo_url,
            mls_id=mls_id,
            webhook_url=webhook_url,
            motion=motion,
            duration_seconds=duration_seconds,
            custom_motion_prompt=custom_motion_prompt,
            aspect_ratio=aspect_ratio,
            photo_urls=photo_urls,
            voice_id=voice_id,
            music_mood=music_mood,
            photos=photos,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoWalkthroughResult.model_validate(completed.result or {})

    # -- Transition ----------------------------------------------------------

    async def transition(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: Optional[int] = None,
        webhook_url: Optional[str] = None,
        *,
        transition_style: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
    ) -> StudioJob:
        """Before/after morph video. ``POST /v1/studio/video/transition``.

        ``duration_seconds`` must be 5 or 10 (server default 5).
        """
        payload = compact(
            start_image_url=start_image_url,
            end_image_url=end_image_url,
            duration_seconds=duration_seconds,
            transition_style=transition_style,
            aspect_ratio=aspect_ratio,
            webhook_url=webhook_url,
        )
        data = await self._http.post(TRANSITION_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def transition_and_wait(
        self,
        start_image_url: str,
        end_image_url: str,
        duration_seconds: Optional[int] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        transition_style: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
    ) -> VideoTransitionResult:
        job = await self.transition(
            start_image_url,
            end_image_url,
            duration_seconds=duration_seconds,
            webhook_url=webhook_url,
            transition_style=transition_style,
            aspect_ratio=aspect_ratio,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return VideoTransitionResult.model_validate(completed.result or {})

    # -- House tour ----------------------------------------------------------

    async def tour(
        self,
        ordered_photos: Sequence[Union[HouseTourRoomItem, Mapping[str, Any], str]],
        *,
        duration_seconds: Optional[int] = None,
        auto_script: Optional[bool] = None,
        shot_script: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        music_genre: Optional[str] = None,
        webhook_url: Optional[str] = None,
        music_mood: Optional[str] = None,
    ) -> StudioJob:
        """Multi-room house tour reel. ``POST /v1/studio/video/tour``.

        ``ordered_photos`` is a list of ``{"room_name", "photo_url", "highlight"?}`` dicts.
        Plain URL strings and ``music_mood`` are deprecated.
        """
        payload = _tour_body(
            ordered_photos,
            duration_seconds,
            auto_script,
            shot_script,
            aspect_ratio,
            music_genre,
            webhook_url,
            music_mood,
        )
        data = await self._http.post(TOUR_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def tour_and_wait(
        self,
        ordered_photos: Sequence[Union[HouseTourRoomItem, Mapping[str, Any], str]],
        *,
        duration_seconds: Optional[int] = None,
        auto_script: Optional[bool] = None,
        shot_script: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        music_genre: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 120.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        music_mood: Optional[str] = None,
    ) -> HouseTourResult:
        job = await self.tour(
            ordered_photos,
            duration_seconds=duration_seconds,
            auto_script=auto_script,
            shot_script=shot_script,
            aspect_ratio=aspect_ratio,
            music_genre=music_genre,
            webhook_url=webhook_url,
            music_mood=music_mood,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return HouseTourResult.model_validate(completed.result or {})
