import httpx
import pytest
import respx

from pymlsapi import AsyncMlsApiClient, BaseListing, IngestJob, MlsApiClient

SAMPLE_LISTING_PAYLOAD = {
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
    "photos": ["https://cdn.mlsapi.dev/photos/sample1.jpg"],
    "photo_count": 1,
}

SAMPLE_JOB_PAYLOAD = {
    "job_id": "job_ingest_999",
    "mls_id": "A12079565",
    "status": "processing",
    "step": "scraping_zillow",
    "status_url": "/jobs/job_ingest_999",
}


@respx.mock
def test_listings_get_immediate_200(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/A12079565").mock(
        return_value=httpx.Response(200, json=SAMPLE_LISTING_PAYLOAD)
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        result = client.listings.get("A12079565")
        assert isinstance(result, BaseListing)
        assert result.mls_id == "A12079565"
        assert result.price == 420000
        assert result.address.city == "North Miami"


@respx.mock
def test_listings_get_enqueued_202(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/A12079565").mock(
        return_value=httpx.Response(202, json=SAMPLE_JOB_PAYLOAD)
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        result = client.listings.get("A12079565")
        assert isinstance(result, IngestJob)
        assert result.job_id == "job_ingest_999"
        assert result.status == "processing"


@respx.mock
def test_listings_get_and_wait(mock_api_key):
    route_listing = respx.get("https://mlsapi.dev/v1/listing/A12079565")
    # First call returns 202, second call (after job completion) returns 200
    route_listing.side_effect = [
        httpx.Response(202, json=SAMPLE_JOB_PAYLOAD),
        httpx.Response(200, json=SAMPLE_LISTING_PAYLOAD),
    ]

    respx.get("https://mlsapi.dev/jobs/job_ingest_999").mock(
        return_value=httpx.Response(200, json={"job_id": "job_ingest_999", "status": "completed"})
    )

    progress_events = []
    with MlsApiClient(api_key=mock_api_key) as client:
        listing = client.listings.get_and_wait(
            "A12079565",
            poll_interval=0.01,
            on_progress=lambda j: progress_events.append(j.status),
        )
        assert isinstance(listing, BaseListing)
        assert listing.mls_id == "A12079565"
        assert "completed" in progress_events


@respx.mock
def test_listings_enqueue_and_jobs(mock_api_key):
    respx.post("https://mlsapi.dev/jobs").mock(
        return_value=httpx.Response(
            202, json={"jobId": "job_123", "status": "queued", "mlsId": "A12079565"}
        )
    )
    respx.get("https://mlsapi.dev/jobs/job_123").mock(
        return_value=httpx.Response(200, json={"jobId": "job_123", "status": "processing"})
    )
    respx.get("https://mlsapi.dev/jobs").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "jobs": [{"jobId": "job_123", "status": "processing"}]}
        )
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        job = client.listings.enqueue("A12079565", download_photos=True)
        assert job.job_id == "job_123"

        status = client.listings.get_job("job_123")
        assert status.status == "processing"

        job_list = client.listings.list_jobs(limit=10)
        assert len(job_list) == 1
        assert job_list[0].job_id == "job_123"


@respx.mock
@pytest.mark.asyncio
async def test_async_listings_get_and_wait(mock_api_key):
    route_listing = respx.get("https://mlsapi.dev/v1/listing/A12079565")
    route_listing.side_effect = [
        httpx.Response(202, json=SAMPLE_JOB_PAYLOAD),
        httpx.Response(200, json=SAMPLE_LISTING_PAYLOAD),
    ]
    respx.get("https://mlsapi.dev/jobs/job_ingest_999").mock(
        return_value=httpx.Response(200, json={"job_id": "job_ingest_999", "status": "completed"})
    )

    async with AsyncMlsApiClient(api_key=mock_api_key) as client:
        listing = await client.listings.get_and_wait("A12079565", poll_interval=0.01)
        assert isinstance(listing, BaseListing)
        assert listing.mls_id == "A12079565"
