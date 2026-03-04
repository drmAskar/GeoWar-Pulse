# GeoWar Pulse — ROADMAP V2 (Prioritized Execution)

**Objective:** move from MVP prototype to explainable, production-grade global geopolitical risk platform.

## Delivery principles
- Build **data reliability first**, then model complexity.
- Keep scoring **explainable by default**.
- Every risk movement must be traceable to evidence.
- Prefer robust batch cadence before real-time streaming complexity.

---

## Milestone M0 (Week 0–1) — Foundation Lock

## Outcomes
- Single canonical architecture and contracts frozen for implementation.

## Work
1. Freeze canonical schemas: `raw_events`, `normalized_events`, `country_features_daily`, `country_scores`, `score_drivers`, `ingestion_runs`.
2. Align API contract to `/api/v1` endpoints and response envelope.
3. Add migration framework (Alembic), environment config, and seed pipeline.
4. Add CI baseline (lint + unit tests + schema migration check).

## Exit criteria
- Fresh environment can run migrations + start backend + run frontend.
- API schema and DB schema versioned and tagged.

---

## Milestone M1 (Week 1–3) — Data Ingestion Backbone (Top Priority)

## Outcomes
- Real source ingestion + normalization + persistence working on schedule.

## Work
1. Build source adapters (MVP set):
   - ACLED
   - GDELT Events/GKG
   - UNHCR
   - World Bank + FAO
2. Implement canonical normalization mapping:
   - category (M/P/E/I/H/B)
   - signal_code (M1..B4 where possible)
   - severity, direction, event confidence fields
3. Implement dedupe/reconciliation:
   - provider key + time/geo/entity similarity
   - merge linked duplicates into single canonical event
4. Add ingestion run tracking + freshness SLA + failure metadata.
5. Schedule jobs:
   - GDELT every 15–30 min
   - ACLED daily/weekly refresh
   - UNHCR/FAO/WB daily or per source cadence

## Exit criteria
- Ingestion jobs populate DB with stable canonical events.
- Freshness dashboard available (at least API metadata).

---

## Milestone M2 (Week 3–5) — Multi-Factor Scoring v0.2

## Outcomes
- Scoring based on real data and category-level explainability.

## Work
1. Implement feature builder for 24h/7d/30d windows:
   - category aggregates
   - momentum (`24h vs 7d`, `7d vs 30d`)
   - burst, volatility, persistence
2. Implement robust normalization:
   - winsorization p1/p99
   - robust z-score (MAD)
   - bounded transform (sigmoid/tanh)
3. Score computation:
   - weighted interpretable core -> 0–100
   - confidence-adjusted shrinkage when low certainty
4. Store top positive/negative drivers per score snapshot.

## Exit criteria
- Scores generated for all active countries with reproducible outputs.
- Driver attribution available and queryable.

---

## Milestone M3 (Week 5–6) — Confidence Model + Anti-Rumor Layer

## Outcomes
- Reduced false alarms and explicit uncertainty handling.

## Work
1. Confidence decomposition model:
   - source reliability
   - independent corroboration
   - coverage/freshness
   - disagreement penalty
2. Anti-rumor pipeline:
   - rumor likelihood (`U_e`) from low diversity, high reposting, delayed corroboration
   - rumor penalty multiplier + low-confidence gate
   - duplicate/viral propagation dampening
3. Source reliability feedback loop:
   - update trust priors from retractions/verified confirmations.

## Exit criteria
- Country output includes confidence breakdown and rumor impact note.
- No major score jumps from low-confidence rumor bursts.

---

## Milestone M4 (Week 6–7) — API Contract Completion

## Outcomes
- Contract-compliant API for frontend and third-party consumption.

## Work
Implement and harden:
1. `GET /api/v1/health`
2. `GET /api/v1/map/snapshot?window=24h|7d|30d`
3. `GET /api/v1/countries/{countryCode}`
4. `GET /api/v1/countries/{countryCode}/timeline`
5. Alerts:
   - `GET /api/v1/alerts`
   - `POST /api/v1/alerts/subscribe`
6. Standardized non-2xx error envelope.
7. Pagination/filters + min confidence filters.

## Exit criteria
- OpenAPI matches docs/API_CONTRACT.md.
- Integration tests pass for all primary endpoints.

---

## Milestone M5 (Week 7–9) — Modern World-Map Frontend

## Outcomes
- Production-grade, explainable map UX connected to real backend.

## Work
1. Replace marker-only view with **country polygon choropleth** (GeoJSON).
2. Add window toggle (24h/7d/30d) + min-confidence filter.
3. Country detail panel with:
   - risk score, momentum, confidence
   - top drivers (up/down)
   - latest verified evidence
4. Timeline chart integration.
5. Alerts UX (subscribe/list).
6. Strong loading/error/stale states.

## Exit criteria
- Full user flow works from real API without sample fallback.
- Map + panel + timeline performance acceptable on desktop/mobile.

---

## Milestone M6 (Week 9–10) — Scheduler, Ops, and Production Hardening

## Outcomes
- Reliable periodic updates and operational safety.

## Work
1. Orchestration:
   - scheduled ingestion + scoring runs
   - idempotent jobs and retry policy
2. Observability:
   - structured logs with run/request IDs
   - freshness and API latency metrics
   - alerting on stale/failed pipelines
3. Quality gates:
   - unit tests (scoring/confidence)
   - integration tests (API + DB)
   - E2E smoke (ingest -> score -> map)
4. Security and robustness:
   - rate limiting
   - input validation hardening
   - secrets/config separation by environment

## Exit criteria
- Automated daily operations with SLA monitoring.
- Release candidate passes smoke and regression tests.

---

## Cross-cutting technical decisions (recommended now)

1. **Scoring cadence:** hourly incremental + nightly full recompute.  
2. **Confidence gate for UI:** show low-confidence badge and reduce headline band sensitivity.  
3. **Source tiering:** Tier A/B can move headline score; Tier C mostly affects momentum/confidence.  
4. **Reproducibility:** every score stores `model_version`, `source_versions`, `as_of`.

---

## Risk Register and Mitigations

1. **Noise from high-frequency machine sources** → strict dedupe + corroboration threshold + rumor penalty.  
2. **Coverage gaps in low-information regions** → coverage-aware confidence + uncertainty messaging.  
3. **Schema drift from new providers** → canonical adapter contracts + validation tests.  
4. **Frontend latency at global scale** → precomputed snapshots + map simplification + caching.

---

## Arabic Executive Summary (ملخص تنفيذي)

GeoWar Pulse حالياً في مرحلة **MVP أولية**: الواجهة جيدة كبداية والوثائق قوية، لكن المنصة ليست جاهزة للإنتاج بعد.  
الأولوية القصوى الآن هي بناء خط بيانات حقيقي (ingestion + normalization + storage) ثم ربطه بمحرك تقييم مخاطر متعدد العوامل مع **نموذج ثقة واضح** وطبقة **مكافحة الشائعات**.  
بعدها يتم تثبيت واجهات API حسب العقد، ثم تطوير خريطة عالمية حديثة (choropleth) مع تتبع زمني وتفسيرات "لماذا تغيّر المؤشر".  
النجاح يعتمد على: جودة المصادر، الحوكمة على الثقة، والجدولة الدورية الموثوقة مع مراقبة تشغيلية.

## Arabic Technical Task List (قائمة مهام تقنية مختصرة)

1. توحيد مخطط قاعدة البيانات وعقود API وإضافة Alembic + CI.
2. تنفيذ موصلات المصادر المفتوحة الأساسية: ACLED + GDELT + UNHCR + WorldBank/FAO.
3. بناء طبقة normalization موحدة مع إزالة التكرار وتتبع lineage.
4. تشغيل جدولة دورية للإدخال والحساب (15–30 دقيقة للمصادر السريعة + إعادة حساب ليلي).
5. تنفيذ محرك تقييم v0.2 (فئات M/P/E/I/H/B + ميزات الزخم/التقلب + التطبيع robust).
6. تنفيذ نموذج الثقة المفصل (Reliability/Corroboration/Coverage/Disagreement).
7. إضافة طبقة anti-rumor (gating + penalty + dampening).
8. إكمال نقاط API التعاقدية (`/map/snapshot`, `/countries/{code}`, `/timeline`, alerts).
9. ترقية الواجهة إلى choropleth عالمي + timeline + مرشحات (window/confidence).
10. إضافة observability واختبارات وحدة/تكامل/E2E قبل الإطلاق.
