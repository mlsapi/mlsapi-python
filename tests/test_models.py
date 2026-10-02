from pymlsapi.models import (
    BaseListing,
    InteriorStyle,
    RoomType,
    StagingResult,
    StudioJob,
)


def test_interior_styles_presets():
    assert InteriorStyle.SCANDINAVIAN.value == "scandinavian"
    assert InteriorStyle.LUXURY.value == "luxury"
    assert RoomType.LIVING_ROOM.value == "living_room"
    assert len(InteriorStyle) == 29
    assert len(RoomType) == 12


def test_base_listing_validation():
    data = {
        "mls_id": "A12079565",
        "status": "for_sale",
        "price": 420000,
        "currency": "USD",
        "address": {
            "street": "1650 NE 135th St Apt 304",
            "city": "North Miami",
            "state": "FL",
            "zip": "33181",
            "formatted": "1650 NE 135th St Apt 304, North Miami, FL 33181",
        },
        "specifications": {
            "beds": 2,
            "baths_full": 2.0,
            "baths_half": 0.0,
            "sqft": 1045,
            "property_type": "Condo",
        },
        "photos": ["https://cdn.mlsapi.dev/photos/sample.jpg"],
        "photo_count": 1,
    }
    listing = BaseListing.model_validate(data)
    assert listing.mls_id == "A12079565"
    assert listing.price == 420000
    assert listing.specifications.beds == 2
    assert listing.photo_count == 1


def test_studio_job_and_result():
    job_data = {
        "job_id": "job_stage_123",
        "status": "completed",
        "progress_percentage": 100,
        "result": {
            "staged_photo_url": "https://cdn.mlsapi.dev/output/staged.jpg",
            "before_after_comparison_url": "https://cdn.mlsapi.dev/output/slider.html",
            "staging_manifest": ["Bouclé sofa", "Marble table"],
        },
    }
    job = StudioJob.model_validate(job_data)
    assert job.status == "completed"
    assert job.progress_percentage == 100
    result = StagingResult.model_validate(job.result)
    assert result.staged_photo_url == "https://cdn.mlsapi.dev/output/staged.jpg"
    assert len(result.staging_manifest) == 2
