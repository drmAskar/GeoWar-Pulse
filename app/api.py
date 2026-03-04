from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Literal, List, Optional
from fastapi import APIRouter, HTTPException, Query
from .models import (
    SignalEvent, SourceEvidence, CountryScore, MapSnapshot, CountryDetail,
    Driver, ConfidenceBreakdown, LatestEvidence, Timeline, TimelinePoint,
    RiskBand, TrendLabel, SEED_COUNTRIES, risk_band_from_score
)
from .scoring import score_country, confidence_score, trend_from_deltas

router = APIRouter()

_WINDOW_TO_HOURS = {"24h": 24, "7d": 24 * 7, "30d": 24 * 30}

# Extended sample events for multiple countries (global baseline)
_SAMPLE_EVENTS: list[SignalEvent] = [
    # Ukraine - high risk, escalating
    SignalEvent(
        event_id="evt-ukr-1",
        country_code="UKR",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=4),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=3),
        status="confirmed",
        military=0.9, political=0.6, conflict=0.8, economic=0.3,
        credibility=0.9, spillover=0.5,
        evidence=[
            SourceEvidence(
                source_id="src-ukr-1", source_name="Reuters", source_type="newswire",
                reliability=0.9, url="https://reuters.com/", 
                published_at=datetime.now(timezone.utc) - timedelta(hours=3),
                confirmation_group="ukr-001",
            ),
            SourceEvidence(
                source_id="src-ukr-2", source_name="Defense Ministry", source_type="official",
                reliability=0.95, published_at=datetime.now(timezone.utc) - timedelta(hours=2),
                confirmation_group="ukr-001",
            ),
        ],
    ),
    SignalEvent(
        event_id="evt-ukr-2",
        country_code="UKR",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=12),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=10),
        status="confirmed",
        military=0.7, political=0.5, conflict=0.75, economic=0.4,
        credibility=0.8, spillover=0.6,
        evidence=[
            SourceEvidence(
                source_id="src-ukr-3", source_name="UN OCHA", source_type="official",
                reliability=0.92, url="https://unocha.org/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=10),
                confirmation_group="ukr-002",
            ),
        ],
    ),
    # Israel - high risk, escalating
    SignalEvent(
        event_id="evt-isr-1",
        country_code="ISR",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=6),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=5),
        status="confirmed",
        military=0.8, political=0.85, conflict=0.75, economic=0.4,
        credibility=0.85, spillover=0.7,
        evidence=[
            SourceEvidence(
                source_id="src-isr-1", source_name="AP News", source_type="newswire",
                reliability=0.88, url="https://apnews.com/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=5),
                confirmation_group="isr-001",
            ),
        ],
    ),
    SignalEvent(
        event_id="evt-isr-2",
        country_code="ISR",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=18),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=16),
        status="reported",
        military=0.6, political=0.7, conflict=0.6, economic=0.3,
        credibility=0.7, spillover=0.5,
        evidence=[
            SourceEvidence(
                source_id="src-isr-2", source_name="Social Media", source_type="social",
                reliability=0.5, published_at=datetime.now(timezone.utc) - timedelta(hours=16),
                confirmation_group=None,
            ),
        ],
    ),
    # Taiwan - elevated risk
    SignalEvent(
        event_id="evt-twn-1",
        country_code="TWN",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=10),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=9),
        status="reported",
        military=0.6, political=0.7, conflict=0.4, economic=0.5,
        credibility=0.6, spillover=0.4, viral_unverified_penalty=0.1,
        evidence=[
            SourceEvidence(
                source_id="src-twn-1", source_name="AP News", source_type="newswire",
                reliability=0.85, url="https://apnews.com/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=8),
                confirmation_group="twn-001",
            ),
        ],
    ),
    # Venezuela - elevated risk
    SignalEvent(
        event_id="evt-ven-1",
        country_code="VEN",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=20),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=18),
        status="confirmed",
        military=0.3, political=0.8, conflict=0.5, economic=0.9,
        credibility=0.6, spillover=0.3,
        evidence=[
            SourceEvidence(
                source_id="src-ven-1", source_name="Human Rights Watch", source_type="ngo",
                reliability=0.8, url="https://hrw.org/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=18),
                confirmation_group="ven-001",
            ),
        ],
    ),
    # Russia - elevated risk
    SignalEvent(
        event_id="evt-rus-1",
        country_code="RUS",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=30),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=28),
        status="confirmed",
        military=0.7, political=0.6, conflict=0.5, economic=0.5,
        credibility=0.75, spillover=0.4,
        evidence=[
            SourceEvidence(
                source_id="src-rus-1", source_name="Reuters", source_type="newswire",
                reliability=0.9, url="https://reuters.com/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=28),
                confirmation_group="rus-001",
            ),
        ],
    ),
    # Iran - elevated risk
    SignalEvent(
        event_id="evt-irn-1",
        country_code="IRN",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=15),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=14),
        status="reported",
        military=0.65, political=0.75, conflict=0.5, economic=0.6,
        credibility=0.65, spillover=0.45,
        evidence=[
            SourceEvidence(
                source_id="src-irn-1", source_name="BBC", source_type="media",
                reliability=0.82, url="https://bbc.com/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=14),
                confirmation_group="irn-001",
            ),
        ],
    ),
    # North Korea - low but with activity
    SignalEvent(
        event_id="evt-prk-1",
        country_code="PRK",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=40),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=38),
        status="reported",
        military=0.5, political=0.4, conflict=0.3, economic=0.2,
        credibility=0.4, spillover=0.2,
        evidence=[
            SourceEvidence(
                source_id="src-prk-1", source_name="38 North", source_type="intel",
                reliability=0.75, url="https://38north.org/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=38),
                confirmation_group="prk-001",
            ),
        ],
    ),
    # Saudi Arabia - low risk
    SignalEvent(
        event_id="evt-sau-1",
        country_code="SAU",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=50),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=48),
        status="confirmed",
        military=0.2, political=0.3, conflict=0.15, economic=0.25,
        credibility=0.7, spillover=0.2,
        evidence=[
            SourceEvidence(
                source_id="src-sau-1", source_name="Reuters", source_type="newswire",
                reliability=0.9, url="https://reuters.com/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=48),
                confirmation_group="sau-001",
            ),
        ],
    ),
]

# Country name mapping
_COUNTRY_NAMES = {c.code: c.name for c in SEED_COUNTRIES}


def _events_for_country(country_code: str, window: Literal["24h", "7d", "30d"]) -> list[SignalEvent]:
    """Filter events for a specific country within the time window."""
    threshold = datetime.now(timezone.utc) - timedelta(hours=_WINDOW_TO_HOURS[window])
    return [
        e for e in _SAMPLE_EVENTS 
        if e.country_code.upper() == country_code.upper() 
        and e.occurred_at >= threshold
    ]


def _all_countries_in_window(window: Literal["24h", "7d", "30d"]) -> list[str]:
    """Get all countries with events in the window."""
    threshold = datetime.now(timezone.utc) - timedelta(hours=_WINDOW_TO_HOURS[window])
    return sorted({e.country_code.upper() for e in _SAMPLE_EVENTS if e.occurred_at >= threshold})


def _build_country_score(country_code: str, events: list[SignalEvent], 
                         delta_24h: float = 0.0, delta_7d: float = 0.0) -> CountryScore:
    """Build a CountryScore object from events, matching API contract."""
    raw_score = score_country(country_code=country_code, events=events, delta_24h=delta_24h, delta_7d=delta_7d)
    # Compute delta from 24h change (use delta_24h as the primary delta)
    delta = delta_24h
    
    return CountryScore(
        country_code=country_code.upper(),
        country_name=_COUNTRY_NAMES.get(country_code.upper(), country_code),
        risk_score=raw_score.risk_score,
        risk_band=raw_score.risk_band,
        momentum=raw_score.momentum,
        confidence=raw_score.confidence,
        delta=round(delta, 1),
        delta_24h=round(delta_24h, 1),
        delta_7d=round(delta_7d, 1),
        top_drivers=raw_score.top_drivers,
    )


@router.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "geowar-pulse-api",
        "version": "0.1.0",
        "time": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/map/snapshot")
def map_snapshot(
    window: Literal["24h", "7d", "30d"] = Query("24h"),
    min_confidence: float = Query(0, ge=0, le=100)
) -> MapSnapshot:
    """
    Get map snapshot - all countries with risk scores for map rendering.
    Matches API contract: /api/v1/map/snapshot
    """
    countries = []
    country_codes = _all_countries_in_window(window)
    
    # Sample deltas for demo (in production, compute from historical data)
    delta_map = {
        "UKR": (9.0, 14.0),
        "ISR": (7.0, 12.0),
        "TWN": (4.0, 8.0),
        "VEN": (3.0, 5.0),
        "RUS": (2.0, 4.0),
        "IRN": (1.0, 3.0),
        "PRK": (0.5, 1.0),
        "SAU": (-1.0, -2.0),
    }
    
    for code in country_codes:
        events = _events_for_country(code, window)
        if events:
            d24, d7 = delta_map.get(code, (0.0, 0.0))
            score = _build_country_score(code, events, delta_24h=d24, delta_7d=d7)
            if score.confidence >= min_confidence:
                countries.append(score)
    
    # Calculate data freshness (mock - would be from actual data)
    data_freshness = 18  # minutes
    
    return MapSnapshot(
        as_of=datetime.now(timezone.utc),
        window=window,
        countries=countries,
        meta={
            "totalCountries": len(countries),
            "dataFreshnessMinutes": data_freshness,
        }
    )


@router.get("/countries/{country_code}")
def country_detail(
    country_code: str,
    window: Literal["24h", "7d", "30d"] = Query("24h")
) -> CountryDetail:
    """
    Get detailed country information.
    Matches API contract: /api/v1/countries/{countryCode}
    """
    events = _events_for_country(country_code, window)
    
    if not events:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "COUNTRY_NOT_FOUND", 
                    "message": f"Country code not found: {country_code}"
                }
            }
        )
    
    # Sample deltas (would be computed from historical data)
    delta_map = {
        "UKR": (9.0, 14.0),
        "ISR": (7.0, 12.0),
        "TWN": (4.0, 8.0),
        "VEN": (3.0, 5.0),
    }
    d24, d7 = delta_map.get(country_code.upper(), (0.0, 0.0))
    
    country_score = _build_country_score(country_code, events, delta_24h=d24, delta_7d=d7)
    
    # Build driver list with impact values
    drivers = []
    for i, driver_key in enumerate(country_score.top_drivers):
        impact = 12.4 - (i * 3.5)  # Sample impacts
        drivers.append(Driver(
            key=driver_key.replace(" ", "_").lower(),
            label=driver_key.title(),
            impact=round(impact, 1),
            direction="up"
        ))
    
    # Confidence breakdown (would be computed from evidence)
    conf = country_score.confidence / 100.0
    confidence_breakdown = ConfidenceBreakdown(
        source_reliability=round(0.75 + (conf * 0.2), 2),
        corroboration=round(0.6 + (conf * 0.3), 2),
        coverage=round(0.65 + (conf * 0.25), 2),
        rumor_penalty=round(0.05 * (1 - conf), 2),
    )
    
    # Latest evidence (most recent event)
    latest_evidence = []
    for event in sorted(events, key=lambda e: e.occurred_at, reverse=True)[:3]:
        if event.evidence:
            ev = event.evidence[0]
            signal_code = f"M{int(event.military * 5 + 1)}"
            latest_evidence.append(LatestEvidence(
                event_id=event.event_id,
                timestamp=event.occurred_at,
                signal=signal_code,
                summary=f"Recorded {event.event_id} with military={event.military}, political={event.political}",
                source=ev,
                verified=(event.status == "confirmed"),
            ))
    
    return CountryDetail(
        as_of=datetime.now(timezone.utc),
        country=country_score,
        drivers=drivers,
        confidence_breakdown=confidence_breakdown,
        latest_evidence=latest_evidence,
    )


@router.get("/countries/{country_code}/timeline")
def country_timeline(
    country_code: str,
    window: Literal["24h", "7d", "30d"] = Query("30d"),
    bucket: Literal["hour", "day"] = Query("day")
) -> Timeline:
    """
    Get timeline data for a country.
    Matches API contract: /api/v1/countries/{countryCode}/timeline
    """
    events = _events_for_country(country_code, window)
    
    if not events:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "COUNTRY_NOT_FOUND", 
                    "message": f"No timeline data for: {country_code}"
                }
            }
        )
    
    # Generate sample timeline points (would be computed from historical data)
    # For now, create a simple trajectory based on current score
    base_score = score_country(country_code, events).score
    base_conf = confidence_score(events)
    
    points = []
    now = datetime.now(timezone.utc)
    num_points = 7 if window == "7d" else (30 if window == "30d" else 1)
    
    for i in range(num_points):
        ts = now - timedelta(days=num_points - i - 1)
        # Simulate a gradual trajectory
        score_variation = (i - num_points/2) * 1.5
        points.append(TimelinePoint(
            ts=ts,
            risk_score=round(max(min(base_score + score_variation, 100), 0), 1),
            confidence=round(max(min(base_conf + (i * 0.5), 100), 0), 1),
        ))
    
    return Timeline(
        country_code=country_code.upper(),
        window=window,
        bucket=bucket,
        points=points,
    )


# Legacy endpoints for backward compatibility
@router.get("/scores")
def list_scores(window: Literal["24h", "7d", "30d"] = Query("24h")):
    """Legacy endpoint - returns scores in simplified format."""
    scores = []
    for code in _all_countries_in_window(window):
        events = _events_for_country(code, window)
        if events:
            d24, d7 = (9.0, 14.0) if code == "UKR" else (0.0, 0.0)
            scores.append(_build_country_score(code, events, delta_24h=d24, delta_7d=d7))
    
    return {"window": window, "count": len(scores), "items": scores}


@router.get("/scores/{country_code}")
def country_score(country_code: str, window: Literal["24h", "7d", "30d"] = Query("24h")):
    """Legacy endpoint - returns single country score."""
    events = _events_for_country(country_code, window)
    if not events:
        raise HTTPException(status_code=404, detail=f"No score data for country {country_code}")
    
    d24, d7 = (9.0, 14.0) if country_code.upper() == "UKR" else (0.0, 0.0)
    return _build_country_score(country_code, events, delta_24h=d24, delta_7d=d7)