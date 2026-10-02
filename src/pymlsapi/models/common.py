from __future__ import annotations

from enum import Enum


class InteriorStyle(str, Enum):
    MODERN = "modern"
    LUXURY = "luxury"
    SCANDINAVIAN = "scandinavian"
    JAPANDI = "japandi"
    INDUSTRIAL = "industrial"
    BOHEMIAN = "bohemian"
    MINIMALIST = "minimalist"
    COASTAL = "coastal"
    MID_CENTURY_MODERN = "mid_century_modern"
    ART_DECO = "art_deco"
    FARMHOUSE = "farmhouse"
    MEDITERRANEAN = "mediterranean"
    CONTEMPORARY = "contemporary"
    RUSTIC = "rustic"
    TRANSITIONAL = "transitional"
    FRENCH_COUNTRY = "french_country"
    HOLLYWOOD_REGENCY = "hollywood_regency"
    ECLECTIC = "eclectic"
    ZEN = "zen"
    BAUHAUS = "bauhaus"
    VICTORIAN = "victorian"
    TROPICAL = "tropical"
    MODERN_CRAFTSMAN = "modern_craftsman"
    SOUTHWESTERN = "southwestern"
    WABI_SABI = "wabi_sabi"
    SHABBY_CHIC = "shabby_chic"
    CHALET = "chalet"
    URBAN_LOFT = "urban_loft"
    CUSTOM = "custom"


class RoomType(str, Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    PRIMARY_BEDROOM = "primary_bedroom"
    DINING_ROOM = "dining_room"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    PATIO = "patio"
    OUTDOOR_PATIO = "outdoor_patio"
    HOME_OFFICE = "home_office"
    ENTRYWAY = "entryway"
    BASEMENT = "basement"
    COMMERCIAL_LOBBY = "commercial_lobby"


class SocialPlatform(str, Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    X_TWITTER = "x_twitter"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
