-- GeoWar Pulse MVP indexes

BEGIN;

-- countries
CREATE INDEX IF NOT EXISTS idx_countries_region ON countries(region);
CREATE INDEX IF NOT EXISTS idx_countries_active ON countries(is_active) WHERE is_active = TRUE;

-- sources
CREATE INDEX IF NOT EXISTS idx_sources_active ON sources(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_sources_type ON sources(source_type);

-- events
CREATE INDEX IF NOT EXISTS idx_events_country_occurred_at ON events(country_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_status_occurred_at ON events(status, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_source_reported_at ON events(source_id, reported_at DESC);
CREATE INDEX IF NOT EXISTS idx_events_penalized_claim ON events(is_penalized_claim) WHERE is_penalized_claim = TRUE;
CREATE INDEX IF NOT EXISTS idx_events_metadata_gin ON events USING GIN (metadata);

-- features
CREATE INDEX IF NOT EXISTS idx_features_country_observed_at ON features(country_id, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_features_bucket_window ON features(bucket, window_hours, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_features_key_country ON features(feature_key, country_id);

-- scores
CREATE INDEX IF NOT EXISTS idx_scores_country_as_of ON scores(country_id, as_of DESC);
CREATE INDEX IF NOT EXISTS idx_scores_window_as_of ON scores(window_hours, as_of DESC);
CREATE INDEX IF NOT EXISTS idx_scores_risk_desc ON scores(risk_score DESC, as_of DESC);
CREATE INDEX IF NOT EXISTS idx_scores_momentum ON scores(momentum_label, as_of DESC);

-- score drivers
CREATE INDEX IF NOT EXISTS idx_score_drivers_score_rank ON score_drivers(score_id, rank_order);
CREATE INDEX IF NOT EXISTS idx_score_drivers_feature ON score_drivers(feature_id) WHERE feature_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_score_drivers_event ON score_drivers(event_id) WHERE event_id IS NOT NULL;

COMMIT;
