-- GeoWar Pulse MVP seed data

BEGIN;

-- Countries
INSERT INTO countries (iso2, iso3, name, region, subregion)
VALUES
  ('UA', 'UKR', 'Ukraine', 'Europe', 'Eastern Europe'),
  ('IL', 'ISR', 'Israel', 'Asia', 'Western Asia'),
  ('TW', 'TWN', 'Taiwan', 'Asia', 'Eastern Asia'),
  ('PL', 'POL', 'Poland', 'Europe', 'Eastern Europe')
ON CONFLICT (iso2) DO UPDATE
SET iso3 = EXCLUDED.iso3,
    name = EXCLUDED.name,
    region = EXCLUDED.region,
    subregion = EXCLUDED.subregion,
    updated_at = NOW();

-- Sources
INSERT INTO sources (name, source_type, base_url, reliability_weight, default_credibility_tag)
VALUES
  ('Reuters', 'wire', 'https://www.reuters.com', 0.92, 'high'),
  ('UN OCHA', 'official', 'https://www.unocha.org', 0.90, 'high'),
  ('Local Monitor Feed', 'local_media', NULL, 0.62, 'medium')
ON CONFLICT (name) DO UPDATE
SET source_type = EXCLUDED.source_type,
    base_url = EXCLUDED.base_url,
    reliability_weight = EXCLUDED.reliability_weight,
    default_credibility_tag = EXCLUDED.default_credibility_tag,
    updated_at = NOW();

-- Events
WITH c AS (
  SELECT id, iso2 FROM countries WHERE iso2 IN ('UA', 'IL', 'TW')
), s AS (
  SELECT id, name FROM sources WHERE name IN ('Reuters', 'UN OCHA', 'Local Monitor Feed')
)
INSERT INTO events (
  country_id, source_id, external_ref, event_type, status, title, summary,
  severity, occurred_at, reported_at, verified_at,
  confidence_score, confirmation_count, recency_decay_factor, is_penalized_claim, metadata
)
VALUES
  (
    (SELECT id FROM c WHERE iso2 = 'UA'),
    (SELECT id FROM s WHERE name = 'Reuters'),
    'reuters-ua-001',
    'cross_border_strike',
    'confirmed',
    'Cross-border strike reported near industrial zone',
    'Multiple independent outlets corroborated the incident.',
    4,
    NOW() - INTERVAL '5 hours',
    NOW() - INTERVAL '4 hours',
    NOW() - INTERVAL '3 hours',
    84,
    3,
    0.96,
    FALSE,
    '{"tags": ["military", "infrastructure"]}'::jsonb
  ),
  (
    (SELECT id FROM c WHERE iso2 = 'IL'),
    (SELECT id FROM s WHERE name = 'UN OCHA'),
    'ocha-il-001',
    'security_advisory',
    'reported',
    'Security advisory escalated for border-adjacent districts',
    'Advisory level raised pending further verification.',
    3,
    NOW() - INTERVAL '8 hours',
    NOW() - INTERVAL '7 hours',
    NULL,
    66,
    1,
    0.90,
    FALSE,
    '{"tags": ["advisory", "diplomatic"]}'::jsonb
  ),
  (
    (SELECT id FROM c WHERE iso2 = 'TW'),
    (SELECT id FROM s WHERE name = 'Local Monitor Feed'),
    'lmf-tw-viral-001',
    'naval_disruption_claim',
    'reported',
    'Unverified social footage claims naval disruption',
    'Claim is currently unconfirmed and flagged for penalty.',
    2,
    NOW() - INTERVAL '10 hours',
    NOW() - INTERVAL '9 hours',
    NULL,
    38,
    0,
    0.82,
    TRUE,
    '{"tags": ["viral_claim", "naval"], "note": "penalized until confirmed"}'::jsonb
  )
ON CONFLICT (source_id, external_ref) DO NOTHING;

-- Features (aligned to scoring buckets)
WITH c AS (
  SELECT id, iso2 FROM countries WHERE iso2 IN ('UA', 'IL', 'TW')
)
INSERT INTO features (
  country_id, feature_key, bucket, value, normalized_value,
  observed_at, window_hours, source_count, confidence_score, recency_decay_factor
)
VALUES
  ((SELECT id FROM c WHERE iso2 = 'UA'), 'force_mobilization', 'military_signals', 73, 0.73, NOW(), 24, 3, 82, 0.97),
  ((SELECT id FROM c WHERE iso2 = 'UA'), 'verified_incident_rate', 'conflict_events', 68, 0.68, NOW(), 24, 2, 80, 0.95),
  ((SELECT id FROM c WHERE iso2 = 'IL'), 'official_escalation_language', 'political_diplomatic', 61, 0.61, NOW(), 24, 2, 70, 0.94),
  ((SELECT id FROM c WHERE iso2 = 'IL'), 'shipping_insurance_stress', 'economic_stress', 40, 0.40, NOW(), 24, 2, 65, 0.92),
  ((SELECT id FROM c WHERE iso2 = 'TW'), 'viral_claim_penalty_proxy', 'information_credibility', 25, 0.25, NOW(), 24, 1, 42, 0.88),
  ((SELECT id FROM c WHERE iso2 = 'TW'), 'neighbor_incident_propagation', 'regional_spillover', 54, 0.54, NOW(), 24, 2, 60, 0.90)
ON CONFLICT (country_id, feature_key, observed_at, window_hours) DO NOTHING;

-- Scores
WITH c AS (
  SELECT id, iso2 FROM countries WHERE iso2 IN ('UA', 'IL', 'TW')
)
INSERT INTO scores (
  country_id, as_of, window_hours, risk_score, confidence_score,
  momentum_label, delta_24h, delta_7d, penalties, confidence_adjustment, scoring_version
)
VALUES
  ((SELECT id FROM c WHERE iso2 = 'UA'), NOW(), 24, 71.40, 83.20, 'escalating', 6.80, 11.20, 0.00, 1.15, 'v0.1'),
  ((SELECT id FROM c WHERE iso2 = 'IL'), NOW(), 24, 56.10, 69.40, 'stable', 1.70, 5.10, 0.00, 0.55, 'v0.1'),
  ((SELECT id FROM c WHERE iso2 = 'TW'), NOW(), 24, 48.30, 57.90, 'escalating', 4.20, 7.00, 4.50, -0.90, 'v0.1')
ON CONFLICT (country_id, as_of, window_hours, scoring_version) DO NOTHING;

-- Score drivers (top reasons behind score movement)
WITH latest_scores AS (
  SELECT s.*,
         ROW_NUMBER() OVER (PARTITION BY s.country_id ORDER BY s.as_of DESC) AS rn
  FROM scores s
  WHERE s.window_hours = 24 AND s.scoring_version = 'v0.1'
),
country_map AS (
  SELECT c.id AS country_id, c.iso2
  FROM countries c
  WHERE c.iso2 IN ('UA', 'IL', 'TW')
),
feature_map AS (
  SELECT f.id, f.country_id, f.feature_key
  FROM features f
  WHERE f.window_hours = 24
),
event_map AS (
  SELECT e.id, e.country_id, e.external_ref
  FROM events e
)
INSERT INTO score_drivers (
  score_id, feature_id, event_id, driver_key, driver_type, description,
  weight, raw_value, normalized_value, contribution, direction, rank_order
)
VALUES
  (
    (SELECT ls.id FROM latest_scores ls JOIN country_map cm ON cm.country_id = ls.country_id WHERE cm.iso2 = 'UA' AND ls.rn = 1),
    (SELECT fm.id FROM feature_map fm JOIN country_map cm ON cm.country_id = fm.country_id WHERE cm.iso2 = 'UA' AND fm.feature_key = 'force_mobilization'),
    (SELECT em.id FROM event_map em JOIN country_map cm ON cm.country_id = em.country_id WHERE cm.iso2 = 'UA' AND em.external_ref = 'reuters-ua-001'),
    'force_mobilization', 'feature', 'Elevated mobilization and verified strike activity',
    0.30, 73, 0.73, 21.90, 'up', 1
  ),
  (
    (SELECT ls.id FROM latest_scores ls JOIN country_map cm ON cm.country_id = ls.country_id WHERE cm.iso2 = 'IL' AND ls.rn = 1),
    (SELECT fm.id FROM feature_map fm JOIN country_map cm ON cm.country_id = fm.country_id WHERE cm.iso2 = 'IL' AND fm.feature_key = 'official_escalation_language'),
    (SELECT em.id FROM event_map em JOIN country_map cm ON cm.country_id = em.country_id WHERE cm.iso2 = 'IL' AND em.external_ref = 'ocha-il-001'),
    'official_escalation_language', 'feature', 'Escalatory rhetoric and elevated advisories',
    0.20, 61, 0.61, 12.20, 'up', 1
  ),
  (
    (SELECT ls.id FROM latest_scores ls JOIN country_map cm ON cm.country_id = ls.country_id WHERE cm.iso2 = 'TW' AND ls.rn = 1),
    (SELECT fm.id FROM feature_map fm JOIN country_map cm ON cm.country_id = fm.country_id WHERE cm.iso2 = 'TW' AND fm.feature_key = 'viral_claim_penalty_proxy'),
    (SELECT em.id FROM event_map em JOIN country_map cm ON cm.country_id = em.country_id WHERE cm.iso2 = 'TW' AND em.external_ref = 'lmf-tw-viral-001'),
    'unverified_viral_claim_penalty', 'penalty', 'Penalty applied due to unverified viral claim',
    NULL, 1, NULL, -4.50, 'down', 1
  )
ON CONFLICT (score_id, driver_key, rank_order) DO NOTHING;

COMMIT;
