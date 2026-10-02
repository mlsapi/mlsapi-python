from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SystemCondition(BaseModel):
    age_years: Optional[int] = None
    material: Optional[str] = None
    condition: Optional[str] = None
    estimated_replacement_horizon: Optional[str] = None
    confidence: Optional[float] = None


class StormProtection(BaseModel):
    has_impact_windows: bool = False
    has_impact_doors: bool = False
    insurance_premium_impact: Optional[str] = None


class SystemsAndCapex(BaseModel):
    roof: Optional[SystemCondition] = None
    hvac: Optional[SystemCondition] = None
    water_heater: Optional[SystemCondition] = None
    appliances: Optional[Dict[str, Any]] = None
    storm_protection: Optional[StormProtection] = None


class RentRange(BaseModel):
    low: float = 0.0
    median: float = 0.0
    high: float = 0.0


class InvestorInsights(BaseModel):
    estimated_monthly_rent: RentRange = Field(default_factory=RentRange)
    estimated_gross_yield_pct: float = 0.0
    hoa_present: bool = False
    rental_restrictions: Optional[str] = None
    tenant_suitability: Optional[str] = None


class FinancialFlag(BaseModel):
    type: str
    severity: str
    summary: str
    explanation: str


class LlmIntelligence(BaseModel):
    systems_and_capex: SystemsAndCapex = Field(default_factory=SystemsAndCapex)
    investor_insights: InvestorInsights = Field(default_factory=InvestorInsights)
    financial_flags: List[FinancialFlag] = Field(default_factory=list)
    property_strengths: List[str] = Field(default_factory=list)
    watch_items: List[str] = Field(default_factory=list)


class PropertyIntelligence(BaseModel):
    mls_id: str
    parcel_id: Optional[str] = None
    summary: Dict[str, Any] = Field(default_factory=dict)
    public_records: Dict[str, Any] = Field(default_factory=dict)
    llm_derived_intelligence: Optional[LlmIntelligence] = None
    generated_at: Optional[str] = None
