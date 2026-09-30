from __future__ import annotations

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.intelligence import PropertyIntelligence


class IntelligenceResource:
    """Synchronous property intelligence and CapEx operations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(
        self,
        mls_id: str,
        include_llm: bool = True,
        investor_mode: bool = False,
    ) -> PropertyIntelligence:
        """Synthesize public records, tax assessment history, and structural CapEx lifespan analysis."""
        params = {
            "include_llm": str(include_llm).lower(),
            "investor_mode": str(investor_mode).lower(),
        }
        data = self._http.get(f"/v1/listing/{mls_id}/intelligence", params=params)
        return PropertyIntelligence.model_validate(data)


class AsyncIntelligenceResource:
    """Asynchronous property intelligence and CapEx operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get(
        self,
        mls_id: str,
        include_llm: bool = True,
        investor_mode: bool = False,
    ) -> PropertyIntelligence:
        """Synthesize public records, tax assessment history, and structural CapEx lifespan analysis."""
        params = {
            "include_llm": str(include_llm).lower(),
            "investor_mode": str(investor_mode).lower(),
        }
        data = await self._http.get(f"/v1/listing/{mls_id}/intelligence", params=params)
        return PropertyIntelligence.model_validate(data)
