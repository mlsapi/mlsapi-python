from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.requests import CreativeBrandKit, CreativesPropertyDetails, OpenHouse
from pymlsapi.models.studio import AdCreativesResult, StudioJob
from pymlsapi.resources._params import compact
from pymlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource

CREATIVES_PATH = "/v1/studio/creatives/generate"


def _creatives_body(**fields: Any) -> Dict[str, Any]:
    if not (fields.get("mls_id") or fields.get("photo_url") or fields.get("photos")):
        raise ValueError(
            "creatives.generate needs a listing photo: pass `photo_url`, `photos`, "
            "or an `mls_id` for an ingested listing."
        )
    return compact(**fields)


class CreativesResource:
    """Synchronous branded real estate multi-placement ad creative generation."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def generate(
        self,
        mls_id: Optional[str] = None,
        trigger: Optional[str] = None,
        direction: Optional[str] = None,
        placements: Optional[List[str]] = None,
        brand_kit: Optional[CreativeBrandKit] = None,
        webhook_url: Optional[str] = None,
        *,
        photo_url: Optional[str] = None,
        photos: Optional[List[str]] = None,
        property_details: Optional[CreativesPropertyDetails] = None,
        ad_type: Optional[str] = None,
        custom_badge: Optional[str] = None,
        custom_headline: Optional[str] = None,
        highlights: Optional[List[str]] = None,
        open_house: Optional[OpenHouse] = None,
        include_carousel: Optional[bool] = None,
        agent_headshot_url: Optional[str] = None,
        realtor_photo: Optional[str] = None,
    ) -> StudioJob:
        """Branded ad creatives for one or more placements. ``POST /v1/studio/creatives/generate``.

        At least one of ``mls_id``, ``photo_url`` or ``photos`` is required.
        """
        payload = _creatives_body(
            mls_id=mls_id,
            photos=photos,
            photo_url=photo_url,
            property_details=property_details,
            direction=direction,
            placements=placements,
            trigger=trigger,
            ad_type=ad_type,
            custom_badge=custom_badge,
            custom_headline=custom_headline,
            realtor_photo=realtor_photo,
            agent_headshot_url=agent_headshot_url,
            brand_kit=brand_kit,
            highlights=highlights,
            open_house=open_house,
            include_carousel=include_carousel,
            webhook_url=webhook_url,
        )
        data = self._http.post(CREATIVES_PATH, json=payload)
        return StudioJob.model_validate(data)

    def generate_and_wait(
        self,
        mls_id: Optional[str] = None,
        trigger: Optional[str] = None,
        direction: Optional[str] = None,
        placements: Optional[List[str]] = None,
        brand_kit: Optional[CreativeBrandKit] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        photo_url: Optional[str] = None,
        photos: Optional[List[str]] = None,
        property_details: Optional[CreativesPropertyDetails] = None,
        ad_type: Optional[str] = None,
        custom_badge: Optional[str] = None,
        custom_headline: Optional[str] = None,
        highlights: Optional[List[str]] = None,
        open_house: Optional[OpenHouse] = None,
        include_carousel: Optional[bool] = None,
        agent_headshot_url: Optional[str] = None,
        realtor_photo: Optional[str] = None,
    ) -> AdCreativesResult:
        job = self.generate(
            mls_id,
            trigger=trigger,
            direction=direction,
            placements=placements,
            brand_kit=brand_kit,
            webhook_url=webhook_url,
            photo_url=photo_url,
            photos=photos,
            property_details=property_details,
            ad_type=ad_type,
            custom_badge=custom_badge,
            custom_headline=custom_headline,
            highlights=highlights,
            open_house=open_house,
            include_carousel=include_carousel,
            agent_headshot_url=agent_headshot_url,
            realtor_photo=realtor_photo,
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
        mls_id: Optional[str] = None,
        trigger: Optional[str] = None,
        direction: Optional[str] = None,
        placements: Optional[List[str]] = None,
        brand_kit: Optional[CreativeBrandKit] = None,
        webhook_url: Optional[str] = None,
        *,
        photo_url: Optional[str] = None,
        photos: Optional[List[str]] = None,
        property_details: Optional[CreativesPropertyDetails] = None,
        ad_type: Optional[str] = None,
        custom_badge: Optional[str] = None,
        custom_headline: Optional[str] = None,
        highlights: Optional[List[str]] = None,
        open_house: Optional[OpenHouse] = None,
        include_carousel: Optional[bool] = None,
        agent_headshot_url: Optional[str] = None,
        realtor_photo: Optional[str] = None,
    ) -> StudioJob:
        """Branded ad creatives for one or more placements. ``POST /v1/studio/creatives/generate``.

        At least one of ``mls_id``, ``photo_url`` or ``photos`` is required.
        """
        payload = _creatives_body(
            mls_id=mls_id,
            photos=photos,
            photo_url=photo_url,
            property_details=property_details,
            direction=direction,
            placements=placements,
            trigger=trigger,
            ad_type=ad_type,
            custom_badge=custom_badge,
            custom_headline=custom_headline,
            realtor_photo=realtor_photo,
            agent_headshot_url=agent_headshot_url,
            brand_kit=brand_kit,
            highlights=highlights,
            open_house=open_house,
            include_carousel=include_carousel,
            webhook_url=webhook_url,
        )
        data = await self._http.post(CREATIVES_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def generate_and_wait(
        self,
        mls_id: Optional[str] = None,
        trigger: Optional[str] = None,
        direction: Optional[str] = None,
        placements: Optional[List[str]] = None,
        brand_kit: Optional[CreativeBrandKit] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        photo_url: Optional[str] = None,
        photos: Optional[List[str]] = None,
        property_details: Optional[CreativesPropertyDetails] = None,
        ad_type: Optional[str] = None,
        custom_badge: Optional[str] = None,
        custom_headline: Optional[str] = None,
        highlights: Optional[List[str]] = None,
        open_house: Optional[OpenHouse] = None,
        include_carousel: Optional[bool] = None,
        agent_headshot_url: Optional[str] = None,
        realtor_photo: Optional[str] = None,
    ) -> AdCreativesResult:
        job = await self.generate(
            mls_id,
            trigger=trigger,
            direction=direction,
            placements=placements,
            brand_kit=brand_kit,
            webhook_url=webhook_url,
            photo_url=photo_url,
            photos=photos,
            property_details=property_details,
            ad_type=ad_type,
            custom_badge=custom_badge,
            custom_headline=custom_headline,
            highlights=highlights,
            open_house=open_house,
            include_carousel=include_carousel,
            agent_headshot_url=agent_headshot_url,
            realtor_photo=realtor_photo,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return AdCreativesResult.model_validate(completed.result or {})
