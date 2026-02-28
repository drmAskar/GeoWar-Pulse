from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field


class TrendLabel(str, Enum):
    DEESCALATING = "de-escalating"
    STABLE = "stable"
    ESCALATING = "escalating"


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


class CountryScore(BaseModel):
    country_code: str = Field(..., min_length=2, max_length=3)
    score: float = Field(..., ge=0.0, le=100.0)
    confidence: float = Field(..., ge=0.0, le=100.0)
    trend: TrendLabel

    delta_24h: float = 0.0
    delta_7d: float = 0.0

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    top_drivers: list[str] = Field(default_factory=list)
