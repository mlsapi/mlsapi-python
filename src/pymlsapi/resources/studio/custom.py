from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.studio import CustomStudioResult, StudioJob
from pymlsapi.resources._params import compact, warn_deprecated
from pymlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource

CUSTOM_PATH = "/v1/studio/custom"


def _custom_body(
    prompt: str,
    reference_image_urls: Optional[List[str]],
    photo_url: Optional[str],
    aspect_ratio: Optional[str],
    webhook_url: Optional[str],
    image_urls: Optional[List[str]],
    negative_prompt: Optional[str],
) -> Dict[str, Any]:
    if image_urls is not None:
        warn_deprecated("image_urls", "reference_image_urls", stacklevel=4)
        if reference_image_urls is None:
            reference_image_urls = image_urls
    if negative_prompt is not None:
        warn_deprecated(
            "negative_prompt",
            note="Describe what to avoid in `prompt` instead.",
            stacklevel=4,
        )
    return compact(
        prompt=prompt,
        reference_image_urls=reference_image_urls,
        photo_url=photo_url,
        aspect_ratio=aspect_ratio,
        webhook_url=webhook_url,
    )


class CustomResource:
    """Synchronous custom multimodal generative studio prompt."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def generate(
        self,
        prompt: str,
        reference_image_urls: Optional[List[str]] = None,
        *,
        photo_url: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        webhook_url: Optional[str] = None,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
    ) -> StudioJob:
        """Free-form prompt with optional reference images. ``POST /v1/studio/custom``.

        ``image_urls`` is a deprecated alias for ``reference_image_urls``;
        ``negative_prompt`` is deprecated and ignored (the server never read it).
        """
        payload = _custom_body(
            prompt,
            reference_image_urls,
            photo_url,
            aspect_ratio,
            webhook_url,
            image_urls,
            negative_prompt,
        )
        data = self._http.post(CUSTOM_PATH, json=payload)
        return StudioJob.model_validate(data)

    def generate_and_wait(
        self,
        prompt: str,
        reference_image_urls: Optional[List[str]] = None,
        *,
        photo_url: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
    ) -> CustomStudioResult:
        job = self.generate(
            prompt,
            reference_image_urls=reference_image_urls,
            photo_url=photo_url,
            aspect_ratio=aspect_ratio,
            webhook_url=webhook_url,
            image_urls=image_urls,
            negative_prompt=negative_prompt,
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
        reference_image_urls: Optional[List[str]] = None,
        *,
        photo_url: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        webhook_url: Optional[str] = None,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
    ) -> StudioJob:
        """Free-form prompt with optional reference images. ``POST /v1/studio/custom``.

        ``image_urls`` is a deprecated alias for ``reference_image_urls``;
        ``negative_prompt`` is deprecated and ignored (the server never read it).
        """
        payload = _custom_body(
            prompt,
            reference_image_urls,
            photo_url,
            aspect_ratio,
            webhook_url,
            image_urls,
            negative_prompt,
        )
        data = await self._http.post(CUSTOM_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def generate_and_wait(
        self,
        prompt: str,
        reference_image_urls: Optional[List[str]] = None,
        *,
        photo_url: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        image_urls: Optional[List[str]] = None,
        negative_prompt: Optional[str] = None,
    ) -> CustomStudioResult:
        job = await self.generate(
            prompt,
            reference_image_urls=reference_image_urls,
            photo_url=photo_url,
            aspect_ratio=aspect_ratio,
            webhook_url=webhook_url,
            image_urls=image_urls,
            negative_prompt=negative_prompt,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return CustomStudioResult.model_validate(completed.result or {})
