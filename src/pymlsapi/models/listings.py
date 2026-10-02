from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str
    county: Optional[str] = None
    country: Optional[str] = None
    formatted: str


class Coordinates(BaseModel):
    latitude: float
    longitude: float


class PropertySpecifications(BaseModel):
    beds: int
    baths_full: float
    baths_half: float = 0.0
    sqft: int
    lot_sqft: Optional[int] = None
    year_built: Optional[int] = None
    stories: Optional[int] = None
    property_type: str
    parking_spaces: Optional[int] = None
    garage: Optional[bool] = None


class PropertyFeatures(BaseModel):
    heating: List[str] = Field(default_factory=list)
    cooling: List[str] = Field(default_factory=list)
    appliances: List[str] = Field(default_factory=list)
    flooring: List[str] = Field(default_factory=list)
    roof_type: Optional[str] = None
    water_source: Optional[str] = None
    sewer: Optional[str] = None
    view: List[str] = Field(default_factory=list)


class AgentInfo(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    license: Optional[str] = None
    brokerage: Optional[str] = None


class ListingMetadata(BaseModel):
    days_on_market: Optional[int] = None
    listed_date: Optional[str] = None
    mls_board: Optional[str] = None
    updated_at: Optional[str] = None


class BaseListing(BaseModel):
    source: str = "cache"
    mls_id: str
    status: str
    price: float
    currency: str = "USD"
    price_per_sqft: Optional[float] = None
    address: Address
    coordinates: Optional[Coordinates] = None
    specifications: PropertySpecifications
    features: PropertyFeatures = Field(default_factory=PropertyFeatures)
    photos: List[str] = Field(default_factory=list)
    photo_count: int = 0
    agent: Optional[AgentInfo] = None
    description: str = ""
    meta: Optional[ListingMetadata] = None


class IngestJob(BaseModel):
    job_id: Optional[str] = Field(None, alias="jobId")
    mls_id: Optional[str] = Field(None, alias="mlsId")
    status: str
    step: Optional[str] = None
    status_url: Optional[str] = Field(None, alias="statusUrl")
    lookup_url: Optional[str] = Field(None, alias="lookupUrl")
    progress_percentage: Optional[int] = 0
    error: Optional[str] = None
    result: Optional[Any] = None

    model_config = ConfigDict(populate_by_name=True)
