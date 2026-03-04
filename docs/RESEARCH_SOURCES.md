# GeoWar Pulse — Research Brief: Public/Global Data Sources for Conflict Risk Scoring

_Last updated: 2026-02-28 (UTC)_

## 1) Scope and selection criteria

This brief catalogs high-value **public/global** datasets for a country-level conflict risk score, grouped into:

1. **Official / institutional structural indicators**
2. **Event datasets (battle/violence/protest/terrorism records)**
3. **Media and near-real-time text/event streams**
4. **Market stress proxies (commodity/financial pressure signals)**

Each source is rated for reliability and operational use with:
- reliability tier,
- update cadence,
- access method,
- key risks/biases.

---

## 2) Reliability tiers used in this brief

- **Tier A (High-trust anchor)**: transparent methodology, long history, widely cited, stable maintenance.
- **Tier B (Strong but with limitations)**: high utility, but known coverage/latency/standardization constraints.
- **Tier C (Useful contextual signal)**: informative but noisier, weaker governance, or less reproducible.
- **Tier D (Experimental/auxiliary)**: potentially useful for nowcasting but high bias/noise and should not drive scores alone.

---

## 3) Source inventory (recommended)

## A) Official / institutional structural & humanitarian indicators

| Source | Type | Reliability | Typical cadence | Access | Strengths | Risks / biases |
|---|---|---:|---|---|---|---|
| **World Bank WDI / WGI** | Macro + governance baseline | A | Annual / periodic | API + bulk CSV | Global coverage; cross-country comparability; core structural priors | Lagged (not crisis-nowcast); governance indicators may embed perception bias |
| **IMF datasets (WEO/IFS, debt, BOP where public)** | Macro vulnerability | A | Monthly/quarterly/annual mix | API/portal/download | Strong macro stress context (inflation, external balances, reserves) | Publication lag; revisions can backfill history |
| **UNHCR Refugee Data API** | Forced displacement pressure | A | Frequent (often monthly or better) | API | Direct humanitarian/conflict spillover signal | Reporting lag by country; registration quality varies |
| **UN OCHA HDX datasets** | Humanitarian operations + crisis layers | B | Dataset-specific | CKAN API + files | Useful crisis overlays (access constraints, affected population, etc.) | Highly heterogeneous quality and timeliness across datasets |
| **FAOSTAT / FAO Food Price Index** | Food stress (global + some country indicators) | A/B | Monthly | API/download | Strong signal where food shocks fuel unrest risk | National transmission from global prices is uneven |
| **WHO emergency / health burden indicators (selected)** | Health-system stress context | B | Periodic | API/download/reports | Adds fragility context (epidemic + capacity stress) | Not conflict-specific; significant reporting heterogeneity |
| **SIPRI (military expenditure/transfers)** | Security capacity + arms flows | A/B | Annual | Download | Valuable medium-term military posture features | Low-frequency; weak for short-term escalation timing |

### Notes
- Use these as **baseline risk and vulnerability priors**, not as immediate triggers.
- These features stabilize model behavior and reduce overreaction to media spikes.

---

## B) Conflict/event datasets (core for incident-based scoring)

| Source | Type | Reliability | Typical cadence | Access | Strengths | Risks / biases |
|---|---|---:|---|---|---|---|
| **ACLED** | Political violence, demonstrations, strategic developments (event-level geocoded) | A- | Weekly publication (near-real-time coding) | API + export files | Very strong global subnational event coverage; rich actor taxonomy | Media/reporting dependence; variable local visibility; occasional recoding/backfills |
| **UCDP GED / UCDP API** | Organized violence with strict definitions | A | Versioned releases (typically slower than ACLED, often annual major updates) | API + downloads + codebooks | Methodological rigor, academic gold standard definitions | Lower real-time responsiveness; conservative coding thresholds |
| **GTD (START)** | Terrorism incidents historical panel | A- | Periodic major releases (commonly annual, with lag) | Download (registration) | Long horizon, strong for structural terrorism risk | Significant reporting/publication lag; weaker for immediate nowcasting |
| **GDELT Events (CAMEO-based)** | Machine-coded global events from news | B | ~15-min updates | Open files/BigQuery/API ecosystem | Ultra-fast refresh, broad language/media intake | High noise; duplicate/churn risk; coding artifacts; media attention bias |
| **ICEWS** | Machine-coded political events (research dataset) | B/C | Release-dependent | Dataverse/files | Useful for historical modeling and CAMEO-style features | Access/versioning friction; not true live production feed |
| **SCAD / Mass mobilization datasets (where available)** | Protest/social disorder records | B/C | Periodic | Download | Adds protest/riot specialization missing in some pipelines | Regional or temporal limits; coder/interpreter subjectivity |

### Notes
- **Best practice**: combine one **human-curated event dataset** (ACLED/UCDP) with one **machine-speed stream** (GDELT) to balance precision vs latency.
- De-duplication and event harmonization are mandatory when combining sources.

---

## C) Media, narrative, and text-based risk signals

| Source | Type | Reliability | Typical cadence | Access | Strengths | Risks / biases |
|---|---|---:|---|---|---|---|
| **GDELT GKG / Mentions** | Global themes, sentiment, actor/media attention | B | ~15 min | Open files/BigQuery/API ecosystem | Strong for narrative momentum and attention shocks | Sentiment quality varies by language/domain; susceptible to media amplification cycles |
| **Google Trends (topic-level)** | Search attention and concern | C | Daily/weekly granularity | API wrappers/web | Fast population attention proxy for instability signals | Sampling opacity; internet penetration bias; not direct conflict measure |
| **Wikidata/Wikipedia pageview signals (selected)** | Public attention / salience | C | Daily/hourly | APIs | Cheap and global; helpful for anomaly detection | Strong geography/platform bias; easy to overfit to news cycles |
| **Major newsroom RSS aggregations (curated)** | Headline flow | C | Near-real-time | RSS/API | Operationally simple and transparent source lists | Editorial and geopolitical bias; language imbalance; duplicate stories |

### Notes
- Treat these as **leading but noisy** features.
- Use robust normalization (z-scores, rolling baselines, language-region controls).

---

## D) Market stress proxies (indirect conflict-pressure channels)

| Proxy source | Signal | Reliability | Typical cadence | Access | Why it matters | Risks / biases |
|---|---|---:|---|---|---|---|
| **Brent/WTI crude benchmarks** | Energy shock pressure | A | Daily/intraday | Public market data portals/APIs | Energy shocks correlate with fiscal stress/import burden/social pressure | Global benchmark may not reflect local subsidy/pass-through realities |
| **Wheat/maize/rice global benchmarks + FAO food prices** | Food affordability stress | A/B | Daily (futures) + monthly (FAO) | Exchanges/public portals/API | Food price spikes can precede unrest in import-dependent states | Local stocks/subsidies/policy buffers can mute effect |
| **FX stress (USD strength, local FX depreciation where available)** | External financing and inflation stress | B | Daily | Central bank/FRED/market feeds | Captures pressure on imports, debt servicing, and inflation | Capital controls and managed pegs distort comparability |
| **Sovereign risk proxies (bond spreads/EMBI-like, CDS where accessible)** | Perceived default/political risk | B/C | Daily | Mixed (many series paid; some proxies public) | Fast market-based stress signal | Coverage gaps for low-income/conflict states; market illiquidity artifacts |
| **VIX / global risk-off indicators** | Global risk sentiment regime | B | Intraday/daily | Public feeds | Useful regime-switch control feature | Very indirect for country conflict dynamics |
| **Shipping/freight disruption indicators (e.g., Baltic indices, route disruptions)** | Trade/logistics pressure | C | Daily | Public feeds | Useful for conflict spillover and chokepoint stress | Not country-specific; noisy causal link |

### Notes
- Market features should be modeled as **exogenous stress multipliers**, not direct conflict labels.
- Interaction terms matter: e.g., food shock × import dependence × governance weakness.

---

## 4) Recommended “best available” source stack by role

## Core production stack (MVP)

1. **ACLED** (event backbone, weekly curated)
2. **UCDP API/GED** (methodological anchor + cross-check)
3. **GDELT Events + GKG** (high-frequency nowcast layer)
4. **World Bank/IMF/UNHCR** (structural vulnerability + displacement)
5. **Food/energy market proxies** (external stress multipliers)

This combination balances:
- **speed** (GDELT),
- **event fidelity** (ACLED/UCDP),
- **structural context** (WB/IMF/UN),
- **economic stress transmission** (commodities/FX/spreads).

## Secondary enrichment layer (Phase 2)

- GTD for terrorism-specific historical priors,
- OCHA/HDX crisis layers,
- curated news/RSS + Trends/pageviews for narrative shocks,
- SIPRI annual military features.

---

## 5) Access patterns and integration guidance

## Ingestion pattern

- **Streaming/near-real-time:** GDELT (15-min batches)
- **Weekly:** ACLED refresh and re-score
- **Monthly/quarterly:** macro/humanitarian updates (IMF/FAO/UNHCR etc.)
- **Annual structural backfill:** WGI/SIPRI/GTD-style releases

## Storage model (recommended)

- `raw_events_*` tables per provider (immutable snapshots)
- `normalized_events` canonical schema (country, date, actor class, severity, source)
- `feature_store_daily_country` (lagged, rolled, standardized features)
- `score_outputs` with full lineage (`model_version`, `source_version`, `asof`)

## Quality controls

- source-level freshness monitors,
- anomaly guards (sudden zeroes/spikes by source-country),
- duplicate resolution across ACLED/GDELT-like records,
- confidence score weighted by source tier + recency + cross-source agreement.

---

## 6) Bias/risk register (must be explicit in model docs)

1. **Media visibility bias**: underreported rural/closed regimes look falsely calm.
2. **Language bias**: non-English and low-digital ecosystems can be underweighted unless multilingual pipelines are robust.
3. **Definition mismatch**: ACLED/UCDP/GDELT event taxonomies differ; direct count comparison is invalid without mapping.
4. **Latency mismatch**: structural data lag vs event data speed can create contradictory signals.
5. **Revision risk**: historical event backfills/reclassifications can silently shift training labels.
6. **Market proxy distortion**: global prices do not map 1:1 to domestic hardship due to subsidies/controls.
7. **Urban bias**: many open sources overweight cities vs periphery.

Mitigation: publish confidence/coverage flags, keep per-source uncertainty, and avoid single-source score moves.

---

## 7) Practical tiered recommendation (what to trust most)

### Highest trust for scoring backbone
- **ACLED + UCDP + UNHCR + World Bank/IMF + FAO**

### High-value but needs guardrails
- **GDELT (events + GKG), GTD, OCHA/HDX**

### Contextual only (do not dominate final score)
- **Google Trends, pageviews, ad-hoc RSS sentiment, broad global risk indices alone**

---

## 8) Minimum viable source policy for GeoWar Pulse

1. No country score change >X points unless at least one Tier A/B source confirms movement.
2. If only Tier C/D signals move, adjust **momentum/confidence**, not headline risk band.
3. Recompute past 30 days when major backfills arrive (ACLED/UCDP revisions).
4. Expose “why score moved” with source attribution and timestamp.
5. Track per-country data coverage to avoid false precision.

---

## 9) Quick implementation priority list

**Week 1–2:** ACLED + GDELT + country feature schema + daily scorer.  
**Week 3:** UCDP and UNHCR integration + confidence model.  
**Week 4:** Food/energy/FX stress multipliers + explanation layer.  
**Then:** GTD, OCHA layers, narrative enrichments, model calibration audits.

---

## 10) Reference links (entry points)

- ACLED methodology/codebook and API/export portal
- UCDP download center + API
- GDELT project docs/data endpoints
- START GTD portal
- UNHCR Refugee Data API portal
- World Bank Data API
- IMF data portal (WEO/IFS and related)
- FAO/FAOSTAT and Food Price Index
- OCHA HDX platform

(Use official API/docs URLs during implementation and pin exact dataset versions in the ingestion metadata.)
