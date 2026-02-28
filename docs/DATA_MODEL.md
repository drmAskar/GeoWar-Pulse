# Data Model (MVP)

This document defines the PostgreSQL model for GeoWar Pulse MVP and how it maps to `docs/SCORING_FRAMEWORK.md`.

## Design Goals
- Country-level risk snapshots with explainability.
- Clear separation of **reported** vs **confirmed** signals.
- Traceability from score → driver → feature/event → source.
- Time-windowed outputs for 24h / 7d / 30d.

## Entity Relationship Overview

- `countries` (1) -> (N) `events`
- `countries` (1) -> (N) `features`
- `countries` (1) -> (N) `scores`
- `sources` (1) -> (N) `events`
- `scores` (1) -> (N) `score_drivers`
- `features` (1) -> (N) `score_drivers` (optional link)
- `events` (1) -> (N) `score_drivers` (optional link)

`score_drivers` can reference either a `feature`, an `event`, or be a synthetic `penalty/adjustment` driver.

## Tables

### 1) countries
Country master data and map identity.

Key columns:
- `iso2`, `iso3`, `name` (unique identifiers)
- `region`, `subregion`
- `is_active`

### 2) sources
Signal provenance and base reliability.

Key columns:
- `source_type` (`official`, `wire`, `ngo`, `local_media`, `social`, `other`)
- `reliability_weight` (0..1)
- `default_credibility_tag` (`low`, `medium`, `high`)

### 3) events
Raw/normalized incidents and advisories.

Key columns:
- `status` (`reported`, `confirmed`, `retracted`) to enforce guardrail separation.
- `severity` (1..5)
- `confidence_score` (0..100)
- `confirmation_count` and `recency_decay_factor`
- `is_penalized_claim` for unverified viral claims
- `metadata` (JSONB) for adapter-specific attributes

### 4) features
Scoring-ready features aggregated by country/time window.

Key columns:
- `feature_key` (e.g., `force_mobilization`)
- `bucket` aligned to scoring framework buckets:
  - `military_signals`
  - `political_diplomatic`
  - `conflict_events`
  - `economic_stress`
  - `information_credibility`
  - `regional_spillover`
- `value`, `normalized_value`
- `window_hours` (24, 168, 720)
- `source_count`, `confidence_score`, `recency_decay_factor`

### 5) scores
Point-in-time scoring outputs per country/window.

Key columns:
- `risk_score` (0..100)
- `confidence_score` (0..100)
- `momentum_label` (`de-escalating`, `stable`, `escalating`)
- `delta_24h`, `delta_7d`
- `penalties`, `confidence_adjustment`
- `scoring_version` (defaults `v0.1`)

This table stores the composite output of:
`RiskScore = Σ(weight_i * feature_i) - penalties + confidence_adjustment`

### 6) score_drivers
Explainability layer for "why the score moved."

Key columns:
- `driver_key`, `driver_type` (`feature`, `event`, `penalty`, `adjustment`)
- `weight`, `raw_value`, `normalized_value`, `contribution`
- `direction` (`up`, `down`)
- `rank_order` (top-driver ordering)
- optional links to `feature_id` and/or `event_id`

## Alignment with Scoring Framework v0.1

- **Feature buckets**: enforced by `features.bucket` CHECK constraint.
- **Confidence score** inputs: represented through event/source reliability fields and feature confidence fields, then materialized into `scores.confidence_score`.
- **Momentum**: captured in `scores.delta_24h`, `scores.delta_7d`, and `scores.momentum_label`.
- **Guardrails**:
  - `events.status` separates reported vs confirmed.
  - `events.is_penalized_claim` supports unverified-claim penalty logic.
  - `score_drivers` supports explicit `penalty` entries for explainability.

## Retention Strategy (MVP)

### Keep indefinitely
- `countries`, `sources` (slow-changing reference data)
- `scores` and top `score_drivers` (historical analytics + auditability)

### Time-boxed retention
- `events`: keep hot data for 18 months; archive older rows to cold storage (object storage or archive DB).
- `features`: keep 12 months of materialized features (recomputable from events when needed).

### Rollups (future)
- Maintain daily rollups for `scores` for long-term trend visualization.
- Optionally compact `score_drivers` beyond top N per score after 12 months.

### Operational notes
- Partitioning is deferred for MVP, but schema/indexes are compatible with future time partitioning on:
  - `events.occurred_at`
  - `features.observed_at`
  - `scores.as_of`

## Load Order
1. `db/schema.sql`
2. `db/indexes.sql`
3. `db/seed.sql`
