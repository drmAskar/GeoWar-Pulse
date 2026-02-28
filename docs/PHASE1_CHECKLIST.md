# GeoWar Pulse — Phase 1 Execution Checklist (Acceptance Criteria)

Use this as the go/no-go checklist for MVP Phase 1.

## A. Data + DB Layer

- [ ] **A1. Schema migrated in clean environment**
  - Acceptance:
    - Migrations run up/down without manual intervention.
    - Core tables exist: `countries`, `events_raw`, `events_normalized`, `country_features_daily`, `country_scores`, `alerts`, `ingestion_runs`.

- [ ] **A2. Country seed loaded**
  - Acceptance:
    - ISO3 countries populated and queryable.
    - No duplicate country codes.

- [ ] **A3. Ingestion run tracking works**
  - Acceptance:
    - Every ingestion job writes `started_at`, `finished_at`, `status`, row counters.
    - Failed runs retain error metadata.

- [ ] **A4. Raw + normalized event persistence works**
  - Acceptance:
    - Fixture ingest stores raw provider payload and normalized canonical event.
    - Dedupe rules prevent duplicate normalized events for same provider event key.

## B. Scoring Engine + Features

- [ ] **B1. Daily feature generation works**
  - Acceptance:
    - For test countries, features are generated for 24h/7d/30d windows.
    - Missing input data does not crash job; defaults are explicit.

- [ ] **B2. Risk score generated (0–100)**
  - Acceptance:
    - Scores are integers in [0,100].
    - Risk band mapping exactly follows README ranges.

- [ ] **B3. Momentum labels generated**
  - Acceptance:
    - Output is one of: `escalating | stable | de-escalating`.
    - Label is tied to window deltas (24h and 7d logic).

- [ ] **B4. Confidence score generated**
  - Acceptance:
    - Confidence output in [0,100].
    - Includes at least source reliability + corroboration components.

- [ ] **B5. Driver attribution stored**
  - Acceptance:
    - Top positive and negative contributors are persisted per score snapshot.
    - Country detail endpoint can render at least top 3 drivers.

## C. API Layer (Contract Compliance)

- [ ] **C1. Health endpoint available** (`GET /api/v1/health`)
  - Acceptance:
    - Returns service status, version, and UTC timestamp.

- [ ] **C2. Map snapshot endpoint compliant** (`GET /api/v1/map/snapshot`)
  - Acceptance:
    - Returns country list with `riskScore`, `riskBand`, `momentum`, `confidence`, `topDrivers`.
    - Supports window filter `24h|7d|30d`.

- [ ] **C3. Country detail endpoint compliant** (`GET /api/v1/countries/{countryCode}`)
  - Acceptance:
    - Returns summary metrics + drivers + confidence breakdown + evidence list.
    - Unknown country returns 404 with error envelope.

- [ ] **C4. Timeline endpoint compliant** (`GET /api/v1/countries/{countryCode}/timeline`)
  - Acceptance:
    - Returns ordered points for selected window.
    - Supports daily buckets for MVP.

- [ ] **C5. Alerts endpoints compliant** (`GET /api/v1/alerts`, `POST /api/v1/alerts/subscribe`)
  - Acceptance:
    - Can create and list alert subscriptions.
    - Validation rejects unsupported thresholds/channels.

- [ ] **C6. Error envelope standardized**
  - Acceptance:
    - All non-2xx responses follow `{ error: { code, message, details? } }`.

## D. Frontend Layer

- [ ] **D1. Map renders risk bands**
  - Acceptance:
    - Countries visibly colored by risk band.
    - No-data countries use neutral style.

- [ ] **D2. Time window toggle works**
  - Acceptance:
    - Switching 24h/7d/30d updates map and country panel.

- [ ] **D3. Country interaction works**
  - Acceptance:
    - Hover/tap shows quick tooltip.
    - Selecting a country opens details drawer/sheet with score, momentum, confidence, drivers.

- [ ] **D4. Trend visualization works**
  - Acceptance:
    - Timeline graph reads from timeline API and handles sparse data.

- [ ] **D5. Alert UX wired**
  - Acceptance:
    - User can submit alert subscription and see active alerts list.

- [ ] **D6. Fault tolerance in UI**
  - Acceptance:
    - Loading, API error, and stale-data states are visibly handled.

## E. End-to-End + Operational Readiness

- [ ] **E1. End-to-end smoke test passes**
  - Acceptance:
    - Ingest fixture -> generate features/scores -> API serves -> frontend displays expected country update.

- [ ] **E2. Data freshness visible**
  - Acceptance:
    - API returns freshness metadata.
    - UI shows “updated X min ago”.

- [ ] **E3. Observability baseline present**
  - Acceptance:
    - Logs include request IDs / ingestion run IDs.
    - Basic metrics captured (ingestion duration, API p95 for snapshot endpoint).

- [ ] **E4. MVP limitations documented**
  - Acceptance:
    - README/docs list known caveats (coverage gaps, confidence caveats, not deterministic predictions).

## Final Phase-1 Signoff Criteria

Phase 1 is accepted only if all are true:
- [ ] No P0/P1 defects in ingest->score->map flow
- [ ] API contract matches `docs/API_CONTRACT.md`
- [ ] Demo scenario completes in <10 minutes on clean setup
- [ ] At least 3 representative countries validated manually (high/elevated/low)
- [ ] Stakeholder review confirms explainability output is understandable
