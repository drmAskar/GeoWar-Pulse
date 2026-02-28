-- GeoWar Pulse MVP schema (PostgreSQL)
-- Aligns with docs/SCORING_FRAMEWORK.md v0.1

BEGIN;

CREATE TABLE IF NOT EXISTS countries (
  id              BIGSERIAL PRIMARY KEY,
  iso2            CHAR(2) NOT NULL UNIQUE,
  iso3            CHAR(3) NOT NULL UNIQUE,
  name            TEXT NOT NULL UNIQUE,
  region          TEXT,
  subregion       TEXT,
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sources (
  id                      BIGSERIAL PRIMARY KEY,
  name                    TEXT NOT NULL UNIQUE,
  source_type             TEXT NOT NULL CHECK (source_type IN ('official', 'wire', 'ngo', 'local_media', 'social', 'other')),
  base_url                TEXT,
  reliability_weight      NUMERIC(4,3) NOT NULL CHECK (reliability_weight >= 0 AND reliability_weight <= 1),
  default_credibility_tag TEXT NOT NULL CHECK (default_credibility_tag IN ('low', 'medium', 'high')),
  is_active               BOOLEAN NOT NULL DEFAULT TRUE,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events (
  id                      BIGSERIAL PRIMARY KEY,
  country_id              BIGINT NOT NULL REFERENCES countries(id) ON DELETE RESTRICT,
  source_id               BIGINT NOT NULL REFERENCES sources(id) ON DELETE RESTRICT,
  external_ref            TEXT,
  event_type              TEXT NOT NULL,
  status                  TEXT NOT NULL CHECK (status IN ('reported', 'confirmed', 'retracted')),
  title                   TEXT NOT NULL,
  summary                 TEXT,
  severity                SMALLINT NOT NULL CHECK (severity BETWEEN 1 AND 5),
  occurred_at             TIMESTAMPTZ NOT NULL,
  reported_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  verified_at             TIMESTAMPTZ,
  confidence_score        NUMERIC(5,2) NOT NULL DEFAULT 50 CHECK (confidence_score >= 0 AND confidence_score <= 100),
  confirmation_count      INTEGER NOT NULL DEFAULT 0 CHECK (confirmation_count >= 0),
  recency_decay_factor    NUMERIC(5,4) NOT NULL DEFAULT 1 CHECK (recency_decay_factor >= 0 AND recency_decay_factor <= 1),
  is_penalized_claim      BOOLEAN NOT NULL DEFAULT FALSE,
  metadata                JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(source_id, external_ref)
);

CREATE TABLE IF NOT EXISTS features (
  id                      BIGSERIAL PRIMARY KEY,
  country_id              BIGINT NOT NULL REFERENCES countries(id) ON DELETE RESTRICT,
  feature_key             TEXT NOT NULL,
  bucket                  TEXT NOT NULL CHECK (bucket IN (
                            'military_signals',
                            'political_diplomatic',
                            'conflict_events',
                            'economic_stress',
                            'information_credibility',
                            'regional_spillover'
                          )),
  value                   NUMERIC(10,4) NOT NULL,
  normalized_value        NUMERIC(10,4) CHECK (normalized_value >= 0 AND normalized_value <= 1),
  observed_at             TIMESTAMPTZ NOT NULL,
  window_hours            INTEGER NOT NULL CHECK (window_hours IN (24, 168, 720)),
  source_count            INTEGER NOT NULL DEFAULT 1 CHECK (source_count >= 0),
  confidence_score        NUMERIC(5,2) NOT NULL DEFAULT 50 CHECK (confidence_score >= 0 AND confidence_score <= 100),
  recency_decay_factor    NUMERIC(5,4) NOT NULL DEFAULT 1 CHECK (recency_decay_factor >= 0 AND recency_decay_factor <= 1),
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(country_id, feature_key, observed_at, window_hours)
);

CREATE TABLE IF NOT EXISTS scores (
  id                      BIGSERIAL PRIMARY KEY,
  country_id              BIGINT NOT NULL REFERENCES countries(id) ON DELETE RESTRICT,
  as_of                   TIMESTAMPTZ NOT NULL,
  window_hours            INTEGER NOT NULL CHECK (window_hours IN (24, 168, 720)),
  risk_score              NUMERIC(5,2) NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
  confidence_score        NUMERIC(5,2) NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 100),
  momentum_label          TEXT NOT NULL CHECK (momentum_label IN ('de-escalating', 'stable', 'escalating')),
  delta_24h               NUMERIC(6,2) NOT NULL DEFAULT 0,
  delta_7d                NUMERIC(6,2) NOT NULL DEFAULT 0,
  penalties               NUMERIC(8,4) NOT NULL DEFAULT 0,
  confidence_adjustment   NUMERIC(8,4) NOT NULL DEFAULT 0,
  scoring_version         TEXT NOT NULL DEFAULT 'v0.1',
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(country_id, as_of, window_hours, scoring_version)
);

CREATE TABLE IF NOT EXISTS score_drivers (
  id                      BIGSERIAL PRIMARY KEY,
  score_id                BIGINT NOT NULL REFERENCES scores(id) ON DELETE CASCADE,
  feature_id              BIGINT REFERENCES features(id) ON DELETE SET NULL,
  event_id                BIGINT REFERENCES events(id) ON DELETE SET NULL,
  driver_key              TEXT NOT NULL,
  driver_type             TEXT NOT NULL CHECK (driver_type IN ('feature', 'event', 'penalty', 'adjustment')),
  description             TEXT NOT NULL,
  weight                  NUMERIC(6,4),
  raw_value               NUMERIC(10,4),
  normalized_value        NUMERIC(10,4),
  contribution            NUMERIC(10,4) NOT NULL,
  direction               TEXT NOT NULL CHECK (direction IN ('up', 'down')),
  rank_order              SMALLINT NOT NULL CHECK (rank_order > 0),
  created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (feature_id IS NOT NULL OR event_id IS NOT NULL OR driver_type IN ('penalty', 'adjustment')),
  UNIQUE(score_id, driver_key, rank_order)
);

COMMIT;
