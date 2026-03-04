# GeoWar Pulse - Build Report

## Overview
This report documents the changes made to align the GeoWar Pulse backend and frontend with the API contract defined in `docs/API_CONTRACT.md`.

## Completed Tasks

### 1. Backend API Contract Correctness ✅

**Changes made to `app/models.py`:**
- Added `RiskBand` enum (low/elevated/high/critical)
- Added `Driver` model for risk drivers with key, label, impact, direction
- Added `ConfidenceBreakdown` model with source_reliability, corroboration, coverage, rumor_penalty
- Added `LatestEvidence` model for evidence display
- Added `CountryDetail` model for `/countries/{countryCode}` endpoint
- Added `Timeline` and `TimelinePoint` models for `/countries/{countryCode}/timeline`
- Added `MapSnapshot` model for `/map/snapshot` endpoint
- Renamed `score` field to `risk_score` for API contract compliance
- Added `risk_band` field computed from risk score
- Added `delta` field (primary score change)
- Added `country_name` field
- Added `SEED_COUNTRIES` list with 20 countries for global baseline

**Changes made to `app/api.py`:**
- Added `/map/snapshot` endpoint returning all countries for map rendering
- Added `/countries/{countryCode}` endpoint returning detailed country info
- Added `/countries/{countryCode}/timeline` endpoint for time series data
- Added `/health` endpoint with version info
- Kept legacy `/scores` and `/scores/{country_code}` endpoints for backward compatibility
- Added sample events for 8 countries (UKR, ISR, TWN, VEN, RUS, IRN, PRK, SAU)
- Added transformation functions to build contract-compliant responses

### 2. Scoring Fields Normalization ✅

**In `app/scoring.py` (unchanged, integrated with new models):**
- `riskScore`: 0-100 risk score (from weighted event analysis)
- `confidence`: 0-100 confidence based on source reliability, corroboration, and recency
- `momentum`: escalating/stable/de-escalating based on delta calculations
- `drivers`: Top 3 risk drivers from event categories

**New fields in response:**
- `riskBand`: Computed from riskScore (0-24=low, 25-49=elevated, 50-74=high, 75-100=critical)
- `delta`: Primary score change value
- `delta_24h`: 24-hour change
- `delta_7d`: 7-day change
- `confidenceBreakdown`: Detailed confidence factors (in country detail)

### 3. Seed/Data Scaffold for Multiple Countries ✅

**Countries with sample data:**
- UKR (Ukraine) - High risk, escalating
- ISR (Israel) - High risk, escalating  
- TWN (Taiwan) - Elevated risk
- VEN (Venezuela) - Elevated risk
- RUS (Russia) - Elevated risk
- IRN (Iran) - Elevated risk
- PRK (North Korea) - Low risk
- SAU (Saudi Arabia) - Low risk

**Seed countries list (20 total):**
UKR, ISR, TWN, RUS, CHN, USA, IND, PAK, IRN, SAU, PRK, KOR, VEN, BRA, NGA, EGY, SSD, ETH, COL, MEX

### 4. Frontend Render Compatibility ✅

**New files created:**
- `frontend/src/services/api.js` - API client with response transformation

**Updated files:**
- `frontend/src/App.jsx` - Now fetches from real API with fallback to sample data
- `frontend/src/components/RiskMap.jsx` - Updated for new data format with momentum display
- `frontend/src/components/CountryDetailPanel.jsx` - Full detail view with drivers, confidence breakdown, evidence, timeline
- `frontend/src/components/HotspotsList.jsx` - Updated for new data format
- `frontend/src/styles.css` - Complete restyle with dark theme and new component styles

**Frontend features:**
- Window selector (24h/7d/30d)
- Auto-refresh every 5 minutes
- Fallback to sample data when API unavailable
- Country detail panel with:
  - Risk score and band
  - Confidence breakdown bars
  - Top drivers with impact values
  - Latest evidence with verification status
  - 30-day timeline chart

## How to Run

### Backend
```bash
cd /root/.openclaw/workspace/GeoWar-Pulse
source .venv/bin/activate  # or . .venv/bin/activate
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API will be available at: http://localhost:8000

### Frontend
```bash
cd /root/.openclaw/workspace/GeoWar-Pulse/frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

### Environment Variables (optional)
Create `.env` file in frontend:
```
VITE_API_URL=http://localhost:8000/api/v1
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /map/snapshot?window=24h|7d|30d&min_confidence=0` | All countries for map |
| `GET /countries/{countryCode}?window=24h|7d|30d` | Country detail |
| `GET /countries/{countryCode}/timeline?window=30d&bucket=day` | Timeline data |
| `GET /scores?window=24h|7d|30d` | Legacy scores list |
| `GET /scores/{countryCode}` | Legacy single score |

## Commit Summary

```
# Backend changes
- models.py: Added contract-compliant models (RiskBand, Driver, ConfidenceBreakdown, etc.)
- api.py: Added /map/snapshot, /countries/{code}, /countries/{code}/timeline endpoints
- Added 8 countries with sample events (expanded from 3)

# Frontend changes  
- services/api.js: New API client with response transformation
- App.jsx: API integration with fallback
- RiskMap.jsx: Updated for new format
- CountryDetailPanel.jsx: Full detail view
- HotspotsList.jsx: Updated for new format
- styles.css: Complete restyle
```

## Remaining Tasks (for future iterations)

1. **Database integration** - Replace in-memory events with PostgreSQL
2. **Real data ingestion** - Connect to ACLED, GDELT, UNHCR sources
3. **Historical deltas** - Compute true delta from stored historical scores
4. **Alerts endpoint** - Implement `/alerts` and `/alerts/subscribe`
5. **GeoJSON map** - Upgrade from circle markers to choropleth polygons
6. **Testing** - Add unit and integration tests

## Notes

- The API now matches the contract in `docs/API_CONTRACT.md`
- Frontend has graceful fallback to sample data if API is unavailable
- Confidence breakdown shows source reliability, corroboration, coverage, and rumor penalty
- Momentum is computed from delta values (escalating if delta_24h >= 3 or delta_7d >= 5)