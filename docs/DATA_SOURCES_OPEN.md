# GeoWar Pulse — OPEN Data Sources by Risk Factor (Production-Oriented)

**Goal:** practical, immediately implementable open-source stack for global country-level risk scoring.  
**Legend:** Reliability (A high → C medium), Integration complexity (Low/Med/High).

---

## 1) Military (M)

## Primary
1. **ACLED API / exports**  
   - Coverage: political violence, armed clashes, strategic military developments  
   - Update: weekly curated refresh  
   - Reliability: **A-**  
   - Complexity: **Medium** (API/export handling + taxonomy mapping)  
   - Use: M1/M2/M4/M5 event backbone

2. **GDELT 2.1 Events (CAMEO)**  
   - Coverage: machine-coded global event stream from news  
   - Update: ~15 minutes  
   - Reliability: **B** (fast but noisy)  
   - Complexity: **Medium-High** (dedupe/filtering essential)  
   - Use: near-real-time early signal for force movement, incidents, maritime/air probes

## Secondary
3. **UCDP GED/API**  
   - Coverage: organized violence with strict methodology  
   - Update: slower/versioned releases  
   - Reliability: **A**  
   - Complexity: **Medium**  
   - Use: calibration anchor / backtesting truth layer

4. **SIPRI open datasets**  
   - Coverage: military expenditure, arms transfer (structural)  
   - Update: annual  
   - Reliability: **A/B**  
   - Complexity: **Low**  
   - Use: baseline military posture, not short-term trigger

---

## 2) Political & Diplomatic (P)

## Primary
1. **GDELT Events + GKG**  
   - Update: ~15 min  
   - Reliability: **B**  
   - Complexity: **Medium-High**  
   - Use: diplomatic rupture, escalatory rhetoric, peace-talk mentions (with strict confidence gates)

2. **UN Digital Library / UN press feeds (open)**  
   - Update: daily/event-driven  
   - Reliability: **A/B**  
   - Complexity: **Medium** (RSS/API parsing varies)  
   - Use: official diplomatic statements and resolutions

## Secondary
3. **Curated official government MFA/RSS feeds (open web)**  
   - Update: event-driven  
   - Reliability: **B** (official but political framing)  
   - Complexity: **High** (many adapters, language variance)  
   - Use: high-value country-specific diplomatic actions

---

## 3) Economic & Strategic Pressure (E)

## Primary
1. **World Bank Data API (WDI/WGI)**  
   - Update: periodic/annual  
   - Reliability: **A**  
   - Complexity: **Low**  
   - Use: structural economic/governance priors

2. **IMF public datasets (WEO/IFS where accessible)**  
   - Update: monthly/quarterly/annual mixed  
   - Reliability: **A**  
   - Complexity: **Medium** (series harmonization)  
   - Use: macro stress (inflation, reserves, external pressure)

3. **FAO/FAOSTAT + FAO Food Price Index**  
   - Update: monthly (plus periodic datasets)  
   - Reliability: **A/B**  
   - Complexity: **Low-Medium**  
   - Use: food stress risk amplifier

## Secondary
4. **Public market benchmarks (Brent/WTI, key commodity proxies)**  
   - Update: daily/intraday depending source  
   - Reliability: **A/B**  
   - Complexity: **Low-Medium**  
   - Use: exogenous stress multipliers

---

## 4) Cyber / Information / Irregular (I)

## Primary
1. **GDELT GKG + Mentions**  
   - Update: ~15 min  
   - Reliability: **B**  
   - Complexity: **Medium-High**  
   - Use: disinformation intensity, narrative volatility, actor-based info warfare proxies

2. **NVD (National Vulnerability Database) feeds (open)**  
   - Update: daily/continuous feed publication  
   - Reliability: **A-** (for vulnerability disclosures, not attacks)  
   - Complexity: **Low-Medium**  
   - Use: cyber exposure baseline (state capacity stress context)

## Secondary
3. **CISA advisories / CERT open bulletins (where available)**  
   - Update: event-driven  
   - Reliability: **A/B**  
   - Complexity: **Medium**  
   - Use: verified cyber campaign signals (limited global consistency)

4. **Google Trends (context only)**  
   - Update: daily/weekly granularity  
   - Reliability: **C**  
   - Complexity: **Low**  
   - Use: public attention anomalies; should affect confidence/momentum more than core risk

---

## 5) Humanitarian & Civil Stress (H)

## Primary
1. **UNHCR Refugee Data API**  
   - Update: often monthly or better by stream  
   - Reliability: **A**  
   - Complexity: **Low-Medium**  
   - Use: displacement acceleration (H1)

2. **OCHA HDX (CKAN API)**  
   - Update: dataset-specific, often frequent in crises  
   - Reliability: **B**  
   - Complexity: **Medium-High** (heterogeneous formats/quality)  
   - Use: affected population, humanitarian access, emergency system strain

## Secondary
3. **WHO emergency/public health indicators (open)**  
   - Update: periodic  
   - Reliability: **B**  
   - Complexity: **Medium**  
   - Use: health-system stress as fragility component

---

## 6) Baseline Structural Risk (B)

## Primary
1. **World Bank WGI + WDI**  
   - Update: annual/periodic  
   - Reliability: **A**  
   - Complexity: **Low**  
   - Use: governance fragility, institutional capacity, economic resilience

2. **UCDP historical conflict data**  
   - Update: versioned/periodic  
   - Reliability: **A**  
   - Complexity: **Medium**  
   - Use: conflict propensity priors

3. **SIPRI structural military indicators**  
   - Update: annual  
   - Reliability: **A/B**  
   - Complexity: **Low**  
   - Use: long-term militarization baseline

---

## 7) Recommended MVP Source Stack (OPEN, practical now)

## Phase MVP-1 (ship quickly)
- ACLED (curated incidents)
- GDELT Events + GKG (high-frequency nowcast)
- UNHCR (displacement)
- World Bank + FAO (structural + food stress)

## Phase MVP-2 (quality lift)
- UCDP (validation/calibration anchor)
- IMF series integration
- OCHA HDX crisis layers

## Phase MVP-3 (robustness and explainability depth)
- CERT/CISA/NVD cyber context package
- SIPRI baseline enrichment
- Additional official diplomatic feeds adapters

---

## 8) Source Governance Rules (must implement)

1. **No major score jump from a single noisy source** (especially machine-coded stream alone).  
2. **Tier-aware weighting:** A/A- sources dominate confidence and score moves.  
3. **Rumor gate:** low corroboration + high virality => down-weight to near-zero contribution.  
4. **Freshness SLA per provider** with confidence penalty when stale.  
5. **Provider lineage in every score explanation** (source, timestamp, verification state).

---

## 9) Integration Complexity Summary

- **Low complexity quick wins:** World Bank, FAO, UNHCR, SIPRI  
- **Medium complexity core value:** ACLED, UCDP, IMF  
- **High complexity but high nowcast value:** GDELT (needs dedupe/noise controls), OCHA HDX multi-format harmonization, multi-government diplomatic adapters

---

## 10) Practical Final Recommendation

For immediate execution, build around **ACLED + GDELT + UNHCR + World Bank/FAO**, then stabilize with **UCDP/IMF**.  
This gives the best speed/coverage/trust tradeoff while staying open-data and explainable.