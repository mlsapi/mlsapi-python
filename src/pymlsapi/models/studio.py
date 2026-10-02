"""Response models for Studio endpoints.

Field names follow the server's actual job ``result`` payloads. All models allow extra
fields so new server output never breaks parsing, and fields are only required when the
server always returns them. Attribute names from pymlsapi 0.1.0 that the server never
returned are kept as read-only aliases where cheap.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class _Model(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class StudioJob(_Model):
    job_id: str
    status: str
    # The server sends `type`; the Studio spec documents `job_type`.
    type: Optional[str] = Field(default=None, validation_alias=AliasChoices("type", "job_type"))
    progress_percentage: int = 0
    current_step: Optional[str] = None
    estimated_completion_seconds: Optional[float] = None
    status_url: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Staging
# ---------------------------------------------------------------------------


class StagingResult(_Model):
    staged_photo_url: str
    before_after_comparison_url: Optional[str] = None
    room_type: Optional[str] = None
    style: Optional[str] = None
    staging_manifest: List[str] = Field(default_factory=list)


class DeclutterResult(_Model):
    decluttered_photo_url: str
    before_after_comparison_url: Optional[str] = None
    items_removed: List[str] = Field(default_factory=list)


class TwilightResult(_Model):
    enhanced_photo_url: str
    mode: Optional[str] = None
    ambient_lighting_applied: Optional[bool] = None
    before_after_comparison_url: Optional[str] = None


class DeStageEmptyResult(_Model):
    empty_photo_url: str
    before_after_comparison_url: Optional[str] = None
    room_type: Optional[str] = None
    flooring_restored: Optional[str] = None


class RestyleResult(_Model):
    # The server currently returns the misspelled key `retyped_photo_url`; accept both.
    restyled_photo_url: str = Field(
        validation_alias=AliasChoices("restyled_photo_url", "retyped_photo_url")
    )
    before_after_comparison_url: Optional[str] = None
    room_type: Optional[str] = None
    style: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("style", "target_style")
    )

    @property
    def target_style(self) -> Optional[str]:
        """Deprecated: use ``style``."""
        return self.style


class ReplaceFurnitureResult(_Model):
    updated_room_photo_url: str = Field(
        validation_alias=AliasChoices("updated_room_photo_url", "result_photo_url")
    )
    target_replaced: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("target_replaced", "target_furniture")
    )
    reference_matched: Optional[bool] = None
    perspective_alignment: Optional[str] = None

    @property
    def result_photo_url(self) -> str:
        """Deprecated: use ``updated_room_photo_url``."""
        return self.updated_room_photo_url

    @property
    def target_furniture(self) -> Optional[str]:
        """Deprecated: use ``target_replaced``."""
        return self.target_replaced


class ReplaceMaterialResult(_Model):
    updated_room_photo_url: str = Field(
        validation_alias=AliasChoices("updated_room_photo_url", "result_photo_url")
    )
    surface_modified: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("surface_modified", "surface_type")
    )
    material_applied: Optional[str] = None

    @property
    def result_photo_url(self) -> str:
        """Deprecated: use ``updated_room_photo_url``."""
        return self.updated_room_photo_url

    @property
    def surface_type(self) -> Optional[str]:
        """Deprecated: use ``surface_modified``."""
        return self.surface_modified


class SwatchItem(_Model):
    color_name: str
    hex: str
    image_url: Optional[str] = None


class WallColorsResult(_Model):
    comparison_grid_3x3_url: str
    swatch_results: List[SwatchItem] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Enhance
# ---------------------------------------------------------------------------


class ExteriorEnhanceResult(_Model):
    enhanced_photo_url: str
    enhancements_applied: List[str] = Field(default_factory=list)


class UpscaleResult(_Model):
    upscaled_image_url: str
    scale_factor: int = 4
    original_resolution: Optional[str] = None
    target_resolution: Optional[str] = None


# ---------------------------------------------------------------------------
# Floor plan
# ---------------------------------------------------------------------------


class RoomCloseup(_Model):
    room_name: str
    image_url: str


class Render3dResult(_Model):
    isometric_3d_dollhouse_url: str
    thumbnail_url: Optional[str] = None
    room_renders: List[RoomCloseup] = Field(default_factory=list)
    design_system_applied: Optional[Dict[str, Any]] = None


class SpatialSummary(_Model):
    total_rooms_detected: int = 0
    stories: int = 1
    layout_type: Optional[str] = None
    orientation: Optional[str] = None


class FloorPlanAnalysisResponse(_Model):
    style: Optional[str] = None
    spatial_summary: SpatialSummary = Field(default_factory=SpatialSummary)
    rooms: List[Dict[str, Any]] = Field(default_factory=list)
    design_system: Optional[Dict[str, Any]] = None
    isometric_3d_prompt: Optional[str] = None
    render_3d_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Architectural render
# ---------------------------------------------------------------------------


class ArchitecturalRenderResult(_Model):
    rendered_image_url: str
    render_type: Optional[str] = None
    style: Optional[str] = None
    lighting_applied: Optional[str] = None
    source_type: Optional[str] = None  # never returned by the server; kept for compatibility


# ---------------------------------------------------------------------------
# Ad creatives & social
# ---------------------------------------------------------------------------


class CreativeDimensions(_Model):
    width: int
    height: int


class CreativePlacement(_Model):
    placement: str
    image_url: str
    aspect_ratio: Optional[str] = None
    dimensions: Optional[CreativeDimensions] = None
    headline: Optional[str] = None
    price_tag: Optional[str] = None
    address_line: Optional[str] = None
    agent_badge: Optional[str] = None
    legal_disclaimer: Optional[str] = None


class CarouselSlide(_Model):
    slide_number: int
    label: Optional[str] = None
    image_url: str
    headline: Optional[str] = None
    description: Optional[str] = None


class AdCreativesCompliance(_Model):
    fair_housing_passed: bool = True
    equal_housing_logo_present: Optional[bool] = None
    broker_attribution: Optional[str] = None
    legal_lines: List[str] = Field(default_factory=list)
    compliance_status: Optional[str] = None
    audit_score: Optional[float] = None
    checks: Optional[Dict[str, Any]] = None
    visual_quality_rating: Optional[str] = None
    typography_legibility: Optional[str] = None
    compliance_notes: List[str] = Field(default_factory=list)
    flags: List[str] = Field(default_factory=list)  # kept for compatibility


class AdCreativesResult(_Model):
    mls_id: Optional[str] = None
    direction: Optional[str] = None
    trigger: Optional[str] = None
    creatives: Dict[str, CreativePlacement] = Field(default_factory=dict)
    carousel_pack: Optional[List[CarouselSlide]] = None
    compliance: AdCreativesCompliance = Field(default_factory=AdCreativesCompliance)
    generated_at: Optional[str] = None


class SocialPublishItem(_Model):
    platform: Optional[str] = None
    target_type: Optional[str] = None
    status: Optional[str] = None
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    error: Optional[str] = None


class SocialPublishResult(_Model):
    status: str
    publish_id: Optional[str] = None
    results: List[SocialPublishItem] = Field(default_factory=list)
    destinations_dispatched: List[str] = Field(default_factory=list)  # kept for compatibility


# ---------------------------------------------------------------------------
# Video
# ---------------------------------------------------------------------------


class MasteredVideo(_Model):
    aspect_ratio: str
    url: str
    format: Optional[str] = None
    resolution: Optional[str] = None
    thumbnail_url: Optional[str] = None
    target_channels: List[str] = Field(default_factory=list)


class TranscriptWord(_Model):
    word: str
    start: float
    end: float
    highlight: Optional[bool] = None


class TranscriptSegment(_Model):
    start: float
    end: float
    text: str
    words: List[TranscriptWord] = Field(default_factory=list)


class VideoEnhanceResult(_Model):
    duration_seconds: Optional[float] = None
    mastered_videos: List[MasteredVideo] = Field(default_factory=list)
    transcript: List[TranscriptSegment] = Field(default_factory=list)
    audio_enhancements: Optional[Dict[str, Any]] = None
    b_roll_cuts: Optional[List[Dict[str, Any]]] = None


class VideoWalkthroughResult(_Model):
    video_url: str
    poster_url: Optional[str] = None
    duration_seconds: Optional[float] = None
    resolution: Optional[str] = None


class VideoTransitionResult(_Model):
    video_url: str
    poster_url: Optional[str] = None
    duration_seconds: Optional[float] = None
    transition_style: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("transition_style", "transition_type")
    )

    @property
    def transition_type(self) -> Optional[str]:
        """Deprecated: use ``transition_style``."""
        return self.transition_style


class HouseTourResult(_Model):
    video_url: str = Field(validation_alias=AliasChoices("video_url", "video_tour_url"))
    poster_url: Optional[str] = None
    duration_seconds: Optional[float] = None
    shots_count: Optional[int] = None
    script_used: Optional[str] = None
    rooms_included: List[str] = Field(default_factory=list)  # kept for compatibility

    @property
    def video_tour_url(self) -> str:
        """Deprecated: use ``video_url``."""
        return self.video_url


# ---------------------------------------------------------------------------
# Custom prompt & upload
# ---------------------------------------------------------------------------


class CustomStudioResult(_Model):
    image_url: str = Field(validation_alias=AliasChoices("image_url", "output_url"))
    prompt_applied: Optional[str] = Field(
        default=None, validation_alias=AliasChoices("prompt_applied", "prompt_used")
    )
    aspect_ratio: Optional[str] = None

    @property
    def output_url(self) -> str:
        """Deprecated: use ``image_url``."""
        return self.image_url

    @property
    def prompt_used(self) -> Optional[str]:
        """Deprecated: use ``prompt_applied``."""
        return self.prompt_applied


class UploadResult(_Model):
    url: str
    filename: Optional[str] = None
    content_type: Optional[str] = None
    bytes: Optional[int] = None
    storage_key: Optional[str] = None
