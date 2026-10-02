from __future__ import annotations

from typing import List, Optional
from urllib.parse import quote

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.content import ContentGenerationResponse
from pymlsapi.models.requests import ContentPropertyDetails
from pymlsapi.resources._params import compact


class ContentResource:
    """Synchronous context-aware marketing copy generation operations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def generate(
        self,
        mls_id: str,
        outputs: Optional[List[str]] = None,
        tone: Optional[str] = None,
        social_platforms: Optional[List[str]] = None,
        target_audience: Optional[str] = None,
        custom_notes: Optional[str] = None,
        property_details: Optional[ContentPropertyDetails] = None,
    ) -> ContentGenerationResponse:
        """Generate context-aware marketing copy across social channels, video scripts, and email."""
        payload = compact(
            outputs=outputs,
            social_platforms=social_platforms,
            tone=tone,
            target_audience=target_audience,
            custom_notes=custom_notes,
            property_details=property_details,
        )

        data = self._http.post(f"/v1/listing/{quote(mls_id, safe='')}/content", json=payload)
        return ContentGenerationResponse.model_validate(data)


class AsyncContentResource:
    """Asynchronous context-aware marketing copy generation operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def generate(
        self,
        mls_id: str,
        outputs: Optional[List[str]] = None,
        tone: Optional[str] = None,
        social_platforms: Optional[List[str]] = None,
        target_audience: Optional[str] = None,
        custom_notes: Optional[str] = None,
        property_details: Optional[ContentPropertyDetails] = None,
    ) -> ContentGenerationResponse:
        """Generate context-aware marketing copy across social channels, video scripts, and email."""
        payload = compact(
            outputs=outputs,
            social_platforms=social_platforms,
            tone=tone,
            target_audience=target_audience,
            custom_notes=custom_notes,
            property_details=property_details,
        )

        data = await self._http.post(f"/v1/listing/{quote(mls_id, safe='')}/content", json=payload)
        return ContentGenerationResponse.model_validate(data)
