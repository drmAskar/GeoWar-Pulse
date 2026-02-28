# GeoWar Pulse — Implementation Plan (Phase 1 Integration)

## Goal
Ship a working MVP that integrates **database + backend APIs + frontend map UI** in a low-risk merge sequence.

## Assumptions
- Backend: FastAPI
- DB: Postgres
- Frontend: React map UI
- Data refresh is batch/scheduled for MVP (not full streaming)

---

## Branching & Merge Strategy
- Keep one long-lived integration branch: `integration/phase1-mvp`
- Merge in small vertical slices from feature branches.
- Every merge must pass:
  - backend tests
  - DB migration check (up/down locally)
  - frontend smoke test
  - contract check for API response shape

Recommended branch naming:
- `feat/db-*`
- `feat/api-*`
- `feat/frontend-*`
- `chore/ci-*`

---

## Step-by-Step Merge Order

## 0) Foundation (first merge)
**Branch:** `chore/foundation`

Deliverables:
- Project structure for `backend/`, `frontend/`, `infra/` (if missing)
- Shared `.env.example`
- Local dev orchestration (e.g., docker compose for Postgres)
- CI skeleton (lint/test placeholders)

Why first:
- Prevents later rework and broken local setup.

---

## 1) Database Schema v1 (second merge)
**Branch:** `feat/db-schema-v1`

Deliverables:
- Migration tool setup (Alembic or equivalent)
- Core tables:
  - `countries`
  - `events_raw`
  - `events_normalized`
  - `country_features_daily`
  - `country_scores`
  - `alerts`
  - `ingestion_runs`
- Indexes:
  - `country_scores(country_code, as_of_ts desc)`
  - `events_normalized(country_code, event_ts desc)`
  - `alerts(country_code, created_at desc)`
- Seed file for countries (ISO3 baseline)

Exit criteria:
- Migration up/down works on clean DB
- Seed script inserts all countries

---

## 2) Ingestion Contract + Normalization Pipeline (third merge)
**Branch:** `feat/backend-ingestion-contract`

Deliverables:
- Internal ingestion DTO/schema for event ingestion
- Normalization mapper from raw provider event -> canonical event model
- Write path into `events_raw` + `events_normalized`
- Basic dedupe key strategy (`provider + provider_event_id + event_ts`)

Exit criteria:
- Can ingest sample ACLED/GDELT fixtures
- Normalized rows visible in DB with predictable schema

---

## 3) Feature Builder + Scoring Engine v0.1 (fourth merge)
**Branch:** `feat/backend-scoring-v01`

Deliverables:
- Daily feature aggregation job:
  - 24h/7d/30d deltas
  - category buckets
  - confidence inputs
- Score computation v0.1 (0–100)
- Momentum labels (`escalating`, `stable`, `de-escalating`)
- Driver attribution output for top factors
- Persistence to `country_features_daily` and `country_scores`

Exit criteria:
- Given fixed fixtures, scoring output is deterministic
- Score + confidence + drivers saved per country

---

## 4) Backend Read APIs (fifth merge)
**Branch:** `feat/api-mvp-read-endpoints`

Deliverables:
- MVP read endpoints:
  - `GET /api/v1/health`
  - `GET /api/v1/map/snapshot`
  - `GET /api/v1/countries/{countryCode}`
  - `GET /api/v1/countries/{countryCode}/timeline`
  - `GET /api/v1/alerts`
  - `POST /api/v1/alerts/subscribe` (lightweight MVP)
- Response models match `docs/API_CONTRACT.md`

Exit criteria:
- OpenAPI generated and validated
- Contract examples return from real data fixtures

---

## 5) Frontend Map Skeleton + API Wiring (sixth merge)
**Branch:** `feat/frontend-map-mvp`

Deliverables:
- World map with risk band coloring
- Filter controls for `24h / 7d / 30d`
- Country tooltip (score, momentum, confidence)
- Country detail drawer using `/countries/{code}` + `/timeline`
- Error/empty/stale-data states

Exit criteria:
- Frontend renders from backend snapshot endpoint
- Selecting a country shows detail panel and trend

---

## 6) Alerts Flow + Watchlist UX (seventh merge)
**Branch:** `feat/frontend-alerts-watchlist`

Deliverables:
- Alerts list page or panel
- Subscribe action wired to `POST /alerts/subscribe`
- Threshold crossing indicators

Exit criteria:
- User can subscribe to country threshold alerts
- Triggered alerts are retrievable and visible in UI

---

## 7) Hardening + Observability + Release Candidate (eighth merge)
**Branch:** `chore/phase1-hardening`

Deliverables:
- Logging correlation IDs (ingestion run id/request id)
- API latency + ingestion freshness metrics
- Basic auth/rate-limit guardrails (if exposed)
- Smoke E2E script: ingest fixture -> score -> map render
- Release notes for MVP

Exit criteria:
- End-to-end MVP flow works in clean environment
- Known limitations documented

---

## Integration Risks & Mitigations
1. **Schema churn while frontend starts**
   - Mitigation: freeze API DTOs before frontend deep wiring.
2. **Provider-specific event inconsistency**
   - Mitigation: strict normalized canonical schema and fixture tests.
3. **Noisy signals causing unstable UI**
   - Mitigation: min confidence gate + capped score jumps per run.
4. **Latency from heavy on-demand aggregation**
   - Mitigation: precompute daily snapshots in `country_scores`.

---

## Definition of Done (Phase 1)
- Map loads global scores for all seeded countries.
- Country panel shows:
  - risk score
  - momentum
  - confidence
  - top drivers
  - 24h/7d/30d trend
- Alerts can be subscribed and listed.
- Every score is traceable to feature and source metadata.
- API contract stable and documented.
