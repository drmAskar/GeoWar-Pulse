# GeoWar Pulse — API Contract (MVP)

Base URL (local/dev): `/api/v1`

## Conventions
- Timestamps are ISO-8601 UTC (`2026-02-28T13:00:00Z`)
- `countryCode` is ISO3 (e.g., `UKR`, `SYR`)
- Scores are integers `0..100`
- Momentum enum: `escalating | stable | de-escalating`
- Risk band enum: `low | elevated | high | critical`

Risk band mapping:
- `0–24` → `low`
- `25–49` → `elevated`
- `50–74` → `high`
- `75–100` → `critical`

---

## 1) Health
### `GET /health`

**200 Response**
```json
{
  "status": "ok",
  "service": "geowar-pulse-api",
  "version": "0.1.0",
  "time": "2026-02-28T13:00:00Z"
}
```

---

## 2) Map Snapshot
### `GET /map/snapshot?window=24h|7d|30d&minConfidence=0`

Returns one row per country for map rendering.

**Example Request**
`GET /api/v1/map/snapshot?window=24h&minConfidence=40`

**200 Response**
```json
{
  "asOf": "2026-02-28T13:00:00Z",
  "window": "24h",
  "countries": [
    {
      "countryCode": "UKR",
      "countryName": "Ukraine",
      "riskScore": 78,
      "riskBand": "critical",
      "momentum": "escalating",
      "delta": 9,
      "confidence": 81,
      "topDrivers": ["cross_border_strikes", "troop_mobilization"]
    },
    {
      "countryCode": "JOR",
      "countryName": "Jordan",
      "riskScore": 33,
      "riskBand": "elevated",
      "momentum": "stable",
      "delta": 1,
      "confidence": 62,
      "topDrivers": ["regional_spillover"]
    }
  ],
  "meta": {
    "totalCountries": 2,
    "dataFreshnessMinutes": 18
  }
}
```

---

## 3) Country Detail
### `GET /countries/{countryCode}?window=24h|7d|30d`

**Example Request**
`GET /api/v1/countries/UKR?window=7d`

**200 Response**
```json
{
  "asOf": "2026-02-28T13:00:00Z",
  "country": {
    "countryCode": "UKR",
    "countryName": "Ukraine",
    "riskScore": 78,
    "riskBand": "critical",
    "momentum": "escalating",
    "confidence": 81,
    "delta24h": 9,
    "delta7d": 14
  },
  "drivers": [
    {
      "key": "cross_border_strikes",
      "label": "Cross-border strikes",
      "impact": 12.4,
      "direction": "up"
    },
    {
      "key": "peace_talk_progress",
      "label": "Peace-talk progress",
      "impact": -3.1,
      "direction": "down"
    }
  ],
  "confidenceBreakdown": {
    "sourceReliability": 0.84,
    "corroboration": 0.73,
    "coverage": 0.78,
    "rumorPenalty": 0.07
  },
  "latestEvidence": [
    {
      "eventId": "evt_01JABCDEFG",
      "timestamp": "2026-02-28T10:45:00Z",
      "signal": "M5",
      "summary": "Confirmed artillery exchange near border sector.",
      "source": {
        "name": "acled",
        "tier": "A",
        "url": "https://example.org/event/evt_01JABCDEFG"
      },
      "verified": true
    }
  ]
}
```

**404 Response**
```json
{
  "error": {
    "code": "COUNTRY_NOT_FOUND",
    "message": "Country code not found: XXX"
  }
}
```

---

## 4) Country Timeline
### `GET /countries/{countryCode}/timeline?window=30d&bucket=day`

**Example Request**
`GET /api/v1/countries/UKR/timeline?window=30d&bucket=day`

**200 Response**
```json
{
  "countryCode": "UKR",
  "window": "30d",
  "bucket": "day",
  "points": [
    {
      "ts": "2026-02-25T00:00:00Z",
      "riskScore": 71,
      "confidence": 76
    },
    {
      "ts": "2026-02-26T00:00:00Z",
      "riskScore": 74,
      "confidence": 79
    },
    {
      "ts": "2026-02-27T00:00:00Z",
      "riskScore": 76,
      "confidence": 80
    },
    {
      "ts": "2026-02-28T00:00:00Z",
      "riskScore": 78,
      "confidence": 81
    }
  ]
}
```

---

## 5) Alerts List
### `GET /alerts?countryCode=UKR&active=true`

**200 Response**
```json
{
  "items": [
    {
      "alertId": "al_01JALERT001",
      "countryCode": "UKR",
      "threshold": 75,
      "triggeredAt": "2026-02-28T11:00:00Z",
      "currentScore": 78,
      "status": "active"
    }
  ],
  "meta": {
    "count": 1
  }
}
```

---

## 6) Subscribe to Alerts
### `POST /alerts/subscribe`

**Request Body**
```json
{
  "countryCode": "UKR",
  "threshold": 75,
  "channel": "email",
  "target": "analyst@example.com"
}
```

Validation:
- `threshold` allowed: `25 | 50 | 75`
- `channel` allowed in MVP: `email | webhook`

**201 Response**
```json
{
  "subscriptionId": "sub_01JSUB001",
  "countryCode": "UKR",
  "threshold": 75,
  "channel": "email",
  "target": "analyst@example.com",
  "createdAt": "2026-02-28T13:00:00Z"
}
```

**422 Response**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "threshold must be one of [25, 50, 75]"
  }
}
```

---

## Shared Error Envelope
All non-2xx responses should follow:

```json
{
  "error": {
    "code": "SOME_ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

Suggested standard error codes:
- `COUNTRY_NOT_FOUND`
- `INVALID_WINDOW`
- `VALIDATION_ERROR`
- `RATE_LIMITED`
- `INTERNAL_ERROR`
