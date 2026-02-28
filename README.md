# GeoWar Pulse

A global conflict-risk intelligence dashboard that visualizes geopolitical tension on a world map.

## Vision
GeoWar Pulse provides a **probabilistic risk score** (not certainty) for escalation and conflict momentum across countries and regions.

## Core Outputs
- **War Risk Score (0–100)**
- **Conflict Momentum** (de-escalating / stable / escalating)
- **Confidence Score** (source quality + cross-verification)

## MVP Scope (Phase 1)
- Country-level risk map with color bands
- Top drivers per country ("why score moved")
- 24h/7d/30d trend views
- Alerts for threshold crossings

## Risk Bands
- 0–24: Low (Green)
- 25–49: Elevated (Yellow)
- 50–74: High (Orange)
- 75–100: Critical (Red)

## High-Level Stack
- **Backend**: Python FastAPI (scoring + API)
- **Data ingestion**: scheduled workers + source adapters
- **Frontend**: React + map visualization
- **Storage**: Postgres (events/features/scores)

## Status
Project initialized. Next step: deep research + scoring framework + data-source catalog.
