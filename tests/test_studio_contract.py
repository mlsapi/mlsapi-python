"""Request contract tests: exact path + JSON body for every Studio/content method.

Each case runs against both the sync and async clients. Field names must equal the JSON
keys the server reads (src/server.ts + src/studio/*.ts) / the JS SDK request types, and
``None`` arguments must be omitted.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, List, Tuple

import httpx
import pytest
import respx

from pymlsapi import AsyncMlsApiClient, MlsApiClient
from pymlsapi._version import __version__

BASE = "https://mlsapi.dev"
SUBMITTED = {
    "job_id": "job_studio_01TEST",
    "status": "processing",
    "status_url": "/v1/studio/jobs/job_studio_01TEST",
    "estimated_completion_seconds": 15,
}
PUBLISHED = {
    "publish_id": "pub_abc123",
    "status": "dispatched",
    "results": [
        {
            "platform": "instagram",
            "target_type": "reels",
            "status": "published",
            "post_id": "post_instagram_x1",
            "post_url": "https://instagram.com/p/post_instagram_x1",
        }
    ],
}

PHOTO = "https://cdn.mlsapi.dev/photos/room.jpg"
HOOK = "https://example.com/hook"

# (resource path, method, args, kwargs, expected path, expected body)
Case = Tuple[str, str, Tuple[Any, ...], Dict[str, Any], str, Dict[str, Any]]

CASES: List[Case] = [
    # -- staging ----------------------------------------------------------------
    ("studio.staging", "stage", (PHOTO,), {}, "/v1/studio/staging/stage", {"photo_url": PHOTO}),
    (
        "studio.staging",
        "stage",
        (PHOTO,),
        dict(
            room_type="bedroom",
            style="japandi",
            preserve_flooring=False,
            custom_staging_instructions="oak bed",
            webhook_url=HOOK,
            aspect_ratio="16:9",
        ),
        "/v1/studio/staging/stage",
        {
            "photo_url": PHOTO,
            "room_type": "bedroom",
            "style": "japandi",
            "preserve_flooring": False,
            "custom_staging_instructions": "oak bed",
            "webhook_url": HOOK,
            "aspect_ratio": "16:9",
        },
    ),
    (
        "studio.staging",
        "declutter",
        (PHOTO,),
        dict(room_type="kitchen", removal_targets=["boxes"], webhook_url=HOOK),
        "/v1/studio/staging/declutter",
        {
            "photo_url": PHOTO,
            "room_type": "kitchen",
            "removal_targets": ["boxes"],
            "webhook_url": HOOK,
        },
    ),
    (
        "studio.staging",
        "empty",
        (PHOTO,),
        dict(room_type="bedroom", restore_flooring="tile"),
        "/v1/studio/staging/empty",
        {"photo_url": PHOTO, "room_type": "bedroom", "restore_flooring": "tile"},
    ),
    ("studio.staging", "restyle", (PHOTO,), {}, "/v1/studio/staging/restyle", {"photo_url": PHOTO}),
    (
        "studio.staging",
        "restyle",
        (PHOTO,),
        dict(
            style="japandi",
            room_type="living_room",
            retain_layout=True,
            custom_restyle_instructions="paper lanterns",
            webhook_url=HOOK,
        ),
        "/v1/studio/staging/restyle",
        {
            "photo_url": PHOTO,
            "style": "japandi",
            "room_type": "living_room",
            "retain_layout": True,
            "custom_restyle_instructions": "paper lanterns",
            "webhook_url": HOOK,
        },
    ),
    (
        "studio.staging",
        "replace_furniture",
        (PHOTO, "sofa"),
        dict(
            product_description="tan leather",
            reference_product_image_url="https://ikea.example/sofa.jpg",
            target_location_notes="against the left wall",
            preserve_surroundings=True,
            webhook_url=HOOK,
        ),
        "/v1/studio/staging/replace-furniture",
        {
            "room_photo_url": PHOTO,
            "target_furniture": "sofa",
            "product_description": "tan leather",
            "reference_product_image_url": "https://ikea.example/sofa.jpg",
            "target_location_notes": "against the left wall",
            "preserve_surroundings": True,
            "webhook_url": HOOK,
        },
    ),
    (
        "studio.staging",
        "replace_material",
        (PHOTO, "flooring"),
        dict(
            material_preset="herringbone_white_oak",
            material_sample_image_url="https://cdn.example/oak.jpg",
            custom_finish_notes="matte",
        ),
        "/v1/studio/staging/replace-material",
        {
            "room_photo_url": PHOTO,
            "surface_type": "flooring",
            "material_preset": "herringbone_white_oak",
            "material_sample_image_url": "https://cdn.example/oak.jpg",
            "custom_finish_notes": "matte",
        },
    ),
    (
        "studio.staging",
        "wall_colors",
        (PHOTO,),
        {},
        "/v1/studio/staging/wall-colors",
        {"photo_url": PHOTO},
    ),
    (
        "studio.staging",
        "wall_colors",
        (PHOTO,),
        dict(
            palette_preset="modern_earth",
            custom_colors=[{"name": "Hale Navy", "hex": "#303A45"}],
            webhook_url=HOOK,
        ),
        "/v1/studio/staging/wall-colors",
        {
            "photo_url": PHOTO,
            "palette_preset": "modern_earth",
            "custom_colors": [{"name": "Hale Navy", "hex": "#303A45"}],
            "webhook_url": HOOK,
        },
    ),
    (
        "studio.staging",
        "twilight",
        (PHOTO,),
        {},
        "/v1/studio/staging/twilight",
        {"photo_url": PHOTO},
    ),
    (
        "studio.staging",
        "twilight",
        (PHOTO,),
        dict(mode="blue_sky_replace", webhook_url=HOOK),
        "/v1/studio/staging/twilight",
        {"photo_url": PHOTO, "mode": "blue_sky_replace", "webhook_url": HOOK},
    ),
    # -- enhance ----------------------------------------------------------------
    (
        "studio.enhance",
        "exterior",
        (PHOTO,),
        dict(enhancements=["blue_sky", "clean_pool"]),
        "/v1/studio/enhance/exterior",
        {"photo_url": PHOTO, "enhancements": ["blue_sky", "clean_pool"]},
    ),
    ("studio.enhance", "upscale", (PHOTO,), {}, "/v1/studio/enhance/upscale", {"image_url": PHOTO}),
    (
        "studio.enhance",
        "upscale",
        (PHOTO,),
        dict(scale_factor=2, enhance_details=False),
        "/v1/studio/enhance/upscale",
        {"image_url": PHOTO, "scale_factor": 2, "enhance_details": False},
    ),
    # -- floorplan --------------------------------------------------------------
    (
        "studio.floorplan",
        "render_3d",
        ("https://cdn.example/plan.png",),
        dict(
            style="luxury",
            include_room_closeups=True,
            target_rooms=["kitchen"],
            custom_prompt="oak",
        ),
        "/v1/studio/floorplan/render-3d",
        {
            "floorplan_image_url": "https://cdn.example/plan.png",
            "style": "luxury",
            "include_room_closeups": True,
            "target_rooms": ["kitchen"],
            "custom_prompt": "oak",
        },
    ),
    # -- render -----------------------------------------------------------------
    (
        "studio.render",
        "architectural",
        ("https://cdn.example/cad.png",),
        dict(
            render_type="exterior",
            style="modern_luxury",
            lighting_environment="twilight",
            weather="snowy",
            season="winter",
            custom_instructions="travertine wall",
            webhook_url=HOOK,
        ),
        "/v1/studio/render/architectural",
        {
            "source_image_url": "https://cdn.example/cad.png",
            "render_type": "exterior",
            "style": "modern_luxury",
            "lighting_environment": "twilight",
            "weather": "snowy",
            "season": "winter",
            "custom_instructions": "travertine wall",
            "webhook_url": HOOK,
        },
    ),
    # -- custom -----------------------------------------------------------------
    ("studio.custom", "generate", ("a pit",), {}, "/v1/studio/custom", {"prompt": "a pit"}),
    (
        "studio.custom",
        "generate",
        ("a pit",),
        dict(reference_image_urls=[PHOTO], photo_url=PHOTO, aspect_ratio="16:9", webhook_url=HOOK),
        "/v1/studio/custom",
        {
            "prompt": "a pit",
            "reference_image_urls": [PHOTO],
            "photo_url": PHOTO,
            "aspect_ratio": "16:9",
            "webhook_url": HOOK,
        },
    ),
    # -- creatives --------------------------------------------------------------
    (
        "studio.creatives",
        "generate",
        (),
        dict(photo_url=PHOTO),
        "/v1/studio/creatives/generate",
        {"photo_url": PHOTO},
    ),
    (
        "studio.creatives",
        "generate",
        (),
        dict(
            mls_id="A12079565",
            photos=[PHOTO],
            photo_url=PHOTO,
            property_details={"address": "1 Main St", "price": 500000, "beds": 3},
            direction="bold",
            placements=["square", "feed_portrait"],
            trigger="just_listed",
            ad_type="open_house",
            custom_badge="OPEN SAT",
            custom_headline="Sunny corner lot",
            realtor_photo="https://cdn.example/agent.jpg",
            agent_headshot_url="https://cdn.example/agent2.jpg",
            brand_kit={"agent_name": "Ann", "brokerage_name": "Acme"},
            highlights=["Pool"],
            open_house={"day": "Saturday", "time": "1-4pm"},
            include_carousel=True,
            webhook_url=HOOK,
        ),
        "/v1/studio/creatives/generate",
        {
            "mls_id": "A12079565",
            "photos": [PHOTO],
            "photo_url": PHOTO,
            "property_details": {"address": "1 Main St", "price": 500000, "beds": 3},
            "direction": "bold",
            "placements": ["square", "feed_portrait"],
            "trigger": "just_listed",
            "ad_type": "open_house",
            "custom_badge": "OPEN SAT",
            "custom_headline": "Sunny corner lot",
            "realtor_photo": "https://cdn.example/agent.jpg",
            "agent_headshot_url": "https://cdn.example/agent2.jpg",
            "brand_kit": {"agent_name": "Ann", "brokerage_name": "Acme"},
            "highlights": ["Pool"],
            "open_house": {"day": "Saturday", "time": "1-4pm"},
            "include_carousel": True,
            "webhook_url": HOOK,
        },
    ),
    # -- video ------------------------------------------------------------------
    (
        "studio.video",
        "enhance",
        ("https://cdn.example/raw.mp4",),
        {},
        "/v1/studio/video/enhance",
        {"video_url": "https://cdn.example/raw.mp4"},
    ),
    (
        "studio.video",
        "enhance",
        ("https://cdn.example/raw.mp4",),
        dict(
            features={"studio_voice": True, "b_roll_photo_insertion": True},
            subtitle_style={"font_theme": "clean_minimal"},
            export_aspect_ratios=["9:16"],
            mls_id="A1",
        ),
        "/v1/studio/video/enhance",
        {
            "video_url": "https://cdn.example/raw.mp4",
            "features": {"studio_voice": True, "b_roll_photo_insertion": True},
            "subtitle_style": {"font_theme": "clean_minimal"},
            "export_aspect_ratios": ["9:16"],
            "mls_id": "A1",
        },
    ),
    (
        "studio.video",
        "walkthrough",
        (),
        dict(
            photo_url=PHOTO,
            motion="slow_zoom_in",
            duration_seconds=5,
            custom_motion_prompt="push toward fireplace",
            aspect_ratio="16:9",
            mls_id="A1",
            webhook_url=HOOK,
        ),
        "/v1/studio/video/walkthrough",
        {
            "photo_url": PHOTO,
            "motion": "slow_zoom_in",
            "duration_seconds": 5,
            "custom_motion_prompt": "push toward fireplace",
            "aspect_ratio": "16:9",
            "mls_id": "A1",
            "webhook_url": HOOK,
        },
    ),
    (
        "studio.video",
        "walkthrough",
        (),
        dict(photo_urls=[PHOTO], voice_id="v1", music_mood="calm"),
        "/v1/studio/video/walkthrough",
        {"photo_urls": [PHOTO], "voice_id": "v1", "music_mood": "calm"},
    ),
    (
        "studio.video",
        "transition",
        ("https://a.jpg", "https://b.jpg"),
        {},
        "/v1/studio/video/transition",
        {"start_image_url": "https://a.jpg", "end_image_url": "https://b.jpg"},
    ),
    (
        "studio.video",
        "transition",
        ("https://a.jpg", "https://b.jpg"),
        dict(duration_seconds=10, transition_style="smooth_dissolve", aspect_ratio="1:1"),
        "/v1/studio/video/transition",
        {
            "start_image_url": "https://a.jpg",
            "end_image_url": "https://b.jpg",
            "duration_seconds": 10,
            "transition_style": "smooth_dissolve",
            "aspect_ratio": "1:1",
        },
    ),
    (
        "studio.video",
        "tour",
        ([{"room_name": "Kitchen", "photo_url": PHOTO, "highlight": "island"}],),
        dict(
            duration_seconds=15,
            auto_script=True,
            shot_script="Open on the kitchen",
            aspect_ratio="9:16",
            music_genre="ambient_luxury",
            webhook_url=HOOK,
        ),
        "/v1/studio/video/tour",
        {
            "ordered_photos": [{"room_name": "Kitchen", "photo_url": PHOTO, "highlight": "island"}],
            "duration_seconds": 15,
            "auto_script": True,
            "shot_script": "Open on the kitchen",
            "aspect_ratio": "9:16",
            "music_genre": "ambient_luxury",
            "webhook_url": HOOK,
        },
    ),
    # -- content ----------------------------------------------------------------
    ("content", "generate", ("A12079565",), {}, "/v1/listing/A12079565/content", {}),
    (
        "content",
        "generate",
        ("A12079565",),
        dict(
            outputs=["social"],
            tone="approachable",
            social_platforms=["instagram"],
            target_audience="first-time buyers",
            custom_notes="new roof",
            property_details={"beds": 3, "highlights": ["Pool"]},
        ),
        "/v1/listing/A12079565/content",
        {
            "outputs": ["social"],
            "tone": "approachable",
            "social_platforms": ["instagram"],
            "target_audience": "first-time buyers",
            "custom_notes": "new roof",
            "property_details": {"beds": 3, "highlights": ["Pool"]},
        },
    ),
]

CONTENT_RESPONSE = {"mls_id": "A12079565", "tone": "luxury", "content": {}}
FLOORPLAN_RESPONSE = {"style": "luxury", "rooms": [], "isometric_3d_prompt": "x"}


def _resolve(client: Any, dotted: str) -> Any:
    obj = client
    for part in dotted.split("."):
        obj = getattr(obj, part)
    return obj


def _response_for(path: str) -> Dict[str, Any]:
    if path.endswith("/content"):
        return CONTENT_RESPONSE
    if path.endswith("/analyze"):
        return FLOORPLAN_RESPONSE
    if path.endswith("/social/publish"):
        return PUBLISHED
    return SUBMITTED


def _case_id(case: Case) -> str:
    return f"{case[0]}.{case[1]}[{len(case[3])}kw]"


@pytest.mark.parametrize("case", CASES, ids=[_case_id(c) for c in CASES])
def test_sync_request_contract(case: Case, mock_api_key: str) -> None:
    resource, method, args, kwargs, path, body = case
    with respx.mock(assert_all_called=True) as router:
        route = router.post(BASE + path).mock(
            return_value=httpx.Response(202, json=_response_for(path))
        )
        with MlsApiClient(api_key=mock_api_key) as client:
            getattr(_resolve(client, resource), method)(*args, **kwargs)
        assert json.loads(route.calls.last.request.content) == body


@pytest.mark.parametrize("case", CASES, ids=[_case_id(c) for c in CASES])
def test_async_request_contract(case: Case, mock_api_key: str) -> None:
    resource, method, args, kwargs, path, body = case

    async def run() -> None:
        async with AsyncMlsApiClient(api_key=mock_api_key) as client:
            await getattr(_resolve(client, resource), method)(*args, **kwargs)

    with respx.mock(assert_all_called=True) as router:
        route = router.post(BASE + path).mock(
            return_value=httpx.Response(202, json=_response_for(path))
        )
        asyncio.run(run())
        assert json.loads(route.calls.last.request.content) == body


def test_floorplan_analyze_contract(mock_api_key: str) -> None:
    with respx.mock() as router:
        route = router.post(BASE + "/v1/studio/floorplan/analyze").mock(
            return_value=httpx.Response(200, json=FLOORPLAN_RESPONSE)
        )
        with MlsApiClient(api_key=mock_api_key) as client:
            client.studio.floorplan.analyze("https://plan.png")
            client.studio.floorplan.analyze(
                "https://plan.png", style="luxury", mls_id="A1", generate_3d_render=True
            )
        bodies = [json.loads(c.request.content) for c in route.calls]
        assert bodies == [
            {"floorplan_image_url": "https://plan.png"},
            {
                "floorplan_image_url": "https://plan.png",
                "style": "luxury",
                "mls_id": "A1",
                "generate_3d_render": True,
            },
        ]


def test_social_publish_contract(mock_api_key: str) -> None:
    dest = {"platform": "instagram", "target_type": "reels", "caption": "Just listed!"}
    with respx.mock() as router:
        route = router.post(BASE + "/v1/studio/social/publish").mock(
            return_value=httpx.Response(200, json=PUBLISHED)
        )
        with MlsApiClient(api_key=mock_api_key) as client:
            res = client.studio.social.publish(
                "https://cdn.example/reel.mp4",
                destinations=[dest],
                asset_type="video",
                schedule_time="immediate",
                webhook_url=HOOK,
            )
        assert json.loads(route.calls.last.request.content) == {
            "asset_url": "https://cdn.example/reel.mp4",
            "asset_type": "video",
            "destinations": [dest],
            "schedule_time": "immediate",
            "webhook_url": HOOK,
        }
        assert res.publish_id == "pub_abc123"
        assert res.results[0].post_url == "https://instagram.com/p/post_instagram_x1"


# ---------------------------------------------------------------------------
# Deprecated aliases
# ---------------------------------------------------------------------------

DEPRECATED: List[Case] = [
    (
        "studio.staging",
        "restyle",
        (PHOTO,),
        dict(target_style="coastal"),
        "/v1/studio/staging/restyle",
        {"photo_url": PHOTO, "style": "coastal"},
    ),
    (
        "studio.staging",
        "twilight",
        (PHOTO,),
        dict(interior_lighting=True),
        "/v1/studio/staging/twilight",
        {"photo_url": PHOTO},
    ),
    (
        "studio.custom",
        "generate",
        ("p",),
        dict(image_urls=[PHOTO], negative_prompt="people"),
        "/v1/studio/custom",
        {"prompt": "p", "reference_image_urls": [PHOTO]},
    ),
    (
        "studio.render",
        "architectural",
        ("https://cad.png",),
        dict(prompt="add travertine"),
        "/v1/studio/render/architectural",
        {"source_image_url": "https://cad.png", "custom_instructions": "add travertine"},
    ),
    (
        "studio.video",
        "walkthrough",
        (),
        dict(photos=[PHOTO]),
        "/v1/studio/video/walkthrough",
        {"photo_urls": [PHOTO]},
    ),
    (
        "studio.video",
        "walkthrough",
        ([PHOTO],),
        {},
        "/v1/studio/video/walkthrough",
        {"photo_urls": [PHOTO]},
    ),
    (
        "studio.video",
        "tour",
        ([PHOTO, "https://b.jpg"],),
        dict(music_mood="luxurious"),
        "/v1/studio/video/tour",
        {
            "ordered_photos": [
                {"room_name": "Room 1", "photo_url": PHOTO},
                {"room_name": "Room 2", "photo_url": "https://b.jpg"},
            ]
        },
    ),
    (
        "studio.social",
        "publish",
        ("https://img.jpg", ["instagram", "facebook"]),
        dict(caption="Hello"),
        "/v1/studio/social/publish",
        {
            "asset_url": "https://img.jpg",
            "destinations": [
                {"platform": "instagram", "target_type": "feed", "caption": "Hello"},
                {"platform": "facebook", "target_type": "page_post", "caption": "Hello"},
            ],
        },
    ),
]


@pytest.mark.parametrize("case", DEPRECATED, ids=[_case_id(c) for c in DEPRECATED])
def test_deprecated_aliases(case: Case, mock_api_key: str) -> None:
    resource, method, args, kwargs, path, body = case
    with respx.mock() as router:
        route = router.post(BASE + path).mock(
            return_value=httpx.Response(202, json=_response_for(path))
        )
        with MlsApiClient(api_key=mock_api_key) as client:
            with pytest.warns(DeprecationWarning):
                getattr(_resolve(client, resource), method)(*args, **kwargs)
        assert json.loads(route.calls.last.request.content) == body


@pytest.mark.parametrize("case", DEPRECATED, ids=[_case_id(c) for c in DEPRECATED])
def test_deprecated_aliases_async(case: Case, mock_api_key: str) -> None:
    resource, method, args, kwargs, path, body = case

    async def run() -> None:
        async with AsyncMlsApiClient(api_key=mock_api_key) as client:
            with pytest.warns(DeprecationWarning):
                await getattr(_resolve(client, resource), method)(*args, **kwargs)

    with respx.mock() as router:
        route = router.post(BASE + path).mock(
            return_value=httpx.Response(202, json=_response_for(path))
        )
        asyncio.run(run())
        assert json.loads(route.calls.last.request.content) == body


def test_new_name_wins_over_deprecated_alias(mock_api_key: str) -> None:
    with respx.mock() as router:
        route = router.post(BASE + "/v1/studio/staging/restyle").mock(
            return_value=httpx.Response(202, json=SUBMITTED)
        )
        with MlsApiClient(api_key=mock_api_key) as client:
            with pytest.warns(DeprecationWarning):
                client.studio.staging.restyle(PHOTO, style="zen", target_style="coastal")
        assert json.loads(route.calls.last.request.content)["style"] == "zen"


def test_creatives_requires_a_photo_source(mock_api_key: str) -> None:
    with MlsApiClient(api_key=mock_api_key) as client:
        with pytest.raises(ValueError, match="photo_url"):
            client.studio.creatives.generate()


def test_sync_and_async_signatures_match() -> None:
    import inspect

    from pymlsapi.resources.content import AsyncContentResource, ContentResource
    from pymlsapi.resources.studio import (
        creatives,
        custom,
        enhance,
        floorplan,
        render,
        social,
        staging,
        video,
    )

    pairs = [(ContentResource, AsyncContentResource)]
    for mod in (creatives, custom, enhance, floorplan, render, social, staging, video):
        for name, cls in vars(mod).items():
            if (
                name.endswith("Resource")
                and not name.startswith("Async")
                and cls.__module__ == mod.__name__
            ):
                pairs.append((cls, getattr(mod, "Async" + name)))
    assert len(pairs) == 9
    for sync_cls, async_cls in pairs:
        for name, fn in vars(sync_cls).items():
            if name.startswith("_") or not callable(fn):
                continue
            assert inspect.signature(fn) == inspect.signature(getattr(async_cls, name)), name


# ---------------------------------------------------------------------------
# Transport headers / config
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("env", ["live", "test"])
def test_headers_and_base_url(env: str, mock_api_key: str) -> None:
    with respx.mock() as router:
        route = router.get(BASE + "/v1/studio/jobs/job_1").mock(
            return_value=httpx.Response(200, json={"job_id": "job_1", "status": "processing"})
        )
        with MlsApiClient(api_key=mock_api_key, environment=env) as client:
            assert client.config.base_url == BASE
            client.studio.jobs.get("job_1")
        headers = route.calls.last.request.headers
        assert headers["x-key-env"] == env
        assert headers["user-agent"] == f"pymlsapi/{__version__}"
        assert headers["x-api-key"] == mock_api_key


def test_async_headers(mock_api_key: str) -> None:
    async def run() -> None:
        async with AsyncMlsApiClient(api_key=mock_api_key, environment="test") as client:
            await client.studio.jobs.get("job_1")

    with respx.mock() as router:
        route = router.get(BASE + "/v1/studio/jobs/job_1").mock(
            return_value=httpx.Response(200, json={"job_id": "job_1", "status": "processing"})
        )
        asyncio.run(run())
        assert route.calls.last.request.headers["x-key-env"] == "test"


def test_version() -> None:
    import pymlsapi

    assert pymlsapi.__version__ == "0.1.1"
