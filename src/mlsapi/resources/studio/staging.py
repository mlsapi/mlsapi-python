from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import (
    DeclutterResult,
    DeStageEmptyResult,
    ReplaceFurnitureResult,
    ReplaceMaterialResult,
    RestyleResult,
    StagingResult,
    StudioJob,
    TwilightResult,
    WallColorsResult,
)
from mlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource


class StagingResource:
    """Synchronous Virtual Staging and Room Transformation operations."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    def stage(
        self,
        photo_url: str,
        room_type: Optional[str] = "living_room",
        style: Optional[str] = "modern",
        preserve_flooring: bool = True,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "photo_url": photo_url,
            "room_type": room_type,
            "style": style,
            "preserve_flooring": preserve_flooring,
        }
        if custom_staging_instructions:
            payload["custom_staging_instructions"] = custom_staging_instructions
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/furnish", json=payload)
        return StudioJob.model_validate(data)

    def stage_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = "living_room",
        style: Optional[str] = "modern",
        preserve_flooring: bool = True,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> StagingResult:
        job = self.stage(
            photo_url=photo_url,
            room_type=room_type,
            style=style,
            preserve_flooring=preserve_flooring,
            custom_staging_instructions=custom_staging_instructions,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return StagingResult.model_validate(completed.result or {})

    def declutter(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        removal_targets: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if room_type:
            payload["room_type"] = room_type
        if removal_targets:
            payload["removal_targets"] = removal_targets
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/declutter", json=payload)
        return StudioJob.model_validate(data)

    def declutter_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        removal_targets: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> DeclutterResult:
        job = self.declutter(
            photo_url, room_type=room_type, removal_targets=removal_targets, webhook_url=webhook_url
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return DeclutterResult.model_validate(completed.result or {})

    def empty(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        restore_flooring: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if room_type:
            payload["room_type"] = room_type
        if restore_flooring:
            payload["restore_flooring"] = restore_flooring
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/empty", json=payload)
        return StudioJob.model_validate(data)

    def empty_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        restore_flooring: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> DeStageEmptyResult:
        job = self.empty(
            photo_url,
            room_type=room_type,
            restore_flooring=restore_flooring,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return DeStageEmptyResult.model_validate(completed.result or {})

    def restyle(
        self,
        photo_url: str,
        target_style: str = "scandinavian",
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url, "target_style": target_style}
        if room_type:
            payload["room_type"] = room_type
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/restyle", json=payload)
        return StudioJob.model_validate(data)

    def restyle_and_wait(
        self,
        photo_url: str,
        target_style: str = "scandinavian",
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> RestyleResult:
        job = self.restyle(
            photo_url, target_style=target_style, room_type=room_type, webhook_url=webhook_url
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return RestyleResult.model_validate(completed.result or {})

    def replace_furniture(
        self,
        room_photo_url: str,
        target_furniture: str,
        product_description: Optional[str] = None,
        reference_product_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "room_photo_url": room_photo_url,
            "target_furniture": target_furniture,
        }
        if product_description:
            payload["product_description"] = product_description
        if reference_product_image_url:
            payload["reference_product_image_url"] = reference_product_image_url
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/replace-furniture", json=payload)
        return StudioJob.model_validate(data)

    def replace_furniture_and_wait(
        self,
        room_photo_url: str,
        target_furniture: str,
        product_description: Optional[str] = None,
        reference_product_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ReplaceFurnitureResult:
        job = self.replace_furniture(
            room_photo_url,
            target_furniture,
            product_description=product_description,
            reference_product_image_url=reference_product_image_url,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceFurnitureResult.model_validate(completed.result or {})

    def replace_material(
        self,
        room_photo_url: str,
        surface_type: str,
        material_preset: Optional[str] = None,
        material_sample_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "room_photo_url": room_photo_url,
            "surface_type": surface_type,
        }
        if material_preset:
            payload["material_preset"] = material_preset
        if material_sample_image_url:
            payload["material_sample_image_url"] = material_sample_image_url
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/replace-material", json=payload)
        return StudioJob.model_validate(data)

    def replace_material_and_wait(
        self,
        room_photo_url: str,
        surface_type: str,
        material_preset: Optional[str] = None,
        material_sample_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ReplaceMaterialResult:
        job = self.replace_material(
            room_photo_url,
            surface_type,
            material_preset=material_preset,
            material_sample_image_url=material_sample_image_url,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceMaterialResult.model_validate(completed.result or {})

    def wall_colors(
        self,
        photo_url: str,
        palette_preset: Optional[str] = "popular_neutrals",
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if palette_preset:
            payload["palette_preset"] = palette_preset
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/wall-colors", json=payload)
        return StudioJob.model_validate(data)

    def wall_colors_and_wait(
        self,
        photo_url: str,
        palette_preset: Optional[str] = "popular_neutrals",
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> WallColorsResult:
        job = self.wall_colors(photo_url, palette_preset=palette_preset, webhook_url=webhook_url)
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return WallColorsResult.model_validate(completed.result or {})

    def twilight(
        self,
        photo_url: str,
        mode: str = "day_to_dusk",
        interior_lighting: bool = True,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "photo_url": photo_url,
            "mode": mode,
            "interior_lighting": interior_lighting,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = self._http.post("/v1/studio/staging/twilight", json=payload)
        return StudioJob.model_validate(data)

    def twilight_and_wait(
        self,
        photo_url: str,
        mode: str = "day_to_dusk",
        interior_lighting: bool = True,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> TwilightResult:
        job = self.twilight(
            photo_url, mode=mode, interior_lighting=interior_lighting, webhook_url=webhook_url
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return TwilightResult.model_validate(completed.result or {})


class AsyncStagingResource:
    """Asynchronous Virtual Staging and Room Transformation operations."""

    def __init__(self, http: AsyncHttpClient, jobs: AsyncStudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    async def stage(
        self,
        photo_url: str,
        room_type: Optional[str] = "living_room",
        style: Optional[str] = "modern",
        preserve_flooring: bool = True,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "photo_url": photo_url,
            "room_type": room_type,
            "style": style,
            "preserve_flooring": preserve_flooring,
        }
        if custom_staging_instructions:
            payload["custom_staging_instructions"] = custom_staging_instructions
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/furnish", json=payload)
        return StudioJob.model_validate(data)

    async def stage_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = "living_room",
        style: Optional[str] = "modern",
        preserve_flooring: bool = True,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> StagingResult:
        job = await self.stage(
            photo_url=photo_url,
            room_type=room_type,
            style=style,
            preserve_flooring=preserve_flooring,
            custom_staging_instructions=custom_staging_instructions,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return StagingResult.model_validate(completed.result or {})

    async def declutter(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        removal_targets: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if room_type:
            payload["room_type"] = room_type
        if removal_targets:
            payload["removal_targets"] = removal_targets
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/declutter", json=payload)
        return StudioJob.model_validate(data)

    async def declutter_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        removal_targets: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> DeclutterResult:
        job = await self.declutter(
            photo_url, room_type=room_type, removal_targets=removal_targets, webhook_url=webhook_url
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return DeclutterResult.model_validate(completed.result or {})

    async def empty(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        restore_flooring: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if room_type:
            payload["room_type"] = room_type
        if restore_flooring:
            payload["restore_flooring"] = restore_flooring
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/empty", json=payload)
        return StudioJob.model_validate(data)

    async def empty_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        restore_flooring: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> DeStageEmptyResult:
        job = await self.empty(
            photo_url,
            room_type=room_type,
            restore_flooring=restore_flooring,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return DeStageEmptyResult.model_validate(completed.result or {})

    async def restyle(
        self,
        photo_url: str,
        target_style: str = "scandinavian",
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url, "target_style": target_style}
        if room_type:
            payload["room_type"] = room_type
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/restyle", json=payload)
        return StudioJob.model_validate(data)

    async def restyle_and_wait(
        self,
        photo_url: str,
        target_style: str = "scandinavian",
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> RestyleResult:
        job = await self.restyle(
            photo_url, target_style=target_style, room_type=room_type, webhook_url=webhook_url
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return RestyleResult.model_validate(completed.result or {})

    async def replace_furniture(
        self,
        room_photo_url: str,
        target_furniture: str,
        product_description: Optional[str] = None,
        reference_product_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "room_photo_url": room_photo_url,
            "target_furniture": target_furniture,
        }
        if product_description:
            payload["product_description"] = product_description
        if reference_product_image_url:
            payload["reference_product_image_url"] = reference_product_image_url
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/replace-furniture", json=payload)
        return StudioJob.model_validate(data)

    async def replace_furniture_and_wait(
        self,
        room_photo_url: str,
        target_furniture: str,
        product_description: Optional[str] = None,
        reference_product_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ReplaceFurnitureResult:
        job = await self.replace_furniture(
            room_photo_url,
            target_furniture,
            product_description=product_description,
            reference_product_image_url=reference_product_image_url,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceFurnitureResult.model_validate(completed.result or {})

    async def replace_material(
        self,
        room_photo_url: str,
        surface_type: str,
        material_preset: Optional[str] = None,
        material_sample_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "room_photo_url": room_photo_url,
            "surface_type": surface_type,
        }
        if material_preset:
            payload["material_preset"] = material_preset
        if material_sample_image_url:
            payload["material_sample_image_url"] = material_sample_image_url
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/replace-material", json=payload)
        return StudioJob.model_validate(data)

    async def replace_material_and_wait(
        self,
        room_photo_url: str,
        surface_type: str,
        material_preset: Optional[str] = None,
        material_sample_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> ReplaceMaterialResult:
        job = await self.replace_material(
            room_photo_url,
            surface_type,
            material_preset=material_preset,
            material_sample_image_url=material_sample_image_url,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceMaterialResult.model_validate(completed.result or {})

    async def wall_colors(
        self,
        photo_url: str,
        palette_preset: Optional[str] = "popular_neutrals",
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {"photo_url": photo_url}
        if palette_preset:
            payload["palette_preset"] = palette_preset
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/wall-colors", json=payload)
        return StudioJob.model_validate(data)

    async def wall_colors_and_wait(
        self,
        photo_url: str,
        palette_preset: Optional[str] = "popular_neutrals",
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> WallColorsResult:
        job = await self.wall_colors(
            photo_url, palette_preset=palette_preset, webhook_url=webhook_url
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return WallColorsResult.model_validate(completed.result or {})

    async def twilight(
        self,
        photo_url: str,
        mode: str = "day_to_dusk",
        interior_lighting: bool = True,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        payload: Dict[str, Any] = {
            "photo_url": photo_url,
            "mode": mode,
            "interior_lighting": interior_lighting,
        }
        if webhook_url:
            payload["webhook_url"] = webhook_url
        data = await self._http.post("/v1/studio/staging/twilight", json=payload)
        return StudioJob.model_validate(data)

    async def twilight_and_wait(
        self,
        photo_url: str,
        mode: str = "day_to_dusk",
        interior_lighting: bool = True,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
    ) -> TwilightResult:
        job = await self.twilight(
            photo_url, mode=mode, interior_lighting=interior_lighting, webhook_url=webhook_url
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return TwilightResult.model_validate(completed.result or {})
