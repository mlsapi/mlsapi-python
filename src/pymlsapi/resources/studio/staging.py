from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.requests import WallColorSwatch
from pymlsapi.models.studio import (
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
from pymlsapi.resources._params import compact, resolve_alias, warn_deprecated
from pymlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource

STAGE_PATH = "/v1/studio/staging/stage"
DECLUTTER_PATH = "/v1/studio/staging/declutter"
EMPTY_PATH = "/v1/studio/staging/empty"
RESTYLE_PATH = "/v1/studio/staging/restyle"
REPLACE_FURNITURE_PATH = "/v1/studio/staging/replace-furniture"
REPLACE_MATERIAL_PATH = "/v1/studio/staging/replace-material"
WALL_COLORS_PATH = "/v1/studio/staging/wall-colors"
TWILIGHT_PATH = "/v1/studio/staging/twilight"


def _twilight_body(
    photo_url: str,
    mode: Optional[str],
    webhook_url: Optional[str],
    interior_lighting: Optional[bool],
) -> Dict[str, Any]:
    if interior_lighting is not None:
        warn_deprecated("interior_lighting", stacklevel=4)
    return compact(photo_url=photo_url, mode=mode, webhook_url=webhook_url)


class StagingResource:
    """Synchronous Virtual Staging and Room Transformation operations."""

    def __init__(self, http: HttpClient, jobs: StudioJobsResource) -> None:
        self._http = http
        self._jobs = jobs

    # -- Virtual staging -----------------------------------------------------

    def stage(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        style: Optional[str] = None,
        preserve_flooring: Optional[bool] = None,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        aspect_ratio: Optional[str] = None,
    ) -> StudioJob:
        """Furnish an empty room photo. ``POST /v1/studio/staging/stage``.

        ``aspect_ratio`` is from the Studio spec (``1:1``, ``3:4``, ``4:3``, ``16:9``, ``9:16``).
        """
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            style=style,
            preserve_flooring=preserve_flooring,
            aspect_ratio=aspect_ratio,
            custom_staging_instructions=custom_staging_instructions,
            webhook_url=webhook_url,
        )
        data = self._http.post(STAGE_PATH, json=payload)
        return StudioJob.model_validate(data)

    def stage_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        style: Optional[str] = None,
        preserve_flooring: Optional[bool] = None,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        aspect_ratio: Optional[str] = None,
    ) -> StagingResult:
        job = self.stage(
            photo_url,
            room_type=room_type,
            style=style,
            preserve_flooring=preserve_flooring,
            custom_staging_instructions=custom_staging_instructions,
            webhook_url=webhook_url,
            aspect_ratio=aspect_ratio,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return StagingResult.model_validate(completed.result or {})

    # -- Declutter -----------------------------------------------------------

    def declutter(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        removal_targets: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        """Remove clutter and personal items. ``POST /v1/studio/staging/declutter``."""
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            removal_targets=removal_targets,
            webhook_url=webhook_url,
        )
        data = self._http.post(DECLUTTER_PATH, json=payload)
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
            photo_url,
            room_type=room_type,
            removal_targets=removal_targets,
            webhook_url=webhook_url,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return DeclutterResult.model_validate(completed.result or {})

    # -- Empty (de-stage) ----------------------------------------------------

    def empty(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        restore_flooring: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        """Remove all furniture from a room. ``POST /v1/studio/staging/empty``."""
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            restore_flooring=restore_flooring,
            webhook_url=webhook_url,
        )
        data = self._http.post(EMPTY_PATH, json=payload)
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

    # -- Restyle -------------------------------------------------------------

    def restyle(
        self,
        photo_url: str,
        style: Optional[str] = None,
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        retain_layout: Optional[bool] = None,
        custom_restyle_instructions: Optional[str] = None,
        target_style: Optional[str] = None,
    ) -> StudioJob:
        """Restyle a furnished room. ``POST /v1/studio/staging/restyle``.

        ``target_style`` is a deprecated alias for ``style``.
        """
        style = resolve_alias("style", style, "target_style", target_style)
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            style=style,
            retain_layout=retain_layout,
            custom_restyle_instructions=custom_restyle_instructions,
            webhook_url=webhook_url,
        )
        data = self._http.post(RESTYLE_PATH, json=payload)
        return StudioJob.model_validate(data)

    def restyle_and_wait(
        self,
        photo_url: str,
        style: Optional[str] = None,
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        retain_layout: Optional[bool] = None,
        custom_restyle_instructions: Optional[str] = None,
        target_style: Optional[str] = None,
    ) -> RestyleResult:
        job = self.restyle(
            photo_url,
            style=style,
            room_type=room_type,
            webhook_url=webhook_url,
            retain_layout=retain_layout,
            custom_restyle_instructions=custom_restyle_instructions,
            target_style=target_style,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return RestyleResult.model_validate(completed.result or {})

    # -- Replace furniture ---------------------------------------------------

    def replace_furniture(
        self,
        room_photo_url: str,
        target_furniture: str,
        product_description: Optional[str] = None,
        reference_product_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        target_location_notes: Optional[str] = None,
        preserve_surroundings: Optional[bool] = None,
    ) -> StudioJob:
        """Swap one piece of furniture. ``POST /v1/studio/staging/replace-furniture``."""
        payload = compact(
            room_photo_url=room_photo_url,
            target_furniture=target_furniture,
            reference_product_image_url=reference_product_image_url,
            product_description=product_description,
            target_location_notes=target_location_notes,
            preserve_surroundings=preserve_surroundings,
            webhook_url=webhook_url,
        )
        data = self._http.post(REPLACE_FURNITURE_PATH, json=payload)
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
        *,
        target_location_notes: Optional[str] = None,
        preserve_surroundings: Optional[bool] = None,
    ) -> ReplaceFurnitureResult:
        job = self.replace_furniture(
            room_photo_url,
            target_furniture,
            product_description=product_description,
            reference_product_image_url=reference_product_image_url,
            webhook_url=webhook_url,
            target_location_notes=target_location_notes,
            preserve_surroundings=preserve_surroundings,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceFurnitureResult.model_validate(completed.result or {})

    # -- Replace material ----------------------------------------------------

    def replace_material(
        self,
        room_photo_url: str,
        surface_type: str,
        material_preset: Optional[str] = None,
        material_sample_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        custom_finish_notes: Optional[str] = None,
    ) -> StudioJob:
        """Resurface floors, walls, counters, etc. ``POST /v1/studio/staging/replace-material``."""
        payload = compact(
            room_photo_url=room_photo_url,
            surface_type=surface_type,
            material_sample_image_url=material_sample_image_url,
            material_preset=material_preset,
            custom_finish_notes=custom_finish_notes,
            webhook_url=webhook_url,
        )
        data = self._http.post(REPLACE_MATERIAL_PATH, json=payload)
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
        *,
        custom_finish_notes: Optional[str] = None,
    ) -> ReplaceMaterialResult:
        job = self.replace_material(
            room_photo_url,
            surface_type,
            material_preset=material_preset,
            material_sample_image_url=material_sample_image_url,
            webhook_url=webhook_url,
            custom_finish_notes=custom_finish_notes,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceMaterialResult.model_validate(completed.result or {})

    # -- Wall colors ---------------------------------------------------------

    def wall_colors(
        self,
        photo_url: str,
        palette_preset: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        custom_colors: Optional[List[WallColorSwatch]] = None,
    ) -> StudioJob:
        """Render the room in a grid of wall paint colors. ``POST /v1/studio/staging/wall-colors``.

        ``custom_colors`` is a list of ``{"name": ..., "hex": ...}`` dicts.
        """
        payload = compact(
            photo_url=photo_url,
            palette_preset=palette_preset,
            custom_colors=custom_colors,
            webhook_url=webhook_url,
        )
        data = self._http.post(WALL_COLORS_PATH, json=payload)
        return StudioJob.model_validate(data)

    def wall_colors_and_wait(
        self,
        photo_url: str,
        palette_preset: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        custom_colors: Optional[List[WallColorSwatch]] = None,
    ) -> WallColorsResult:
        job = self.wall_colors(
            photo_url,
            palette_preset=palette_preset,
            webhook_url=webhook_url,
            custom_colors=custom_colors,
        )
        completed = self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return WallColorsResult.model_validate(completed.result or {})

    # -- Twilight ------------------------------------------------------------

    def twilight(
        self,
        photo_url: str,
        mode: Optional[str] = None,
        *,
        webhook_url: Optional[str] = None,
        interior_lighting: Optional[bool] = None,
    ) -> StudioJob:
        """Day-to-dusk or blue-sky replacement. ``POST /v1/studio/staging/twilight``.

        ``interior_lighting`` is deprecated and ignored (the server never read it).
        """
        payload = _twilight_body(photo_url, mode, webhook_url, interior_lighting)
        data = self._http.post(TWILIGHT_PATH, json=payload)
        return StudioJob.model_validate(data)

    def twilight_and_wait(
        self,
        photo_url: str,
        mode: Optional[str] = None,
        *,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        interior_lighting: Optional[bool] = None,
    ) -> TwilightResult:
        job = self.twilight(
            photo_url,
            mode=mode,
            webhook_url=webhook_url,
            interior_lighting=interior_lighting,
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

    # -- Virtual staging -----------------------------------------------------

    async def stage(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        style: Optional[str] = None,
        preserve_flooring: Optional[bool] = None,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        aspect_ratio: Optional[str] = None,
    ) -> StudioJob:
        """Furnish an empty room photo. ``POST /v1/studio/staging/stage``.

        ``aspect_ratio`` is from the Studio spec (``1:1``, ``3:4``, ``4:3``, ``16:9``, ``9:16``).
        """
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            style=style,
            preserve_flooring=preserve_flooring,
            aspect_ratio=aspect_ratio,
            custom_staging_instructions=custom_staging_instructions,
            webhook_url=webhook_url,
        )
        data = await self._http.post(STAGE_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def stage_and_wait(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        style: Optional[str] = None,
        preserve_flooring: Optional[bool] = None,
        custom_staging_instructions: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        aspect_ratio: Optional[str] = None,
    ) -> StagingResult:
        job = await self.stage(
            photo_url,
            room_type=room_type,
            style=style,
            preserve_flooring=preserve_flooring,
            custom_staging_instructions=custom_staging_instructions,
            webhook_url=webhook_url,
            aspect_ratio=aspect_ratio,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return StagingResult.model_validate(completed.result or {})

    # -- Declutter -----------------------------------------------------------

    async def declutter(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        removal_targets: Optional[List[str]] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        """Remove clutter and personal items. ``POST /v1/studio/staging/declutter``."""
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            removal_targets=removal_targets,
            webhook_url=webhook_url,
        )
        data = await self._http.post(DECLUTTER_PATH, json=payload)
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
            photo_url,
            room_type=room_type,
            removal_targets=removal_targets,
            webhook_url=webhook_url,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return DeclutterResult.model_validate(completed.result or {})

    # -- Empty (de-stage) ----------------------------------------------------

    async def empty(
        self,
        photo_url: str,
        room_type: Optional[str] = None,
        restore_flooring: Optional[str] = None,
        webhook_url: Optional[str] = None,
    ) -> StudioJob:
        """Remove all furniture from a room. ``POST /v1/studio/staging/empty``."""
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            restore_flooring=restore_flooring,
            webhook_url=webhook_url,
        )
        data = await self._http.post(EMPTY_PATH, json=payload)
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

    # -- Restyle -------------------------------------------------------------

    async def restyle(
        self,
        photo_url: str,
        style: Optional[str] = None,
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        retain_layout: Optional[bool] = None,
        custom_restyle_instructions: Optional[str] = None,
        target_style: Optional[str] = None,
    ) -> StudioJob:
        """Restyle a furnished room. ``POST /v1/studio/staging/restyle``.

        ``target_style`` is a deprecated alias for ``style``.
        """
        style = resolve_alias("style", style, "target_style", target_style)
        payload = compact(
            photo_url=photo_url,
            room_type=room_type,
            style=style,
            retain_layout=retain_layout,
            custom_restyle_instructions=custom_restyle_instructions,
            webhook_url=webhook_url,
        )
        data = await self._http.post(RESTYLE_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def restyle_and_wait(
        self,
        photo_url: str,
        style: Optional[str] = None,
        room_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        retain_layout: Optional[bool] = None,
        custom_restyle_instructions: Optional[str] = None,
        target_style: Optional[str] = None,
    ) -> RestyleResult:
        job = await self.restyle(
            photo_url,
            style=style,
            room_type=room_type,
            webhook_url=webhook_url,
            retain_layout=retain_layout,
            custom_restyle_instructions=custom_restyle_instructions,
            target_style=target_style,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return RestyleResult.model_validate(completed.result or {})

    # -- Replace furniture ---------------------------------------------------

    async def replace_furniture(
        self,
        room_photo_url: str,
        target_furniture: str,
        product_description: Optional[str] = None,
        reference_product_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        target_location_notes: Optional[str] = None,
        preserve_surroundings: Optional[bool] = None,
    ) -> StudioJob:
        """Swap one piece of furniture. ``POST /v1/studio/staging/replace-furniture``."""
        payload = compact(
            room_photo_url=room_photo_url,
            target_furniture=target_furniture,
            reference_product_image_url=reference_product_image_url,
            product_description=product_description,
            target_location_notes=target_location_notes,
            preserve_surroundings=preserve_surroundings,
            webhook_url=webhook_url,
        )
        data = await self._http.post(REPLACE_FURNITURE_PATH, json=payload)
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
        *,
        target_location_notes: Optional[str] = None,
        preserve_surroundings: Optional[bool] = None,
    ) -> ReplaceFurnitureResult:
        job = await self.replace_furniture(
            room_photo_url,
            target_furniture,
            product_description=product_description,
            reference_product_image_url=reference_product_image_url,
            webhook_url=webhook_url,
            target_location_notes=target_location_notes,
            preserve_surroundings=preserve_surroundings,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceFurnitureResult.model_validate(completed.result or {})

    # -- Replace material ----------------------------------------------------

    async def replace_material(
        self,
        room_photo_url: str,
        surface_type: str,
        material_preset: Optional[str] = None,
        material_sample_image_url: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        custom_finish_notes: Optional[str] = None,
    ) -> StudioJob:
        """Resurface floors, walls, counters, etc. ``POST /v1/studio/staging/replace-material``."""
        payload = compact(
            room_photo_url=room_photo_url,
            surface_type=surface_type,
            material_sample_image_url=material_sample_image_url,
            material_preset=material_preset,
            custom_finish_notes=custom_finish_notes,
            webhook_url=webhook_url,
        )
        data = await self._http.post(REPLACE_MATERIAL_PATH, json=payload)
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
        *,
        custom_finish_notes: Optional[str] = None,
    ) -> ReplaceMaterialResult:
        job = await self.replace_material(
            room_photo_url,
            surface_type,
            material_preset=material_preset,
            material_sample_image_url=material_sample_image_url,
            webhook_url=webhook_url,
            custom_finish_notes=custom_finish_notes,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return ReplaceMaterialResult.model_validate(completed.result or {})

    # -- Wall colors ---------------------------------------------------------

    async def wall_colors(
        self,
        photo_url: str,
        palette_preset: Optional[str] = None,
        webhook_url: Optional[str] = None,
        *,
        custom_colors: Optional[List[WallColorSwatch]] = None,
    ) -> StudioJob:
        """Render the room in a grid of wall paint colors. ``POST /v1/studio/staging/wall-colors``.

        ``custom_colors`` is a list of ``{"name": ..., "hex": ...}`` dicts.
        """
        payload = compact(
            photo_url=photo_url,
            palette_preset=palette_preset,
            custom_colors=custom_colors,
            webhook_url=webhook_url,
        )
        data = await self._http.post(WALL_COLORS_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def wall_colors_and_wait(
        self,
        photo_url: str,
        palette_preset: Optional[str] = None,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        *,
        custom_colors: Optional[List[WallColorSwatch]] = None,
    ) -> WallColorsResult:
        job = await self.wall_colors(
            photo_url,
            palette_preset=palette_preset,
            webhook_url=webhook_url,
            custom_colors=custom_colors,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return WallColorsResult.model_validate(completed.result or {})

    # -- Twilight ------------------------------------------------------------

    async def twilight(
        self,
        photo_url: str,
        mode: Optional[str] = None,
        *,
        webhook_url: Optional[str] = None,
        interior_lighting: Optional[bool] = None,
    ) -> StudioJob:
        """Day-to-dusk or blue-sky replacement. ``POST /v1/studio/staging/twilight``.

        ``interior_lighting`` is deprecated and ignored (the server never read it).
        """
        payload = _twilight_body(photo_url, mode, webhook_url, interior_lighting)
        data = await self._http.post(TWILIGHT_PATH, json=payload)
        return StudioJob.model_validate(data)

    async def twilight_and_wait(
        self,
        photo_url: str,
        mode: Optional[str] = None,
        *,
        webhook_url: Optional[str] = None,
        timeout_seconds: float = 90.0,
        poll_interval: float = 2.0,
        on_progress: Optional[Callable[[StudioJob], None]] = None,
        interior_lighting: Optional[bool] = None,
    ) -> TwilightResult:
        job = await self.twilight(
            photo_url,
            mode=mode,
            webhook_url=webhook_url,
            interior_lighting=interior_lighting,
        )
        completed = await self._jobs.wait_for(
            job.job_id,
            timeout_seconds=timeout_seconds,
            poll_interval=poll_interval,
            on_progress=on_progress,
        )
        return TwilightResult.model_validate(completed.result or {})
