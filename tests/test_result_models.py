"""Result models must parse the exact `result` objects the server stores on completed jobs.

Payloads are copied from the `const result: ... = {...}` blocks in src/studio/*.ts (and the
synchronous responses in src/server.ts), with representative values filled in.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Type

import httpx
import pytest
import respx
from pydantic import BaseModel

from pymlsapi import AsyncMlsApiClient, MlsApiClient
from pymlsapi.models import (
    AdCreativesResult,
    ArchitecturalRenderResult,
    ContentGenerationResponse,
    CustomStudioResult,
    DeclutterResult,
    DeStageEmptyResult,
    ExteriorEnhanceResult,
    FloorPlanAnalysisResponse,
    HouseTourResult,
    Render3dResult,
    ReplaceFurnitureResult,
    ReplaceMaterialResult,
    RestyleResult,
    SocialPublishResult,
    StagingResult,
    StudioJob,
    TwilightResult,
    UpscaleResult,
    VideoEnhanceResult,
    VideoTransitionResult,
    VideoWalkthroughResult,
    WallColorsResult,
)

CDN = "https://cdn.mlsapi.dev/studio"

SERVER_RESULTS: Dict[str, Dict[str, Any]] = {
    # staging.ts
    "staging": {
        "staged_photo_url": f"{CDN}/staged/job_1_living_room_luxury.png",
        "before_after_comparison_url": f"{CDN}/staged/compare_living_room_luxury_abc.webp",
        "room_type": "living_room",
        "style": "luxury",
        "staging_manifest": ["Low-profile Italian leather sectional sofa in warm cream"],
    },
    "declutter": {
        "decluttered_photo_url": f"{CDN}/declutter/job_1_living_room.png",
        "before_after_comparison_url": f"{CDN}/declutter/compare_living_room_abc.webp",
        "items_removed": ["Moving boxes and packing materials"],
    },
    "twilight": {
        "enhanced_photo_url": f"{CDN}/twilight/job_1_day_to_dusk.png",
        "mode": "day_to_dusk",
        "ambient_lighting_applied": True,
    },
    "empty": {
        "empty_photo_url": f"{CDN}/staged/job_1_empty_bedroom.png",
        "before_after_comparison_url": f"{CDN}/staged/empty_bedroom_abc.webp",
        "room_type": "bedroom",
        "flooring_restored": "hardwood",
    },
    "restyle": {
        "retyped_photo_url": f"{CDN}/staged/job_1_restyle_living_room_japandi.png",
        "before_after_comparison_url": f"{CDN}/staged/restyle_living_room_japandi_abc.webp",
        "room_type": "living_room",
        "style": "japandi",
    },
    "replace_furniture": {
        "updated_room_photo_url": f"{CDN}/staged/job_1_replace_sofa.png",
        "target_replaced": "sofa",
        "reference_matched": True,
        "perspective_alignment": "100% matched",
    },
    "replace_material": {
        "updated_room_photo_url": f"{CDN}/staged/job_1_mat_flooring.png",
        "surface_modified": "flooring",
        "material_applied": "herringbone_white_oak",
    },
    "wall_colors": {
        "comparison_grid_3x3_url": f"{CDN}/staged/job_1_wall_colors_grid.png",
        "swatch_results": [
            {
                "color_name": "Alabaster White",
                "hex": "#F2EFE8",
                "image_url": f"{CDN}/staged/job_1_wall_1.png",
            },
            {
                "color_name": "Hale Navy",
                "hex": "#303A45",
                "image_url": f"{CDN}/staged/job_1_wall_3.png",
            },
        ],
    },
    # enhance.ts
    "exterior": {
        "enhanced_photo_url": f"{CDN}/enhance/job_1_exterior.png",
        "enhancements_applied": ["blue_sky", "green_grass"],
    },
    "upscale": {
        "upscaled_image_url": f"{CDN}/enhance/job_1_upscale_4x.png",
        "scale_factor": 4,
        "original_resolution": "Standard Resolution",
        "target_resolution": "4096x3072",
    },
    # floorplan.ts
    "render_3d": {
        "isometric_3d_dollhouse_url": f"{CDN}/renders/job_1_dollhouse.png",
        "thumbnail_url": f"{CDN}/renders/job_1_dollhouse.png",
        "room_renders": [
            {"room_name": "Living Room", "image_url": f"{CDN}/renders/job_1_dollhouse.png"}
        ],
        "design_system_applied": {"flooring": "Wide-plank European White Oak", "style": "luxury"},
    },
    # render.ts
    "architectural": {
        "rendered_image_url": f"{CDN}/renders/job_1_arch_interior.png",
        "render_type": "interior",
        "style": "modern_luxury",
        "lighting_applied": "golden_hour (clear_sunny, summer)",
    },
    # custom.ts
    "custom": {
        "image_url": f"{CDN}/custom/job_1.png",
        "prompt_applied": "Convert this living room into a conversation pit",
        "aspect_ratio": "1:1",
    },
    # video.ts
    "video_enhance": {
        "duration_seconds": 38.5,
        "mastered_videos": [
            {
                "aspect_ratio": "9:16",
                "format": "mp4",
                "resolution": "1080x1920",
                "url": f"{CDN}/video/mastered_9_16_abc.mp4",
                "thumbnail_url": f"{CDN}/video/thumb_9_16_abc.webp",
                "target_channels": ["Instagram Reels", "TikTok", "YouTube Shorts"],
            }
        ],
        "transcript": [
            {
                "start": 0.0,
                "end": 3.2,
                "text": "Welcome!",
                "words": [{"word": "Welcome!", "start": 0.0, "end": 0.5, "highlight": True}],
            }
        ],
        "audio_enhancements": {
            "noise_reduction_db": -18.5,
            "echo_cancellation": True,
            "vocal_leveling": True,
        },
        "b_roll_cuts": [
            {
                "timestamp": "00:04.5",
                "room": "kitchen",
                "photo_url": "https://cdn.mlsapi.dev/p/02.webp",
            }
        ],
    },
    "walkthrough": {
        "video_url": f"{CDN}/walkthrough/listing_reel_9_16.mp4",
        "poster_url": f"{CDN}/walkthrough/listing_poster.webp",
        "duration_seconds": 30,
        "resolution": "1080x1920",
    },
    "transition": {
        "video_url": f"{CDN}/video/transition_furnishing_timelapse_abc.mp4",
        "poster_url": f"{CDN}/video/transition_poster_abc.webp",
        "duration_seconds": 5,
        "transition_style": "furnishing_timelapse",
    },
    "tour": {
        "video_url": f"{CDN}/video/house_tour_15s_abc.mp4",
        "poster_url": "https://cdn.mlsapi.dev/photos/front.jpg",
        "duration_seconds": 15,
        "shots_count": 4,
        "script_used": "Shot 1 (Exterior Front): Pan across Grand double-door entrance.",
    },
    # creatives.ts
    "creatives": {
        "direction": "magazine",
        "trigger": "just_listed",
        "creatives": {
            "square": {
                "placement": "square",
                "dimensions": {"width": 1080, "height": 1080},
                "aspect_ratio": "1:1",
                "image_url": f"{CDN}/creatives/listing_square_job_1.png",
                "headline": "JUST LISTED: 3 BD • 2 BA",
                "price_tag": "$500,000",
                "address_line": "1 Main St",
                "agent_badge": "Ann · Acme",
                "legal_disclaimer": "Equal Housing Opportunity.",
            }
        },
        "carousel_pack": [
            {
                "slide_number": 1,
                "label": "square",
                "image_url": f"{CDN}/creatives/sq.png",
                "headline": "JUST LISTED",
                "description": "$500,000",
            }
        ],
        "compliance": {
            "fair_housing_passed": True,
            "equal_housing_logo_present": True,
            "broker_attribution": "Listing courtesy of Acme",
            "legal_lines": ["Equal Housing Opportunity."],
            "compliance_status": "approved",
            "audit_score": 98,
            "checks": {"disclaimer_present": {"passed": True, "details": "ok"}},
            "visual_quality_rating": "excellent",
            "typography_legibility": "sharp",
            "compliance_notes": [],
        },
        "generated_at": "2026-10-01T00:00:00.000Z",
    },
}

MODELS: Dict[str, Type[BaseModel]] = {
    "staging": StagingResult,
    "declutter": DeclutterResult,
    "twilight": TwilightResult,
    "empty": DeStageEmptyResult,
    "restyle": RestyleResult,
    "replace_furniture": ReplaceFurnitureResult,
    "replace_material": ReplaceMaterialResult,
    "wall_colors": WallColorsResult,
    "exterior": ExteriorEnhanceResult,
    "upscale": UpscaleResult,
    "render_3d": Render3dResult,
    "architectural": ArchitecturalRenderResult,
    "custom": CustomStudioResult,
    "video_enhance": VideoEnhanceResult,
    "walkthrough": VideoWalkthroughResult,
    "transition": VideoTransitionResult,
    "tour": HouseTourResult,
    "creatives": AdCreativesResult,
}


@pytest.mark.parametrize("key", sorted(MODELS))
def test_model_parses_server_result(key: str) -> None:
    MODELS[key].model_validate(SERVER_RESULTS[key])


def test_restyle_accepts_server_typo_and_correct_name() -> None:
    typo = RestyleResult.model_validate(SERVER_RESULTS["restyle"])
    assert typo.restyled_photo_url.endswith("restyle_living_room_japandi.png")
    assert typo.style == "japandi"
    assert typo.target_style == "japandi"  # 0.1.0 attribute
    fixed = RestyleResult.model_validate({"restyled_photo_url": "https://x/fixed.png"})
    assert fixed.restyled_photo_url == "https://x/fixed.png"
    assert "retyped_photo_url" not in typo.model_dump()


def test_renamed_fields_keep_old_attribute_names() -> None:
    fur = ReplaceFurnitureResult.model_validate(SERVER_RESULTS["replace_furniture"])
    assert fur.updated_room_photo_url == fur.result_photo_url
    assert fur.target_replaced == fur.target_furniture == "sofa"
    assert fur.reference_matched is True

    mat = ReplaceMaterialResult.model_validate(SERVER_RESULTS["replace_material"])
    assert mat.updated_room_photo_url == mat.result_photo_url
    assert mat.surface_modified == mat.surface_type == "flooring"

    tour = HouseTourResult.model_validate(SERVER_RESULTS["tour"])
    assert tour.video_url == tour.video_tour_url
    assert tour.shots_count == 4

    custom = CustomStudioResult.model_validate(SERVER_RESULTS["custom"])
    assert custom.image_url == custom.output_url
    assert custom.prompt_applied == custom.prompt_used

    trans = VideoTransitionResult.model_validate(SERVER_RESULTS["transition"])
    assert trans.transition_style == trans.transition_type == "furnishing_timelapse"


def test_old_010_shapes_still_parse() -> None:
    assert (
        ReplaceFurnitureResult.model_validate({"result_photo_url": "u"}).updated_room_photo_url
        == "u"
    )
    assert (
        ReplaceMaterialResult.model_validate({"result_photo_url": "u"}).updated_room_photo_url
        == "u"
    )
    assert HouseTourResult.model_validate({"video_tour_url": "u"}).video_url == "u"
    assert (
        CustomStudioResult.model_validate({"output_url": "u", "prompt_used": "p"}).prompt_applied
        == "p"
    )


def test_creatives_result_details() -> None:
    res = AdCreativesResult.model_validate(SERVER_RESULTS["creatives"])
    sq = res.creatives["square"]
    assert sq.dimensions is not None and sq.dimensions.width == 1080
    assert sq.price_tag == "$500,000"
    assert res.carousel_pack is not None and res.carousel_pack[0].slide_number == 1
    assert res.compliance.compliance_status == "approved"
    assert res.mls_id is None  # server omits mls_id when the request had none


def test_video_enhance_details() -> None:
    res = VideoEnhanceResult.model_validate(SERVER_RESULTS["video_enhance"])
    assert res.duration_seconds == 38.5
    assert res.mastered_videos[0].target_channels[0] == "Instagram Reels"
    assert res.transcript[0].words[0].highlight is True


def test_social_publish_result_list() -> None:
    res = SocialPublishResult.model_validate(
        {
            "publish_id": "pub_1",
            "status": "scheduled",
            "results": [
                {
                    "platform": "facebook",
                    "target_type": "page_post",
                    "status": "scheduled",
                    "post_id": "p",
                    "post_url": "u",
                }
            ],
        }
    )
    assert res.results[0].platform == "facebook"


def test_studio_job_submission_and_spec_job_type() -> None:
    sub = StudioJob.model_validate(
        {
            "job_id": "job_studio_1",
            "status": "processing",
            "status_url": "/v1/studio/jobs/job_studio_1",
            "estimated_completion_seconds": 15,
        }
    )
    assert sub.estimated_completion_seconds == 15
    full = StudioJob.model_validate(
        {
            "job_id": "job_studio_1",
            "type": "staging_restyle",
            "status": "completed",
            "progress_percentage": 100,
            "current_step": "done",
            "estimated_completion_seconds": 14,
            "created_at": "2026-10-01T00:00:00Z",
            "completed_at": "2026-10-01T00:00:14Z",
            "status_url": "/v1/studio/jobs/job_studio_1",
            "result": SERVER_RESULTS["restyle"],
        }
    )
    assert full.type == "staging_restyle"
    assert (
        StudioJob.model_validate({"job_id": "j", "status": "completed", "job_type": "x"}).type
        == "x"
    )


def test_floorplan_analysis_response() -> None:
    res = FloorPlanAnalysisResponse.model_validate(
        {
            "style": "luxury",
            "spatial_summary": {
                "total_rooms_detected": 8,
                "stories": 1,
                "layout_type": "split_floorplan",
                "orientation": "north",
            },
            "rooms": [{"name": "Kitchen", "function": "cooking", "approx_size": "medium"}],
            "design_system": {"flooring": "oak", "wall_color_palette": ["white"]},
            "isometric_3d_prompt": "prompt",
        }
    )
    assert res.spatial_summary.orientation == "north"
    assert res.design_system is not None and res.design_system["flooring"] == "oak"


def test_content_response_tolerates_partial_platform_copy() -> None:
    res = ContentGenerationResponse.model_validate(
        {
            "mls_id": "A1",
            "tone": "luxury",
            "generated_at": "2026-10-01T00:00:00Z",
            "content": {
                "social": {
                    "instagram": {"hashtags": ["#home"]},
                    "youtube": {"shorts": {"title": "t", "caption": "c"}},
                },
                "video_script": {
                    "duration_seconds": 30,
                    "format": "vertical_9_16",
                    "scenes": [{"visual": "v"}],
                },
                "investor_pitch": {"headline": "h", "summary": "s", "key_metrics": {}},
            },
        }
    )
    assert res.content.social is not None and res.content.social.instagram is not None


# ---------------------------------------------------------------------------
# End-to-end *_and_wait with real server result shapes (sync + async)
# ---------------------------------------------------------------------------

WAIT_CASES = [
    (
        "staging",
        "restyle_and_wait",
        ("https://img.jpg",),
        "/v1/studio/staging/restyle",
        "restyle",
        RestyleResult,
    ),
    (
        "staging",
        "replace_furniture_and_wait",
        ("https://img.jpg", "sofa"),
        "/v1/studio/staging/replace-furniture",
        "replace_furniture",
        ReplaceFurnitureResult,
    ),
    (
        "staging",
        "replace_material_and_wait",
        ("https://img.jpg", "flooring"),
        "/v1/studio/staging/replace-material",
        "replace_material",
        ReplaceMaterialResult,
    ),
    (
        "video",
        "tour_and_wait",
        ([{"room_name": "Kitchen", "photo_url": "https://img.jpg"}],),
        "/v1/studio/video/tour",
        "tour",
        HouseTourResult,
    ),
    ("custom", "generate_and_wait", ("prompt",), "/v1/studio/custom", "custom", CustomStudioResult),
    (
        "video",
        "walkthrough_and_wait",
        ("https://img.jpg",),
        "/v1/studio/video/walkthrough",
        "walkthrough",
        VideoWalkthroughResult,
    ),
    (
        "creatives",
        "generate_and_wait",
        ("A1",),
        "/v1/studio/creatives/generate",
        "creatives",
        AdCreativesResult,
    ),
]


def _mock_job(router: respx.MockRouter, path: str, key: str) -> None:
    router.post("https://mlsapi.dev" + path).mock(
        return_value=httpx.Response(
            202,
            json={
                "job_id": "job_w",
                "status": "processing",
                "status_url": "/v1/studio/jobs/job_w",
                "estimated_completion_seconds": 1,
            },
        )
    )
    router.get("https://mlsapi.dev/v1/studio/jobs/job_w").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_w",
                "status": "completed",
                "progress_percentage": 100,
                "result": SERVER_RESULTS[key],
            },
        )
    )


@pytest.mark.parametrize("case", WAIT_CASES, ids=[c[1] for c in WAIT_CASES])
def test_and_wait_parses_server_result_sync(case: Any, mock_api_key: str) -> None:
    resource, method, args, path, key, model = case
    with respx.mock() as router:
        _mock_job(router, path, key)
        with MlsApiClient(api_key=mock_api_key) as client:
            res = getattr(getattr(client.studio, resource), method)(*args, poll_interval=0.01)
    assert isinstance(res, model)


@pytest.mark.parametrize("case", WAIT_CASES, ids=[c[1] for c in WAIT_CASES])
def test_and_wait_parses_server_result_async(case: Any, mock_api_key: str) -> None:
    resource, method, args, path, key, model = case

    async def run() -> Any:
        async with AsyncMlsApiClient(api_key=mock_api_key) as client:
            return await getattr(getattr(client.studio, resource), method)(
                *args, poll_interval=0.01
            )

    with respx.mock() as router:
        _mock_job(router, path, key)
        res = asyncio.run(run())
    assert isinstance(res, model)
