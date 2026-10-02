import httpx
import pytest
import respx

from pymlsapi import AsyncMlsApiClient, MlsApiClient, PropertyIntelligence

SAMPLE_INTELLIGENCE_PAYLOAD = {
    "mls_id": "A12079565",
    "summary": {"address": "1650 NE 135th St Apt 304", "listing_price": 420000},
    "public_records": {"tax_assessment": {"annual_tax_amount": 3820}},
    "llm_derived_intelligence": {
        "systems_and_capex": {
            "roof": {
                "age_years": 8,
                "condition": "good",
                "estimated_replacement_horizon": "12-15 years",
            },
            "hvac": {"age_years": 4, "condition": "excellent"},
            "storm_protection": {"has_impact_windows": True, "has_impact_doors": True},
        },
        "investor_insights": {
            "estimated_monthly_rent": {"low": 2200, "median": 2450, "high": 2700},
            "estimated_gross_yield_pct": 7.0,
            "hoa_present": True,
            "rental_restrictions": "Rent allowed after 1 year ownership",
        },
        "financial_flags": [
            {
                "type": "hoa_reserve",
                "severity": "low",
                "summary": "Healthy reserves",
                "explanation": "Building passed 40-year recertification",
            }
        ],
        "property_strengths": ["Impact windows", "Updated AC"],
        "watch_items": ["HOA approval wait period"],
    },
    "generated_at": "2026-09-30T12:00:00Z",
}


@respx.mock
def test_intelligence_get_sync(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/A12079565/intelligence").mock(
        return_value=httpx.Response(200, json=SAMPLE_INTELLIGENCE_PAYLOAD)
    )

    with MlsApiClient(api_key=mock_api_key) as client:
        intel = client.intelligence.get("A12079565", include_llm=True, investor_mode=True)
        assert isinstance(intel, PropertyIntelligence)
        assert intel.mls_id == "A12079565"
        assert intel.llm_derived_intelligence is not None
        assert intel.llm_derived_intelligence.systems_and_capex.roof.age_years == 8
        assert intel.llm_derived_intelligence.investor_insights.estimated_gross_yield_pct == 7.0
        assert (
            intel.llm_derived_intelligence.systems_and_capex.storm_protection.has_impact_windows
            is True
        )


@respx.mock
@pytest.mark.asyncio
async def test_intelligence_get_async(mock_api_key):
    respx.get("https://mlsapi.dev/v1/listing/A12079565/intelligence").mock(
        return_value=httpx.Response(200, json=SAMPLE_INTELLIGENCE_PAYLOAD)
    )

    async with AsyncMlsApiClient(api_key=mock_api_key) as client:
        intel = await client.intelligence.get("A12079565")
        assert intel.mls_id == "A12079565"
        assert (
            intel.llm_derived_intelligence.investor_insights.estimated_monthly_rent.median == 2450
        )
