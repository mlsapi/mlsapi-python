"""Typed shapes for nested request objects (mirrors the JS SDK request types).

These are ``TypedDict``s, so plain dict literals work everywhere they are accepted.
"""

from __future__ import annotations

from typing import List, TypedDict, Union


class WallColorSwatch(TypedDict):
    name: str
    hex: str


class _HouseTourRoomItemRequired(TypedDict):
    room_name: str
    photo_url: str


class HouseTourRoomItem(_HouseTourRoomItemRequired, total=False):
    highlight: str


class _SocialPublishDestinationRequired(TypedDict):
    platform: str  # "instagram" | "facebook" | "youtube" | "linkedin" | "tiktok"
    target_type: str  # "feed" | "reels" | "story" | "page_post" | "shorts"


class SocialPublishDestination(_SocialPublishDestinationRequired, total=False):
    caption: str
    title: str
    page_id: str
    share_to_feed: bool


class CreativeBrandKit(TypedDict, total=False):
    agent_name: str
    title: str
    brokerage_name: str
    phone: str
    license_number: str
    agent_headshot_url: str
    realtor_photo: str
    brokerage_logo_url: str
    primary_brand_color: str
    accent_brand_color: str


class OpenHouse(TypedDict):
    day: str
    time: str


class CreativesPropertyDetails(TypedDict, total=False):
    address: str
    price: Union[int, float, str]
    beds: Union[int, float]
    baths: Union[int, float]
    sqft: Union[int, float]
    key_features: List[str]
    property_type: str


class VideoEnhanceFeatures(TypedDict, total=False):
    studio_voice: bool
    animated_subtitles: bool
    smart_reframe: bool
    b_roll_photo_insertion: bool


class SubtitleStyle(TypedDict, total=False):
    font_theme: str  # "hormozi_bold" | "clean_minimal" | "luxury_serif"
    primary_color: str
    highlight_color: str
    safe_zone: str  # "instagram_reels" | "tiktok" | "youtube_shorts"


class ContentPropertyDetails(TypedDict, total=False):
    address: str
    city: str
    state: str
    price: Union[int, float]
    beds: Union[int, float]
    baths: Union[int, float]
    sqft: Union[int, float]
    property_type: str
    year_built: int
    description: str
    highlights: List[str]
