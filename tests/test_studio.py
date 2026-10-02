import httpx
import respx

from pymlsapi import (
    AdCreativesResult,
    DeclutterResult,
    DeStageEmptyResult,
    ExteriorEnhanceResult,
    FloorPlanAnalysisResponse,
    MlsApiClient,
    Render3dResult,
    ReplaceFurnitureResult,
    ReplaceMaterialResult,
    RestyleResult,
    SocialPublishResult,
    StagingResult,
    TwilightResult,
    UploadResult,
    UpscaleResult,
    VideoEnhanceResult,
    WallColorsResult,
)


@respx.mock
def test_staging_stage_and_wait(mock_api_key):
    respx.post("https://mlsapi.dev/v1/studio/staging/stage").mock(
        return_value=httpx.Response(202, json={"job_id": "job_stage_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_stage_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_stage_1",
                "status": "completed",
                "result": {
                    "staged_photo_url": "https://cdn.mlsapi.dev/output/staged.jpg",
                    "before_after_comparison_url": "https://cdn.mlsapi.dev/output/slider.html",
                    "staging_manifest": ["Bouclé sofa", "Coffee table"],
                },
            },
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        res = client.studio.staging.stage_and_wait(
            photo_url="https://cdn.mlsapi.dev/uploads/vacant.jpg",
            room_type="living_room",
            style="scandinavian",
            poll_interval=0.01,
        )
        assert isinstance(res, StagingResult)
        assert res.staged_photo_url == "https://cdn.mlsapi.dev/output/staged.jpg"
        assert len(res.staging_manifest) == 2


@respx.mock
def test_staging_declutter_and_wait(mock_api_key):
    respx.post("https://mlsapi.dev/v1/studio/staging/declutter").mock(
        return_value=httpx.Response(202, json={"job_id": "job_dec_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_dec_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_dec_1",
                "status": "completed",
                "result": {
                    "decluttered_photo_url": "https://cdn.mlsapi.dev/output/clean.jpg",
                    "items_removed": ["boxes", "wires"],
                },
            },
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        res = client.studio.staging.declutter_and_wait(
            photo_url="https://cdn.mlsapi.dev/uploads/messy.jpg",
            removal_targets=["boxes"],
            poll_interval=0.01,
        )
        assert isinstance(res, DeclutterResult)
        assert res.decluttered_photo_url == "https://cdn.mlsapi.dev/output/clean.jpg"


@respx.mock
def test_staging_empty_restyle_furniture_material_wallcolors_twilight(mock_api_key):
    # Empty
    respx.post("https://mlsapi.dev/v1/studio/staging/empty").mock(
        return_value=httpx.Response(202, json={"job_id": "job_emp_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_emp_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_emp_1",
                "status": "completed",
                "result": {"empty_photo_url": "https://cdn.mlsapi.dev/empty.jpg"},
            },
        )
    )

    # Restyle
    respx.post("https://mlsapi.dev/v1/studio/staging/restyle").mock(
        return_value=httpx.Response(202, json={"job_id": "job_res_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_res_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_res_1",
                "status": "completed",
                "result": {"restyled_photo_url": "https://cdn.mlsapi.dev/restyled.jpg"},
            },
        )
    )

    # Replace furniture
    respx.post("https://mlsapi.dev/v1/studio/staging/replace-furniture").mock(
        return_value=httpx.Response(202, json={"job_id": "job_fur_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_fur_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_fur_1",
                "status": "completed",
                "result": {"result_photo_url": "https://cdn.mlsapi.dev/sofa.jpg"},
            },
        )
    )

    # Replace material
    respx.post("https://mlsapi.dev/v1/studio/staging/replace-material").mock(
        return_value=httpx.Response(202, json={"job_id": "job_mat_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_mat_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_mat_1",
                "status": "completed",
                "result": {"result_photo_url": "https://cdn.mlsapi.dev/counter.jpg"},
            },
        )
    )

    # Wall colors
    respx.post("https://mlsapi.dev/v1/studio/staging/wall-colors").mock(
        return_value=httpx.Response(202, json={"job_id": "job_wall_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_wall_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_wall_1",
                "status": "completed",
                "result": {
                    "comparison_grid_3x3_url": "https://cdn.mlsapi.dev/grid.jpg",
                    "swatch_results": [
                        {
                            "color_name": "Alabaster",
                            "hex": "#F2F0EB",
                            "image_url": "https://cdn.mlsapi.dev/s1.jpg",
                        }
                    ],
                },
            },
        )
    )

    # Twilight
    respx.post("https://mlsapi.dev/v1/studio/staging/twilight").mock(
        return_value=httpx.Response(202, json={"job_id": "job_twi_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_twi_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_twi_1",
                "status": "completed",
                "result": {"enhanced_photo_url": "https://cdn.mlsapi.dev/dusk.jpg"},
            },
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        emp = client.studio.staging.empty_and_wait("https://img.jpg", poll_interval=0.01)
        assert isinstance(emp, DeStageEmptyResult)

        res = client.studio.staging.restyle_and_wait("https://img.jpg", poll_interval=0.01)
        assert isinstance(res, RestyleResult)

        fur = client.studio.staging.replace_furniture_and_wait(
            "https://img.jpg", target_furniture="sofa", poll_interval=0.01
        )
        assert isinstance(fur, ReplaceFurnitureResult)

        mat = client.studio.staging.replace_material_and_wait(
            "https://img.jpg", surface_type="countertops", poll_interval=0.01
        )
        assert isinstance(mat, ReplaceMaterialResult)

        wall = client.studio.staging.wall_colors_and_wait("https://img.jpg", poll_interval=0.01)
        assert isinstance(wall, WallColorsResult)

        twi = client.studio.staging.twilight_and_wait("https://img.jpg", poll_interval=0.01)
        assert isinstance(twi, TwilightResult)


@respx.mock
def test_enhance_exterior_and_upscale(mock_api_key):
    respx.post("https://mlsapi.dev/v1/studio/enhance/exterior").mock(
        return_value=httpx.Response(202, json={"job_id": "job_ext_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_ext_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_ext_1",
                "status": "completed",
                "result": {"enhanced_photo_url": "https://cdn.mlsapi.dev/ext.jpg"},
            },
        )
    )

    respx.post("https://mlsapi.dev/v1/studio/enhance/upscale").mock(
        return_value=httpx.Response(202, json={"job_id": "job_up_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_up_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_up_1",
                "status": "completed",
                "result": {
                    "upscaled_image_url": "https://cdn.mlsapi.dev/4k.jpg",
                    "scale_factor": 4,
                },
            },
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        ext = client.studio.enhance.exterior_and_wait("https://img.jpg", poll_interval=0.01)
        assert isinstance(ext, ExteriorEnhanceResult)

        up = client.studio.enhance.upscale_and_wait(
            "https://img.jpg", scale_factor=4, poll_interval=0.01
        )
        assert isinstance(up, UpscaleResult)


@respx.mock
def test_floorplan_analyze_and_render3d(mock_api_key):
    respx.post("https://mlsapi.dev/v1/studio/floorplan/analyze").mock(
        return_value=httpx.Response(
            200,
            json={
                "spatial_summary": {"total_rooms_detected": 5, "stories": 1},
                "rooms": [{"name": "Living Room"}],
                "isometric_3d_prompt": "Cutaway 3D dollhouse model",
            },
        )
    )

    respx.post("https://mlsapi.dev/v1/studio/floorplan/render-3d").mock(
        return_value=httpx.Response(202, json={"job_id": "job_3d_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_3d_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_3d_1",
                "status": "completed",
                "result": {
                    "isometric_3d_dollhouse_url": "https://cdn.mlsapi.dev/3d.png",
                    "room_renders": [
                        {"room_name": "Living Room", "image_url": "https://cdn.mlsapi.dev/lr.png"}
                    ],
                },
            },
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        analysis = client.studio.floorplan.analyze("https://floorplan.png")
        assert isinstance(analysis, FloorPlanAnalysisResponse)
        assert analysis.spatial_summary.total_rooms_detected == 5

        dollhouse = client.studio.floorplan.render_3d_and_wait(
            "https://floorplan.png", poll_interval=0.01
        )
        assert isinstance(dollhouse, Render3dResult)
        assert dollhouse.isometric_3d_dollhouse_url == "https://cdn.mlsapi.dev/3d.png"


@respx.mock
def test_creatives_social_video_upload(mock_api_key):
    # Creatives
    respx.post("https://mlsapi.dev/v1/studio/creatives/generate").mock(
        return_value=httpx.Response(202, json={"job_id": "job_cr_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_cr_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_cr_1",
                "status": "completed",
                "result": {
                    "mls_id": "A12079565",
                    "creatives": {
                        "square": {
                            "placement": "square",
                            "image_url": "https://cdn.mlsapi.dev/sq.jpg",
                        }
                    },
                    "compliance": {"fair_housing_passed": True},
                },
            },
        )
    )

    # Social publish
    respx.post("https://mlsapi.dev/v1/studio/social/publish").mock(
        return_value=httpx.Response(
            200, json={"status": "published", "destinations_dispatched": ["instagram"]}
        )
    )

    # Video polish
    respx.post("https://mlsapi.dev/v1/studio/video/enhance").mock(
        return_value=httpx.Response(202, json={"job_id": "job_vid_1", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/v1/studio/jobs/job_vid_1").mock(
        return_value=httpx.Response(
            200,
            json={
                "job_id": "job_vid_1",
                "status": "completed",
                "result": {
                    "mastered_videos": [
                        {"aspect_ratio": "9:16", "url": "https://cdn.mlsapi.dev/reel.mp4"}
                    ]
                },
            },
        )
    )

    # Upload
    respx.post("https://mlsapi.dev/v1/studio/upload").mock(
        return_value=httpx.Response(200, json={"url": "https://cdn.mlsapi.dev/uploads/test.jpg"})
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        ads = client.studio.creatives.generate_and_wait("A12079565", poll_interval=0.01)
        assert isinstance(ads, AdCreativesResult)
        assert ads.compliance.fair_housing_passed is True

        soc = client.studio.social.publish(
            "https://img.jpg",
            destinations=[{"platform": "instagram", "target_type": "feed"}],
            asset_type="image",
        )
        assert isinstance(soc, SocialPublishResult)
        assert soc.status == "published"

        vid = client.studio.video.enhance_and_wait("https://raw.mp4", poll_interval=0.01)
        assert isinstance(vid, VideoEnhanceResult)
        assert vid.mastered_videos[0].url.endswith("reel.mp4")

        upl = client.studio.upload(b"fake_jpeg_binary_data", filename="test.jpg")
        assert isinstance(upl, UploadResult)
        assert upl.url == "https://cdn.mlsapi.dev/uploads/test.jpg"
