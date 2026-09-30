import httpx
import pytest
import respx

from mlsapi import AsyncMlsApiClient, ContentGenerationResponse, MlsApiClient

SAMPLE_CONTENT_PAYLOAD = {
    "mls_id": "A12079565",
    "tone": "luxury",
    "target_audience": "High-net-worth buyers",
    "generated_at": "2026-09-30T12:00:00Z",
    "content": {
        "social": {
            "instagram": {
                "hook_above_fold": "Sun-drenched North Miami sanctuary ✨",
                "caption": "Experience resort-style living with waterfront serenity...",
                "call_to_action": "DM for private tour",
                "hashtags": ["#MiamiRealEstate", "#LuxuryLiving"],
                "character_count": 312,
            },
            "linkedin": {
                "post_copy": "Prime turn-key investment offering 7.0% gross yield in Miami-Dade County.",
                "hashtags": ["#RealEstateInvesting", "#PropTech"],
            },
        },
        "video_script": {
            "duration_seconds": 30,
            "format": "vertical_9_16",
            "hook": "Would you live in this renovated Miami condo for under $450K?",
            "scenes": [
                {
                    "second_range": "0-3s",
                    "visual": "Exterior panning shot",
                    "voiceover": "Welcome home.",
                }
            ],
        },
        "flyer_bullets": ["Fully renovated kitchen", "Impact windows throughout"],
        "mls_remarks": "Remarkable 2-bed 2-bath corner unit with floor-to-ceiling glass.",
    },
}


@respx.mock
def test_content_generation_sync(mock_api_key):
    respx.post("https://mlsapi.dev/v1/listing/A12079565/content").mock(
        return_value=httpx.Response(200, json=SAMPLE_CONTENT_PAYLOAD)
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        copy = client.content.generate(
            "A12079565",
            outputs=["social", "video_script", "mls_remarks"],
            tone="luxury",
            social_platforms=["instagram", "linkedin"],
        )
        assert isinstance(copy, ContentGenerationResponse)
        assert copy.mls_id == "A12079565"
        assert copy.content.social.instagram.caption.startswith("Experience resort-style")
        assert copy.content.video_script.duration_seconds == 30
        assert len(copy.content.flyer_bullets) == 2


@respx.mock
@pytest.mark.asyncio
async def test_content_generation_async(mock_api_key):
    respx.post("https://mlsapi.dev/v1/listing/A12079565/content").mock(
        return_value=httpx.Response(200, json=SAMPLE_CONTENT_PAYLOAD)
    )

    async with AsyncMlsApiClient(api_key=mock_api_key) as client:
        copy = await client.content.generate("A12079565", tone="luxury")
        assert copy.content.mls_remarks.startswith("Remarkable 2-bed")
