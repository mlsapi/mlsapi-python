from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.requests import SocialPublishDestination
from pymlsapi.models.studio import SocialPublishResult
from pymlsapi.resources._params import compact, warn_deprecated

PUBLISH_PATH = "/v1/studio/social/publish"

# Used only to upgrade the deprecated `destinations=["instagram", ...]` form.
_DEFAULT_TARGET_TYPE = {
    "instagram": "feed",
    "facebook": "page_post",
    "youtube": "shorts",
    "linkedin": "feed",
    "tiktok": "feed",
}


def _publish_body(
    asset_url: str,
    destinations: Sequence[Union[SocialPublishDestination, Mapping[str, Any], str]],
    asset_type: Optional[str],
    schedule_time: Optional[str],
    webhook_url: Optional[str],
    caption: Optional[str],
) -> Dict[str, Any]:
    normalized: List[Dict[str, Any]] = []
    warned_strings = False
    for dest in destinations:
        if isinstance(dest, str):
            if not warned_strings:
                warn_deprecated(
                    "destinations as a list of platform names",
                    "a list of {'platform': ..., 'target_type': ...} dicts",
                    stacklevel=4,
                )
                warned_strings = True
            normalized.append(
                {"platform": dest, "target_type": _DEFAULT_TARGET_TYPE.get(dest, "feed")}
            )
        else:
            normalized.append(dict(dest))
    if caption is not None:
        warn_deprecated(
            "caption",
            "a per-destination 'caption'",
            note="The top-level caption is copied into destinations that lack one.",
            stacklevel=4,
        )
        for dest_dict in normalized:
            dest_dict.setdefault("caption", caption)
    return compact(
        asset_url=asset_url,
        asset_type=asset_type,
        destinations=normalized,
        schedule_time=schedule_time,
        webhook_url=webhook_url,
    )


class SocialResource:
    """Synchronous direct social network publishing operations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def publish(
        self,
        asset_url: str,
        destinations: Sequence[Union[SocialPublishDestination, Mapping[str, Any], str]],
        *,
        asset_type: Optional[str] = None,
        schedule_time: Optional[str] = None,
        webhook_url: Optional[str] = None,
        caption: Optional[str] = None,
    ) -> SocialPublishResult:
        """Publish an image or video to social destinations. ``POST /v1/studio/social/publish``.

        ``destinations`` is a list of dicts such as
        ``{"platform": "instagram", "target_type": "reels", "caption": "..."}``.
        Plain platform-name strings and the top-level ``caption`` are deprecated.
        """
        payload = _publish_body(
            asset_url, destinations, asset_type, schedule_time, webhook_url, caption
        )
        data = self._http.post(PUBLISH_PATH, json=payload)
        return SocialPublishResult.model_validate(data)


class AsyncSocialResource:
    """Asynchronous direct social network publishing operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def publish(
        self,
        asset_url: str,
        destinations: Sequence[Union[SocialPublishDestination, Mapping[str, Any], str]],
        *,
        asset_type: Optional[str] = None,
        schedule_time: Optional[str] = None,
        webhook_url: Optional[str] = None,
        caption: Optional[str] = None,
    ) -> SocialPublishResult:
        """Publish an image or video to social destinations. ``POST /v1/studio/social/publish``.

        ``destinations`` is a list of dicts such as
        ``{"platform": "instagram", "target_type": "reels", "caption": "..."}``.
        Plain platform-name strings and the top-level ``caption`` are deprecated.
        """
        payload = _publish_body(
            asset_url, destinations, asset_type, schedule_time, webhook_url, caption
        )
        data = await self._http.post(PUBLISH_PATH, json=payload)
        return SocialPublishResult.model_validate(data)
