from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Literal, Optional, List
from pydantic import BaseModel, Field


class TrendLabel(str, Enum):
    DEESCALATING = "de-escalating"
    STABLE = "stable"
    ESCALATING = "escalating"


# Risk band enum matching API contract
class RiskBand(str, Enum):
    LOW = "low"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"


class SourceEvidence(BaseModel):
    source_id: str = Field(..., description="Unique source identifier")
    source_name: str
    source_type: Literal["official", "newswire", "media", "ngo", "social", "intel"] = "media"
    reliability: float = Field(ge=0.0, le=1.0, description="Source reliability weight")
    url: Optional[str] = None
    published_at: datetime
    confirmation_group: Optional[str] = Field(
        default=None,
        description="ID shared by independently confirming sources",
    )


class SignalEvent(BaseModel):
    event_id: str
    country_code: str = Field(..., min_length=2, max_length=3)
    occurred_at: datetime
    reported_at: datetime
    status: Literal["reported", "confirmed"] = "reported"
    # Category scores (0-1)
    military: float = Field(0.0, ge=0.0, le=1.0)
    political: float = Field(0.0, ge=0.0, le=1.0)
    conflict: float = Field(0.0, ge=0.0, le=1.0)
    economic: float = Field(0.0, ge=0.0, le=1.0)
    credibility: float = Field(0.0, ge=0.0, le=1.0)
    spillover: float = Field(0.0, ge=0.0, le=1.0)
    evidence: list[SourceEvidence] = Field(default_factory=list)
    viral_unverified_penalty: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Penalty strength when event is viral but unverified",
    )


class Driver(BaseModel):
    """A risk driver with impact and direction."""
    key: str = Field(..., description="Driver identifier")
    label: str = Field(..., description="Human-readable label")
    impact: float = Field(..., description="Impact on risk score (positive=up, negative=down)")
    direction: Literal["up", "down"] = Field(..., description="Direction of driver effect")


class ConfidenceBreakdown(BaseModel):
    """Confidence score breakdown by factor."""
    source_reliability: float = Field(ge=0.0, le=1.0)
    corroboration: float = Field(ge=0.0, le=1.0)
    coverage: float = Field(ge=0.0, le=1.0)
    rumor_penalty: float = Field(ge=0.0, le=1.0, default=0.0)


class LatestEvidence(BaseModel):
    """Single piece of evidence for country detail."""
    event_id: str
    timestamp: datetime
    signal: str = Field(..., description="Signal code (e.g., M5, P2)")
    summary: str
    source: SourceEvidence
    verified: bool = False


class CountryScore(BaseModel):
    """
    Risk score for a country.
    Field names match API contract: riskScore, riskBand, momentum, delta, confidence, topDrivers
    """
    country_code: str = Field(..., min_length=2, max_length=3, description="ISO3 country code")
    country_name: str = Field(default="", description="Country display name")
    risk_score: float = Field(..., ge=0.0, le=100.0, description="Overall risk score 0-100")
    risk_band: RiskBand = Field(..., description="Risk band: low/elevated/high/critical")
    momentum: TrendLabel = Field(..., description="Trend: escalating/stable/de-escalating")
    confidence: float = Field(..., ge=0.0, le=100.0, description="Confidence in score 0-100")
    delta: float = Field(default=0.0, description="Score change from previous period")
    delta_24h: float = Field(default=0.0, description="24-hour score change")
    delta_7d: float = Field(default=0.0, description="7-day score change")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    top_drivers: list[str] = Field(default_factory=list, description="Top risk drivers")


class CountryDetail(BaseModel):
    """Detailed country information for /countries/{countryCode} endpoint."""
    as_of: datetime
    country: CountryScore
    drivers: list[Driver] = Field(default_factory=list)
    confidence_breakdown: ConfidenceBreakdown
    latest_evidence: list[LatestEvidence] = Field(default_factory=list)


class TimelinePoint(BaseModel):
    """Single point in time series."""
    ts: datetime
    risk_score: float
    confidence: float


class Timeline(BaseModel):
    """Time series data for /countries/{countryCode}/timeline endpoint."""
    country_code: str
    window: str
    bucket: str
    points: list[TimelinePoint]


class MapSnapshot(BaseModel):
    """Response for /map/snapshot endpoint."""
    as_of: datetime
    window: str
    countries: list[CountryScore]
    meta: dict = Field(default_factory=dict)


# Helper function to compute risk band from score
def risk_band_from_score(score: float) -> RiskBand:
    """Map numeric score to risk band enum."""
    if score >= 75:
        return RiskBand.CRITICAL
    elif score >= 50:
        return RiskBand.HIGH
    elif score >= 25:
        return RiskBand.ELEVATED
    else:
        return RiskBand.LOW


# Country metadata for seed data
class CountryMetadata(BaseModel):
    code: str = Field(..., min_length=2, max_length=3)
    name: str
    region: str


# Seed countries list - global baseline
SEED_COUNTRIES: list[CountryMetadata] = [
    CountryMetadata(code="UKR", name="Ukraine", region="Europe"),
    CountryMetadata(code="ISR", name="Israel", region="Middle East"),
    CountryMetadata(code="TWN", name="Taiwan", region="Asia"),
    CountryMetadata(code="RUS", name="Russia", region="Europe"),
    CountryMetadata(code="CHN", name="China", region="Asia"),
    CountryMetadata(code="USA", name="United States", region="Americas"),
    CountryMetadata(code="IND", name="India", region="Asia"),
    CountryMetadata(code="PAK", name="Pakistan", region="Asia"),
    CountryMetadata(code="IRN", name="Iran", region="Middle East"),
    CountryMetadata(code="SAU", name="Saudi Arabia", region="Middle East"),
    CountryMetadata(code="PRK", name="North Korea", region="Asia"),
    CountryMetadata(code="KOR", name="South Korea", region="Asia"),
    CountryMetadata(code="VEN", name="Venezuela", region="Americas"),
    CountryMetadata(code="BRA", name="Brazil", region="Americas"),
    CountryMetadata(code="NGA", name="Nigeria", region="Africa"),
    CountryMetadata(code="EGY", name="Egypt", region="Africa"),
    CountryMetadata(code="SSD", name="South Sudan", region="Africa"),
    CountryMetadata(code="ETH", name="Ethiopia", region="Africa"),
    CountryMetadata(code="COI", name="Colombia", region="Americas"),
    CountryMetadata(code="MEX", name="Mexico", region="Americas"),
]