# GeoWar Pulse — Execution Audit (Kickoff)

**Date:** 2026-03-03 (UTC)  
**Scope:** repository audit vs production-grade global geopolitical risk platform goals  
**Sources reviewed:** `docs/RESEARCH_SIGNALS.md`, `SPEC.md`, `PLAN.md`, `TASKS.md`, `API_CONTRACT.md`, `DATA_MODEL.md`, `PHASE1_CHECKLIST.md`, code in `app/`, `db/`, `frontend/`.

---

## 1) Executive Assessment

**Current state:** solid **MVP skeleton** with strong conceptual docs and a working demo path, but **not production-ready** yet.

- **Architecture maturity:** 4/10
- **Data ingestion readiness:** 1.5/10
- **Scoring/model readiness:** 3/10
- **API contract completeness:** 3/10
- **Frontend map/dashboard maturity:** 5/10
- **Operational readiness (scheduler/monitoring/security/tests):** 1/10

**Bottom line:** foundations are good; implementation depth is still early. The biggest gaps are ingestion pipelines, canonical normalization, historical storage, confidence/anti-rumor implementation per research spec, and contract-compliant API surface.

---

## 2) What Is Complete vs Missing

## A) Strategy, specification, and explainability design

### ✅ Complete
- Strong product framing and scope in `PRD.md`, `SPEC.md`.
- Clear signal taxonomy and formulas in `RESEARCH_SIGNALS.md` (event confidence, recency decay, rumor penalty, confidence decomposition, explainability output).
- Good source landscape and tiering in `RESEARCH_SOURCES.md`.
- Initial API and data model contracts exist (`API_CONTRACT.md`, `DATA_MODEL.md`).

### ❌ Missing / Gaps
- Contracts are not yet consistently reflected in implemented code and schema naming (e.g., docs mention `events_raw/events_normalized/country_scores`; schema currently uses `events/features/scores`).
- No formal Architecture Decision Records (ADR) for tradeoffs (batch cadence, source precedence, dedupe policy, confidence fail-open/fail-closed behavior).

---

## B) Backend/API

### ✅ Complete
- FastAPI service boots (`app/main.py`) with health/version/root.
- Basic endpoints exist: `/scores`, `/scores/{country_code}`, `/drivers/{country_code}`.
- Pydantic models for event/evidence/score are defined.
- Basic scoring logic implemented (`app/scoring.py`) with weights + recency decay + confidence blend.

### ❌ Missing / Gaps
- Endpoints do **not** match `docs/API_CONTRACT.md` (missing `/api/v1` base, map snapshot, country detail contract shape, timeline, alerts endpoints).
- Error envelope not standardized to contract.
- Data is in-memory sample list (`_SAMPLE_EVENTS`) with TODOs explicitly calling for Postgres ingestion.
- Deltas are hardcoded placeholders, not computed from persisted history.
- No POST ingestion endpoint backed by persistence.
- No pagination, filtering, rate limiting, auth, request IDs, or API versioning strategy.

---

## C) Data model + database

### ✅ Complete
- SQL schema and indexes exist with core entities (`countries`, `sources`, `events`, `features`, `scores`, `score_drivers`).
- Data model aligns with explainability intent (drivers linked to score/event/feature).
- Indexing is reasonable for MVP access patterns.

### ❌ Missing / Gaps
- No migration framework integrated in app path (Alembic or equivalent).
- No repository/ORM layer wired from API/scoring to DB.
- No raw-provider table lineage (`raw_events_*`) as suggested in research guidance.
- No ingestion-run tracking table integrated with code path.
- No partitioning/retention jobs; no archival workflows.

---

## D) Scoring engine, confidence model, anti-rumor

### ✅ Complete
- Basic weighted model exists (military/political/conflict/economic/credibility/spillover).
- Basic recency decay and confirmation bonus implemented.
- Basic confidence from reliability + corroboration + recency implemented.

### ❌ Missing / Gaps
- Research-spec components not implemented yet:
  - full M/P/E/I/H/B taxonomy at signal-code level (M1..B4)
  - robust normalization pipeline (winsorization + MAD z-score + sigmoid/tanh)
  - momentum/burst/volatility/persistence features
  - disagreement/coverage-aware confidence decomposition
  - rumor-likelihood ensemble and propagation dampening
  - source trust update loop (Bayesian reliability updates)
- No backtesting/calibration pipeline.
- No score guardrails for source outage/single-source spikes/sparse regions.

---

## E) Frontend map/dashboard

### ✅ Complete
- React + Vite app runs and renders map via `react-leaflet`.
- Hotspots list, legend, and country detail panel exist.
- API hook implemented with fallback sample data and 30s polling.
- UX includes loading and error states.

### ❌ Missing / Gaps
- Country representation is markers, not full country polygon choropleth.
- No 24h/7d/30d window toggle UI.
- No timeline chart component connected to backend.
- No alerts UX wired.
- Country detail panel assumes non-null country object (possible edge-case crash).
- Coordinate mapping is hardcoded for small subset.
- Internationalization/accessibility/perf testing minimal.

---

## F) Scheduler, operations, quality, and production hardening

### ✅ Complete
- None significant beyond local run capability.

### ❌ Missing / Gaps
- No scheduler/orchestrator (cron/APScheduler/Celery) integrated.
- No ingestion workers/adapters.
- No tests (`unit/integration/e2e`) present in repository.
- No CI/CD pipeline.
- No observability stack (structured logs, metrics, tracing).
- No secrets/config profile strategy for environments.
- No authn/authz plan if public API is exposed.

---

## 3) Production Readiness Gap Summary (By Priority)

## P0 (Blockers for real platform)
1. Build real ingestion + normalization + persistence pipeline.
2. Implement scheduler and deterministic scoring runs.
3. Align backend endpoints to API contract and wire DB-backed reads.
4. Replace static sample data and placeholder deltas with historical computations.

## P1 (High-impact quality)
5. Implement confidence decomposition + anti-rumor controls from research spec.
6. Add coverage/outage guardrails and score-jump controls.
7. Add test suite + CI gates.
8. Build frontend choropleth + timeline + window toggles.

## P2 (Scale + trust)
9. Add source reliability feedback loop and calibration/backtesting.
10. Add observability, SLOs, and ops runbooks.
11. Add alerts delivery and subscription lifecycle.

---

## 4) Recommended Immediate Execution Focus (Next 2 Weeks)

1. **Data backbone first**: adapters (ACLED/GDELT/UNHCR + baseline WB/FAO), canonical event model, DB repositories.
2. **Scoring v0.2 (explainable)**: category-level features + confidence breakdown + rumor gating.
3. **API contract lock**: `/api/v1/map/snapshot`, `/countries/{code}`, `/timeline`, strict response schemas.
4. **Frontend contract integration**: map + panel + timeline from real API (no sample fallback for staging).
5. **Scheduled runs**: hourly near-real-time + nightly recompute for consistency.

---

## 5) Verdict

GeoWar Pulse is currently a **well-documented MVP prototype** with partial implementation.  
To become a production-grade geopolitical risk platform, execution must now shift from UI/demo + conceptual docs to **data engineering, robust scoring pipeline, and contract-driven API + operations hardening**.