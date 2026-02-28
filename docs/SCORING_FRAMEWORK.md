# Scoring Framework v0.1

## Composite Index
`RiskScore = Σ(weight_i * feature_i) - penalties + confidence_adjustment`

## Feature Buckets
1. **Military Signals (30%)**
   - force mobilization
   - cross-border strikes
   - airspace/naval disruptions
2. **Political & Diplomatic (20%)**
   - official escalation language
   - failed/paused negotiations
   - embassy/security advisories
3. **Conflict Events (20%)**
   - count/severity/frequency of verified incidents
4. **Economic Stress (10%)**
   - oil/gold/shipping-insurance stress proxies
5. **Information Credibility (10%)**
   - source reliability and cross-source confirmation
6. **Regional Spillover (10%)**
   - neighboring-country incident propagation

## Confidence Score (0–100)
- source reliability weighting
- independent confirmation count
- recency decay

## Momentum
- `delta_24h` and `delta_7d` drive trend labels:
  - De-escalating
  - Stable
  - Escalating

## Guardrails
- Penalize unverified viral claims
- Separate **"reported"** from **"confirmed"** events
- Never present certainty language
