# GeoWar Pulse — UI/UX Concept Research

## 1) Product UX Goal
Design a **trustworthy, fast-scannable, map-first intelligence dashboard** that helps users answer three questions in under 10 seconds:
1. **Where is risk highest right now?**
2. **What changed, and how much?**
3. **Why did it change (and how reliable is that)?**

Primary users (likely): analysts, journalists, policy teams, risk/compliance teams.

---

## 2) Design Principles

1. **Signal first, detail on demand**
   - Global overview at a glance, deep evidence only when requested.
2. **Explainability by default**
   - Every score is paired with confidence + top drivers + source trail.
3. **Don’t imply certainty**
   - Use language like “probability”, “momentum”, “confidence”, not deterministic labels.
4. **Progressive disclosure**
   - Start simple (map + top hotspots), then layer trends, events, and model details.
5. **Mobile-first intelligence**
   - Designed for monitoring on mobile, deep analysis on desktop.
6. **Accessible under stress**
   - High contrast, shape + text cues (not color-only), keyboard/touch parity.

---

## 3) Information Architecture (MVP)

## Global Navigation
- **Map** (default)
- **Watchlist**
- **Alerts**
- **Sources / Methodology**
- **Settings**

## Map Page (Core)
1. **Top bar**: global filters + search + timestamp + alert state
2. **World map canvas**: choropleth or filled-country style
3. **Hotspot strip/cards**: top N highest-risk movers
4. **Country detail panel** (drawer/sheet): score, trend, confidence, drivers, timeline

---

## 4) Visual System — Color + Semantics

## Base Palette (Dark-first recommended)
Dark UI is generally better for map-heavy intelligence tools and prolonged monitoring.

- **Background-900**: `#0B1020`
- **Surface-800**: `#121A2B`
- **Surface-700**: `#1A2438`
- **Border**: `#2B3956`
- **Text-primary**: `#E6ECFF`
- **Text-secondary**: `#9FB0D6`

## Risk Palette (aligned with README bands)
Use **both color + label + icon/shape** for accessibility.

- **Low (0–24)**: Green `#2FBF71`
- **Elevated (25–49)**: Amber `#F2C14E`
- **High (50–74)**: Orange `#F28C38`
- **Critical (75–100)**: Red `#E6534B`

Optional neutral/no-data:
- **No data / insufficient evidence**: Slate `#5E6C8A` (hatched pattern on map)

## Confidence Palette (independent channel)
Confidence should not be conflated with risk.

- **High confidence**: Cyan `#34B6FF`
- **Medium confidence**: Blue-gray `#6FA5C9`
- **Low confidence**: Violet-gray `#8A87B8`

## Accessibility Rules
- Minimum contrast: WCAG AA for text and data labels.
- Never rely on red/green alone.
- Add secondary encoding for risk level:
  - shape marker in cards (● ▲ ■ ◆)
  - border styles or icon badges
  - textual label always visible

---

## 5) Map Interaction Model

## Core Map Behaviors
- **Hover (desktop) / tap (mobile)**: quick country tooltip
  - country name
  - risk score
  - momentum arrow (↑ ↓ →)
  - confidence badge
- **Click/tap country**: open detail panel (right drawer desktop, bottom sheet mobile)
- **Zoom**: mouse wheel/pinch with bounded zoom levels
- **Pan**: drag with inertial movement

## Filters (top bar)
- Time window: `24h | 7d | 30d`
- Region filter: continent/geo-political group
- Momentum filter: escalating/stable/de-escalating
- Confidence threshold: hide low-confidence estimates
- Event type tags: military, sanctions, rhetoric, cyber, protests

## Map Layers (toggle)
- Risk score (default)
- Momentum heat overlay
- Event density dots
- Confidence opacity mode (lower confidence = lower fill opacity)

## Interaction Safeguards
- No sudden auto-pan when data refreshes.
- Preserve user zoom/position after updates.
- Animate score changes subtly (200–400ms) to avoid visual noise.

---

## 6) Card System (Dashboard + Details)

## A) Hotspot Card (compact)
Purpose: rapid scan of top movers/high-risk countries.

Fields:
- Country + flag
- Risk score (0–100)
- Band pill (Low/Elevated/High/Critical)
- Momentum delta (e.g., `+8 in 24h`)
- Confidence chip (e.g., `Conf: 72%`)
- Top 1–2 driver tags (e.g., “Border clash”, “Sanctions”) 

States:
- Positive/negative momentum arrows
- New alert badge
- Low-confidence warning icon

## B) Country Detail Card (expanded in panel)
Sections:
1. **Headline**: current score, band, momentum, confidence
2. **Trend chart**: 24h/7d/30d sparkline + notable jumps
3. **Top drivers**: ranked contributions with +/- impact bars
4. **Evidence feed**: source snippets with timestamps
5. **Scenario note**: “What this likely means” (short model narrative)

## C) Alert Card
- Trigger condition (e.g., score crossed 75)
- Time of trigger
- Change summary
- CTA: “Open country details”, “Add to watchlist”, “Mute similar alerts”

---

## 7) Explainability UX (Critical Differentiator)

Explainability should be visible at all levels, not hidden in settings.

## Explainability Modules
1. **Why this score?**
   - Top contributing factors with weighted percentages
   - Example: “Military mobilization (+12), hostile rhetoric (+7), ceasefire talks (-4)”
2. **What changed since last period?**
   - Delta decomposition chart (waterfall style)
3. **How reliable is this?**
   - Confidence score + source diversity + recency indicator
4. **Which sources were used?**
   - Source list with credibility tier and timestamp
5. **Model limitations**
   - Inline disclaimer: “Risk indicates probability, not certainty.”

## Explainability UI Patterns
- Use **accordion blocks** in detail panel for readability on mobile.
- Use **tooltips for terminology**: momentum, confidence, driver weight.
- Add **“Methodology” deep link** from every detail view.

---

## 8) Mobile-First Layout Concept

## Small screens (360–480px)
- Sticky top bar: search + filter icon + alert bell
- Map takes top ~55–60% of viewport
- Horizontal hotspot cards below map
- Country details open as draggable bottom sheet (snap points: 35% / 70% / full)

## Tablet (768px+)
- Map left (60%), insights panel right (40%)
- Persistent hotspot rail

## Desktop (1024px+)
- 12-column layout:
  - map: 8 columns
  - insight panel: 4 columns
- Optional left side mini-nav for modules

## Mobile UX Rules
- Minimum tap target: 44x44px
- Avoid dense legends: collapsible legend with quick presets
- One-thumb actions prioritized at bottom region
- Keep key metrics visible while scrolling details

---

## 9) Motion + Feedback

- **Micro-animations**: score transitions, card hover, filter chip activation
- **Live update pulse**: subtle “updated X min ago” indicator
- **Skeleton loading** for map tiles/cards
- **Optimistic interactions** for watchlist toggles
- **Haptic-friendly cues** on mobile for critical alert actions

Avoid excessive animation during crisis scenarios; clarity > flair.

---

## 10) Empty/Error/Edge States

- **No data country**: neutral color + “Insufficient signal” label
- **Low confidence**: striped overlay + warning icon in tooltip
- **Data delay**: banner “Feed delayed by 18 min”
- **API error**: preserve last known map, show stale badge
- **Conflicting signals**: show “high variance” badge and explain impact on confidence

---

## 11) Content Style (Microcopy)

Preferred voice:
- concise, neutral, evidence-oriented
- avoid sensational language

Examples:
- Good: “Escalation probability increased due to cross-border shelling reports.”
- Avoid: “War is imminent.”

Key labels:
- “Risk Score”
- “Momentum”
- “Confidence”
- “Top Drivers”
- “Evidence”
- “Methodology”

---

## 12) Suggested MVP Component List (Frontend)

- `RiskMapCanvas`
- `RiskLegend`
- `GlobalFilterBar`
- `CountryTooltip`
- `CountryDetailDrawer` / `CountryDetailSheet`
- `HotspotCard`
- `AlertCard`
- `ConfidenceBadge`
- `DriverImpactList`
- `TrendSparkline`
- `EvidenceTimeline`
- `MethodologyLinkBlock`

---

## 13) Practical Implementation Notes

- Use vector map rendering where possible for clean zoom (MapLibre/Deck.gl/SVG layer strategy).
- Keep map color interpolation discrete by risk band for trust/interpretability.
- Cache last successful payload to support degraded mode.
- Prefer server-provided precomputed deltas for card speed.
- Build design tokens early (`color.risk.critical`, `space.4`, `radius.md`, etc.) for consistency.

---

## 14) UI Success Metrics

1. Time-to-insight: user can identify top 3 hotspots in <10s.
2. Explainability engagement: % of users opening “Why this score?”.
3. Alert action rate: watchlist/additional drill-down clicks.
4. Mobile usability: completion rate for “find country + view drivers”.
5. Trust proxy: reduced “unclear score” feedback.

---

## 15) Recommended Next Design Deliverables

1. **Low-fi wireframes** (mobile + desktop map page)
2. **Design token file** (risk, confidence, semantic colors)
3. **Interactive prototype** (country tap → detail panel flow)
4. **Explainability module mock** (driver decomposition + source trace)
5. **Usability test script** for analysts (5-task benchmark)

---

## Final Recommendation
For GeoWar Pulse MVP, prioritize:
1. **Map clarity + stable interactions**
2. **Explainability panel quality**
3. **Mobile bottom-sheet experience**

This trio gives the strongest trust + usability foundation before adding advanced analytics layers.
