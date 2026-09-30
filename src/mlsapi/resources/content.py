from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.content import ContentGenerationResponse


class ContentResource:
    """Synchronous context-aware marketing copy generation operations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def generate(
        self,
        mls_id: str,
        outputs: Optional[List[str]] = None,
        tone: str = "luxury",
        social_platforms: Optional[List[str]] = None,
        target_audience: Optional[str] = None,
        custom_notes: Optional[str] = None,
        property_details: Optional[Dict[str, Any]] = None,
    ) -> ContentGenerationResponse:
        """Generate context-aware marketing copy across social channels, video scripts, and email."""
        payload: Dict[str, Any] = {
            "outputs": outputs
            or ["social", "email_blast", "video_script", "flyer_bullets", "mls_remarks"],
            "tone": tone,
        }
        if social_platforms:
            payload["social_platforms"] = social_platforms
        if target_audience:
            payload["target_audience"] = target_audience
        if custom_notes:
            payload["custom_notes"] = custom_notes
        if property_details:
            payload["property_details"] = property_details

        data = self._http.post(f"/v1/listing/{mls_id}/content", json=payload)
        return ContentGenerationResponse.model_validate(data)


class AsyncContentResource:
    """Asynchronous context-aware marketing copy generation operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def generate(
        self,
        mls_id: str,
        outputs: Optional[List[str]] = None,
        tone: str = "luxury",
        social_platforms: Optional[List[str]] = None,
        target_audience: Optional[str] = None,
        custom_notes: Optional[str] = None,
        property_details: Optional[Dict[str, Any]] = None,
    ) -> ContentGenerationResponse:
        """Generate context-aware marketing copy across social channels, video scripts, and email."""
        payload: Dict[str, Any] = {
            "outputs": outputs
            or ["social", "email_blast", "video_script", "flyer_bullets", "mls_remarks"],
            "tone": tone,
        }
        if social_platforms:
            payload["social_platforms"] = social_platforms
        if target_audience:
            payload["target_audience"] = target_audience
        if custom_notes:
            payload["custom_notes"] = custom_notes
        if property_details:
            payload["property_details"] = property_details

        data = await self._http.post(f"/v1/listing/{mls_id}/content", json=payload)
        return ContentGenerationResponse.model_validate(data)
