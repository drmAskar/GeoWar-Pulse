# GeoWar Pulse — Research Signal Taxonomy & Scoring Design

## Purpose
Design a robust, explainable signal system for **War Risk Score (0–100)** that is resilient to noise, propaganda, and rumor bursts.

This document defines:
- Signal taxonomy (what we measure)
- Feature formulas (how we quantify)
- Normalization (how features are made comparable)
- Confidence handling (how certainty affects impact)
- Recency decay (how old events lose influence)
- Anti-rumor penalties (how we suppress unverified hype)

---

## 1) Core Modeling Principles

1. **Probabilistic, not deterministic**
   - Score estimates escalation risk, not factual certainty of war.

2. **Event + trend hybrid**
   - Sudden events matter, but sustained trend shifts matter more than one-off spikes.

3. **Source-aware by design**
   - Every signal carries provenance and reliability weight.

4. **Cross-verified > single source**
   - Independent confirmation increases confidence and feature impact.

5. **Decayed memory**
   - New evidence dominates old evidence via time decay.

6. **Rumor resistance**
   - Unverified viral narratives should produce little or negative net contribution.

---

## 2) Signal Taxonomy (Hierarchical)

Each event is mapped to one or more categories and sub-signals.

## 2.1 Military & Force Posture (M)
- **M1 Troop movement**: mobilization, redeployment, border concentration
- **M2 Equipment movement**: armor/artillery/air defense transfers
- **M3 Air/naval activity**: patrol intensification, carrier positioning, air incursions
- **M4 Combat readiness**: reserve activation, readiness level changes, exercises near borders
- **M5 Kinetic incidents**: shelling, missile/drone strikes, clashes

## 2.2 Political & Diplomatic (P)
- **P1 Diplomatic rupture**: ambassador expulsion, closure, treaty suspension
- **P2 Escalatory rhetoric**: explicit threats, red-line framing, war language
- **P3 Peace signaling**: ceasefire negotiations, mediation progress (de-escalatory)
- **P4 Leadership instability**: emergency decrees, coup indicators, abrupt cabinet/security reshuffles

## 2.3 Economic & Strategic Pressure (E)
- **E1 Sanctions actions**: new sanctions, secondary sanctions, export controls
- **E2 Energy coercion**: pipeline disruptions, export weaponization
- **E3 Trade/logistics disruption**: chokepoints, blockades, port closures
- **E4 Defense-industrial surge**: rapid procurement / wartime production posture

## 2.4 Information, Cyber, and Irregular (I)
- **I1 Cyber operations**: critical infrastructure attacks, sustained campaigns
- **I2 Information warfare intensity**: coordinated disinfo spikes, bot-amplified narratives
- **I3 Legal/gray-zone acts**: maritime harassment, airspace probing, proxy activity
- **I4 Rumor/hoax prevalence**: unverified claims with viral propagation

## 2.5 Humanitarian & Civil Stress (H)
- **H1 Displacement/refugee flow acceleration**
- **H2 Civilian harm indicators**
- **H3 Internal unrest with armed potential**
- **H4 Emergency system strain** (hospital, grid, food logistics)

## 2.6 Structural Baseline Risk (B)
Slow-moving background priors, not immediate triggers.
- **B1 Historical conflict propensity**
- **B2 Border disputes / unresolved territorial claims**
- **B3 State fragility & governance stress**
- **B4 Alliance entanglement complexity**

---

## 3) Event Object Schema (Recommended)

```json
{
  "event_id": "uuid",
  "region_id": "ISO3 or custom",
  "timestamp": "UTC",
  "category": "M|P|E|I|H|B",
  "signal_code": "M1..B4",
  "direction": "escalatory|deescalatory",
  "base_severity": 0.0,
  "source_count": 3,
  "independent_source_count": 2,
  "source_reliability_mean": 0.78,
  "evidence_quality": 0.65,
  "geo_proximity": 0.9,
  "actor_relevance": 0.8,
  "rumor_flag": false,
  "rumor_score": 0.1,
  "text_sentiment_threat": 0.7,
  "metadata": {}
}
```

---

## 4) Feature Engineering

For each event *e* at time *t*:

### 4.1 Base Severity
`sev_e ∈ [0,1]`
- Derived from event type rules + NLP classifier + analyst override.
- Example heuristic anchors:
  - statement-level threat: 0.25
  - border troop concentration: 0.55
  - confirmed cross-border strike: 0.85

### 4.2 Directional Sign
`dir_e = +1` for escalatory, `-1` for de-escalatory.

### 4.3 Source Confidence Components
- `R_e`: mean reliability of sources (historical truthfulness), `[0,1]`
- `I_e`: independence factor (many unique outlets > many reposts), `[0,1]`
- `Q_e`: evidence quality (imagery/docs/official statement quality), `[0,1]`
- `V_e`: verification factor from corroboration counts, `[0,1]`

Suggested corroboration mapping:
`V_e = 1 - exp(-k * indep_source_count)` with `k≈0.7`.

Composite confidence:
`C_e = wR*R_e + wI*I_e + wQ*Q_e + wV*V_e`
with `(wR,wI,wQ,wV)=(0.35,0.20,0.20,0.25)`.

### 4.4 Context Multipliers
- `G_e`: geo proximity to contested zone `[0.5,1.2]`
- `A_e`: actor significance (major military/political actor) `[0.7,1.3]`
- `Sg_e`: signal-type calibration weight per taxonomy bucket (learned or expert-set)

### 4.5 Recency Decay
Use half-life by signal type:
- Kinetic incidents: 24–72h
- Force movements: 3–10d
- Diplomacy statements: 2–7d
- Structural baseline: 90–365d

Decay function:
`D_e(Δt) = 2^(-Δt / HL_signal)`
where `Δt` in hours/days aligned with `HL_signal` units.

### 4.6 Raw Event Contribution
`raw_e(t) = dir_e * sev_e * C_e * G_e * A_e * Sg_e * D_e(Δt)`

### 4.7 Rumor & Manipulation Penalty
Let `U_e` be unverified/rumor likelihood `[0,1]`.

Penalty multiplier:
`P_e = 1 - λ * U_e^γ`, with default `λ=0.8`, `γ=1.5`, clipped to `[0.1,1]`.

Event post-penalty contribution:
`contrib_e(t) = raw_e(t) * P_e`

Optional explicit negative trust shock for confirmed falsehood campaigns:
`trust_shock_e = -τ * U_e * virality_e` (applied to confidence layer)

---

## 5) Aggregation to Region-Time Features

For region *r* at time window *W*:

### 5.1 Category Scores
`CatScore_{r,c} = Σ_{e∈(r,c,W)} contrib_e`

### 5.2 Momentum Features
- `mom_24_7 = mean(last24h) - mean(prev7d)`
- `mom_7_30 = mean(last7d) - mean(prev30d)`
- `burst_index = events_last_24h / max(1, median_daily_events_30d)`

### 5.3 Volatility & Persistence
- `vol_7d = std(daily_contrib, 7d)`
- `persistence = days_with_signal_above_threshold / 14`

### 5.4 De-escalation Counterweight
Maintain separate escalatory and de-escalatory channels:
- `Esc_r = Σ max(contrib_e, 0)`
- `DeEsc_r = Σ |min(contrib_e, 0)|`

Net pressure:
`Net_r = Esc_r - α * DeEsc_r`, with `α` typically `0.8–1.2`.

---

## 6) Normalization Strategy

Goal: comparable scales across regions and categories.

### 6.1 Robust Per-Feature Scaling
For each continuous feature `x`:
1. Winsorize at `[p1, p99]`
2. Robust z-score:
   `z = (x - median_ref) / (1.4826 * MAD_ref + ε)`
3. Squash to bounded range:
   `x_norm = sigmoid(z)` (or rescale to `[-1,1]` by `2*sigmoid(z)-1`)

Use rolling reference window (e.g., 180d global + regional backoff).

### 6.2 Category Balance Normalization
To avoid one category dominating by volume:
`CatNorm_{r,c} = tanh(CatScore_{r,c} / scale_c)`
where `scale_c` is historical 95th percentile absolute score for category `c`.

### 6.3 Baseline Prior Fusion
Structural baseline prior `B_r` should be low-frequency and capped:
`B_norm = clip(B_r, 0, 1)`
It biases score but cannot create sudden spikes alone.

---

## 7) Confidence Modeling (Score-Level)

Separate **risk level** from **confidence in that level**.

### 7.1 Effective Evidence Volume
`N_eff = Σ (I_e * D_e)` over recent window.

### 7.2 Agreement / Consistency
`A_cons = 1 - disagreement_index`
where disagreement measures contradictory high-confidence claims.

### 7.3 Data Freshness/Coverage
`F_cov` based on source latency, missing feeds, and regional blind spots.

### 7.4 Final Confidence Score
`Conf_r = 100 * clip( w1*mean(C_e) + w2*f(N_eff) + w3*A_cons + w4*F_cov - rumor_drag, 0, 1 )`

`f(N_eff)` can be saturation: `1 - exp(-N_eff/θ)`.
`rumor_drag = ρ * rumor_share_recent`.

Recommended starting weights: `(w1,w2,w3,w4)=(0.35,0.25,0.20,0.20)`.

---

## 8) War Risk Score Formula (0–100)

### 8.1 Linear-Explainable Core
Let normalized feature vector for region r be `X_r` containing:
- `CatNorm_{r,M..H}`
- momentum metrics
- burst/volatility/persistence
- baseline prior `B_norm`

Raw logit:
`L_r = β0 + Σ_i β_i * X_{r,i}`

Probability-like risk:
`p_r = sigmoid(L_r)`

Confidence-adjusted (optional conservative shrinkage):
`p'_r = 0.5 + (p_r - 0.5) * (Conf_r/100)^η` with `η≈0.7`

Final score:
`RiskScore_r = round(100 * p'_r)`

### 8.2 Momentum Label
- escalating: `mom_24_7 > t_up`
- de-escalating: `mom_24_7 < -t_down`
- stable: otherwise

Thresholds from historical quantiles (e.g., 60th percentile absolute momentum).

---

## 9) Anti-Rumor System (Detailed)

## 9.1 Rumor Likelihood Inputs
`U_e` from ensemble:
- low-source-diversity + high repost ratio
- claim novelty without corroboration after time lag
- sensational linguistic markers
- known disinfo-domain fingerprints
- mismatch with geospatial/OSINT constraints

## 9.2 Rumor Impact Rules
1. **Low confidence gate**: if `C_e < c_min` and `U_e > u_high`, set `contrib_e ≈ 0`.
2. **Penalty scaling**: apply `P_e` multiplier as above.
3. **Propagation dampener**: repeated near-duplicate rumor events share a capped total impact.
4. **Falsehood back-propagation**: once disproven, reverse prior contribution and lower trust for originating sources.

### 9.3 Source Trust Update
Per source s, maintain reliability prior `Rel_s`.
Update via Bayesian/Beta style:
- true verified reports increment alpha
- false or retracted reports increment beta
- `Rel_s = alpha/(alpha+beta)`

Use recency-weighted updates to forgive very old mistakes slowly.

---

## 10) Calibration & Validation Plan

1. **Backtesting windows**: evaluate on known escalation episodes and calm periods.
2. **Lead-time metric**: how early risk crosses threshold before major incidents.
3. **False alarm control**: alert precision/recall across regions.
4. **Reliability calibration**: Brier score / calibration curves for risk bins.
5. **Ablation tests**: remove each category and rumor controls to quantify contribution.
6. **Human analyst review**: compare top drivers with expert narrative plausibility.

---

## 11) Explainability Output (for UI/API)

For each region score emission, include:
- top positive contributors (event/category)
- top de-escalatory contributors
- confidence decomposition (`source quality`, `coverage`, `agreement`)
- rumor suppression note if material (e.g., “18% of viral claims down-weighted due to low verification”)
- recency profile (how much score is from last 24h vs 7d vs older)

This supports “why score moved” and analyst trust.

---

## 12) Suggested Initial Weights (MVP defaults)

Category weights (in linear model features):
- Military (M): 0.30
- Political/Diplomatic (P): 0.18
- Economic (E): 0.12
- Info/Cyber/Irregular (I): 0.14
- Humanitarian/Civil (H): 0.16
- Baseline (B): 0.10

Notes:
- Keep baseline low to avoid static overprediction.
- Military + humanitarian often provide strongest near-term escalation cues.
- Retrain/tune quarterly or after major regime changes in data sources.

---

## 13) Implementation Blueprint (Backend)

1. **Ingest** event + source metadata
2. **Classify** taxonomy + severity + direction
3. **Score event-level** (`raw_e`, rumor penalty, decay)
4. **Aggregate** by region/category/time
5. **Normalize** robustly vs reference distributions
6. **Model inference** for risk probability + confidence
7. **Persist** score + feature attributions + diagnostics
8. **Serve** API payload for map + trend + explanations

---

## 14) Guardrails & Failure Modes

- **Data outage guardrail**: if major feeds missing, reduce confidence and freeze aggressive jumps.
- **Single-source spike guardrail**: cap contribution from one source cluster.
- **Regional sparsity guardrail**: apply prior and uncertainty widening where data is sparse.
- **Adversarial narrative attack**: detect coordinated rumor bursts and lower system sensitivity to repost storms.

---

## 15) Minimal MVP Feature Set (if constrained)

If shipping quickly, keep only:
1. Taxonomy M/P/E/I/H + severity/direction
2. Confidence composite `C_e`
3. Recency decay by category
4. Rumor penalty `P_e`
5. Category aggregation + robust normalization
6. Linear logit → 0–100 risk
7. Separate confidence score + top drivers

Then iterate with advanced calibration and source-trust learning.

---

## Summary
This framework produces an explainable, source-aware, rumor-resistant conflict-risk signal stack. It balances immediate incidents with trend persistence, separates risk from confidence, and explicitly penalizes unverifiable viral claims to reduce false alarms in high-noise geopolitical environments.
