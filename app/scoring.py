from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from math import exp

from .models import CountryScore, SignalEvent, TrendLabel


@dataclass(frozen=True)
class ScoreWeights:
    military: float = 0.30
    political: float = 0.20
    conflict: float = 0.20
    economic: float = 0.10
    credibility: float = 0.10
    spillover: float = 0.10


WEIGHTS = ScoreWeights()


def _hours_since(timestamp: datetime) -> float:
    now = datetime.now(timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    delta = now - timestamp.astimezone(timezone.utc)
    return max(delta.total_seconds() / 3600.0, 0.0)


def recency_decay(hours_old: float, half_life_hours: float = 24.0) -> float:
    """Exponential decay where older evidence contributes less."""
    if half_life_hours <= 0:
        return 1.0
    return exp(-0.69314718056 * (hours_old / half_life_hours))


def score_event(event: SignalEvent, weights: ScoreWeights = WEIGHTS) -> float:
    weighted_sum = (
        weights.military * event.military
        + weights.political * event.political
        + weights.conflict * event.conflict
        + weights.economic * event.economic
        + weights.credibility * event.credibility
        + weights.spillover * event.spillover
    )

    confirmation_bonus = 0.05 if event.status == "confirmed" else 0.0
    penalty = event.viral_unverified_penalty * 0.20
    decayed = (weighted_sum + confirmation_bonus - penalty) * recency_decay(_hours_since(event.occurred_at))
    return max(min(decayed, 1.0), 0.0)


def confidence_score(events: list[SignalEvent]) -> float:
    if not events:
        return 0.0

    evidences = [ev for event in events for ev in event.evidence]
    if not evidences:
        return 15.0  # low baseline confidence without evidence records

    reliability_avg = sum(e.reliability for e in evidences) / len(evidences)
    confirmation_groups = {e.confirmation_group for e in evidences if e.confirmation_group}
    confirmation_factor = min(len(confirmation_groups) / 5.0, 1.0)

    recency_values = [recency_decay(_hours_since(e.published_at), half_life_hours=36.0) for e in evidences]
    recency_factor = sum(recency_values) / len(recency_values)

    # Framework-inspired blend: reliability + independent confirmation + recency
    confidence = (0.5 * reliability_avg + 0.3 * confirmation_factor + 0.2 * recency_factor) * 100
    return round(max(min(confidence, 100.0), 0.0), 2)


def trend_from_deltas(delta_24h: float, delta_7d: float) -> TrendLabel:
    if delta_24h <= -3.0 and delta_7d <= -5.0:
        return TrendLabel.DEESCALATING
    if delta_24h >= 3.0 or delta_7d >= 5.0:
        return TrendLabel.ESCALATING
    return TrendLabel.STABLE


def score_country(country_code: str, events: list[SignalEvent], delta_24h: float = 0.0, delta_7d: float = 0.0) -> CountryScore:
    event_scores = [score_event(e) for e in events]
    risk_score = (sum(event_scores) / len(event_scores) * 100) if event_scores else 0.0

    ranked = sorted(
        [
            ("military signals", sum(e.military for e in events)),
            ("political & diplomatic", sum(e.political for e in events)),
            ("conflict events", sum(e.conflict for e in events)),
            ("economic stress", sum(e.economic for e in events)),
            ("information credibility", sum(e.credibility for e in events)),
            ("regional spillover", sum(e.spillover for e in events)),
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    top_drivers = [name for name, value in ranked if value > 0][:3]

    # Compute risk band from score
    from .models import risk_band_from_score
    risk_band = risk_band_from_score(risk_score)
    
    score_obj = CountryScore(
        country_code=country_code.upper(),
        risk_score=round(max(min(risk_score, 100.0), 0.0), 2),
        risk_band=risk_band,
        momentum=trend_from_deltas(delta_24h=delta_24h, delta_7d=delta_7d),
        confidence=confidence_score(events),
        delta=delta_24h,
        delta_24h=delta_24h,
        delta_7d=delta_7d,
        top_drivers=top_drivers,
    )
    return score_obj
