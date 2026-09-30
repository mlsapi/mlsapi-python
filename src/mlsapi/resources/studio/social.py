from __future__ import annotations

from typing import Any, Dict, List, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.models.studio import SocialPublishResult


class SocialResource:
    """Synchronous direct social network publishing operations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def publish(
        self,
        asset_url: str,
        destinations: List[str],
        caption: Optional[str] = None,
        schedule_time: Optional[str] = None,
    ) -> SocialPublishResult:
        payload: Dict[str, Any] = {
            "asset_url": asset_url,
            "destinations": destinations,
        }
        if caption:
            payload["caption"] = caption
        if schedule_time:
            payload["schedule_time"] = schedule_time
        data = self._http.post("/v1/studio/social/publish", json=payload)
        return SocialPublishResult.model_validate(data)


class AsyncSocialResource:
    """Asynchronous direct social network publishing operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def publish(
        self,
        asset_url: str,
        destinations: List[str],
        caption: Optional[str] = None,
        schedule_time: Optional[str] = None,
    ) -> SocialPublishResult:
        payload: Dict[str, Any] = {
            "asset_url": asset_url,
            "destinations": destinations,
        }
        if caption:
            payload["caption"] = caption
        if schedule_time:
            payload["schedule_time"] = schedule_time
        data = await self._http.post("/v1/studio/social/publish", json=payload)
        return SocialPublishResult.model_validate(data)
