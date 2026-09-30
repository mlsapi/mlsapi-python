from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class StudioJob(BaseModel):
    job_id: str
    status: str
    progress_percentage: int = 0
    current_step: Optional[str] = None
    status_url: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None


class StagingResult(BaseModel):
    staged_photo_url: str
    before_after_comparison_url: Optional[str] = None
    room_type: Optional[str] = None
    style: Optional[str] = None
    staging_manifest: List[str] = Field(default_factory=list)


class DeclutterResult(BaseModel):
    decluttered_photo_url: str
    before_after_comparison_url: Optional[str] = None
    items_removed: List[str] = Field(default_factory=list)


class TwilightResult(BaseModel):
    enhanced_photo_url: str
    before_after_comparison_url: Optional[str] = None
    mode: Optional[str] = None


class DeStageEmptyResult(BaseModel):
    empty_photo_url: str
    before_after_comparison_url: Optional[str] = None
    flooring_restored: Optional[str] = None


class RestyleResult(BaseModel):
    restyled_photo_url: str
    before_after_comparison_url: Optional[str] = None
    target_style: Optional[str] = None


class ReplaceFurnitureResult(BaseModel):
    result_photo_url: str
    target_furniture: Optional[str] = None


class ReplaceMaterialResult(BaseModel):
    result_photo_url: str
    surface_type: Optional[str] = None
    material_applied: Optional[str] = None


class SwatchItem(BaseModel):
    color_name: str
    hex: str
    image_url: str


class WallColorsResult(BaseModel):
    comparison_grid_3x3_url: str
    swatch_results: List[SwatchItem] = Field(default_factory=list)


class ExteriorEnhanceResult(BaseModel):
    enhanced_photo_url: str
    enhancements_applied: List[str] = Field(default_factory=list)


class UpscaleResult(BaseModel):
    upscaled_image_url: str
    target_resolution: Optional[str] = None
    scale_factor: int = 4


class RoomCloseup(BaseModel):
    room_name: str
    image_url: str


class Render3dResult(BaseModel):
    isometric_3d_dollhouse_url: str
    thumbnail_url: Optional[str] = None
    room_renders: List[RoomCloseup] = Field(default_factory=list)


class SpatialSummary(BaseModel):
    total_rooms_detected: int = 0
    stories: int = 1
    layout_type: Optional[str] = None


class FloorPlanAnalysisResponse(BaseModel):
    style: Optional[str] = None
    spatial_summary: SpatialSummary = Field(default_factory=SpatialSummary)
    rooms: List[Dict[str, Any]] = Field(default_factory=list)
    isometric_3d_prompt: Optional[str] = None
    render_3d_url: Optional[str] = None


class ArchitecturalRenderResult(BaseModel):
    rendered_image_url: str
    source_type: Optional[str] = None


class CreativePlacement(BaseModel):
    placement: str
    image_url: str
    aspect_ratio: Optional[str] = None


class AdCreativesCompliance(BaseModel):
    fair_housing_passed: bool = True
    flags: List[str] = Field(default_factory=list)


class AdCreativesResult(BaseModel):
    mls_id: Optional[str] = None
    creatives: Dict[str, CreativePlacement] = Field(default_factory=dict)
    compliance: AdCreativesCompliance = Field(default_factory=AdCreativesCompliance)


class SocialPublishResult(BaseModel):
    status: str
    destinations_dispatched: List[str] = Field(default_factory=list)
    results: Dict[str, Any] = Field(default_factory=dict)


class MasteredVideo(BaseModel):
    aspect_ratio: str
    url: str


class VideoEnhanceResult(BaseModel):
    mastered_videos: List[MasteredVideo] = Field(default_factory=list)


class VideoWalkthroughResult(BaseModel):
    video_url: str
    duration_seconds: Optional[float] = None


class VideoTransitionResult(BaseModel):
    video_url: str
    transition_type: Optional[str] = None


class HouseTourResult(BaseModel):
    video_tour_url: str
    rooms_included: List[str] = Field(default_factory=list)


class CustomStudioResult(BaseModel):
    output_url: str
    prompt_used: str


class UploadResult(BaseModel):
    url: str
    filename: Optional[str] = None
    content_type: Optional[str] = None
    bytes: Optional[int] = None
