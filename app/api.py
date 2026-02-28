from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, HTTPException, Query

from .models import SignalEvent, SourceEvidence
from .scoring import score_country

router = APIRouter()


# TODO(data-ingestion): Replace this in-memory sample store with Postgres-backed repositories.
# TODO(data-ingestion): Add worker pipelines/adapters for source-specific ingestion + normalization.
# TODO(data-ingestion): Compute deltas from historical snapshots instead of fixed placeholders.
_SAMPLE_EVENTS: list[SignalEvent] = [
    SignalEvent(
        event_id="evt-1",
        country_code="UKR",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=4),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=3),
        status="confirmed",
        military=0.9,
        political=0.6,
        conflict=0.8,
        economic=0.3,
        credibility=0.9,
        spillover=0.5,
        evidence=[
            SourceEvidence(
                source_id="src-1",
                source_name="Reuters",
                source_type="newswire",
                reliability=0.9,
                url="https://www.reuters.com/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=3),
                confirmation_group="ukr-001",
            ),
            SourceEvidence(
                source_id="src-2",
                source_name="Official Defense Briefing",
                source_type="official",
                reliability=0.95,
                published_at=datetime.now(timezone.utc) - timedelta(hours=2),
                confirmation_group="ukr-001",
            ),
        ],
    ),
    SignalEvent(
        event_id="evt-2",
        country_code="TWN",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=10),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=9),
        status="reported",
        military=0.6,
        political=0.7,
        conflict=0.4,
        economic=0.5,
        credibility=0.6,
        spillover=0.4,
        viral_unverified_penalty=0.1,
        evidence=[
            SourceEvidence(
                source_id="src-3",
                source_name="AP News",
                source_type="newswire",
                reliability=0.85,
                url="https://apnews.com/",
                published_at=datetime.now(timezone.utc) - timedelta(hours=8),
                confirmation_group="twn-001",
            )
        ],
    ),
    SignalEvent(
        event_id="evt-3",
        country_code="ISR",
        occurred_at=datetime.now(timezone.utc) - timedelta(hours=26),
        reported_at=datetime.now(timezone.utc) - timedelta(hours=25),
        status="confirmed",
        military=0.7,
        political=0.8,
        conflict=0.7,
        economic=0.4,
        credibility=0.85,
        spillover=0.65,
        evidence=[
            SourceEvidence(
                source_id="src-4",
                source_name="UN Update",
                source_type="official",
                reliability=0.88,
                published_at=datetime.now(timezone.utc) - timedelta(hours=24),
                confirmation_group="isr-001",
            )
        ],
    ),
]

_WINDOW_TO_HOURS = {"24h": 24, "7d": 24 * 7, "30d": 24 * 30}


def _events_for_country(country_code: str, window: Literal["24h", "7d", "30d"]) -> list[SignalEvent]:
    threshold = datetime.now(timezone.utc) - timedelta(hours=_WINDOW_TO_HOURS[window])
    return [
        e
        for e in _SAMPLE_EVENTS
        if e.country_code.upper() == country_code.upper() and e.occurred_at >= threshold
    ]


def _countries_in_window(window: Literal["24h", "7d", "30d"]) -> list[str]:
    threshold = datetime.now(timezone.utc) - timedelta(hours=_WINDOW_TO_HOURS[window])
    return sorted({e.country_code.upper() for e in _SAMPLE_EVENTS if e.occurred_at >= threshold})


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "geowar-pulse-api"}


@router.get("/scores")
def list_scores(window: Literal["24h", "7d", "30d"] = Query("24h")):
    scores = []
    for code in _countries_in_window(window):
        events = _events_for_country(code, window)
        scores.append(score_country(country_code=code, events=events))
    return {"window": window, "count": len(scores), "items": scores}


@router.get("/scores/{country_code}")
def country_score(country_code: str, window: Literal["24h", "7d", "30d"] = Query("24h")):
    events = _events_for_country(country_code, window)
    if not events:
        raise HTTPException(status_code=404, detail=f"No score data for country {country_code} in {window}")

    # TODO(data-ingestion): Pull true deltas from stored historical aggregates.
    score = score_country(country_code=country_code, events=events, delta_24h=2.4, delta_7d=6.1)
    return score


@router.get("/drivers/{country_code}")
def country_drivers(country_code: str, window: Literal["24h", "7d", "30d"] = Query("24h")):
    events = _events_for_country(country_code, window)
    if not events:
        raise HTTPException(status_code=404, detail=f"No driver data for country {country_code} in {window}")

    score = score_country(country_code=country_code, events=events, delta_24h=1.0, delta_7d=2.0)
    return {
        "country_code": country_code.upper(),
        "window": window,
        "drivers": score.top_drivers,
        "score": score.score,
        "confidence": score.confidence,
    }
