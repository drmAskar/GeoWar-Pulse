# GeoWar Pulse - Specification

## Project Overview
GeoWar Pulse is a **real-time geopolitical conflict risk intelligence platform** that displays risk scores on an interactive map. The platform provides:
- **War Risk Score (0-100)** for each country/region
- **Risk momentum** (escalating, stable, de-escalating)
- **Confidence level** based on source quality and verification
- **Multi-factor analysis** based on military, political, economic, information, and humanitarian signals

## Core Features

### 1. Interactive Risk Map
- Color-coded world map showing risk levels (green→yellow→orange→red)
- Click on countries to view detailed risk information
- Real-time updates with color transitions

### 2. Multi-Factor Risk Scoring
Based on RESEARCH_SIGNALS.md, the system analyzes:
- **Military (M)**: Troop movements, equipment, air/naval activity, combat readiness, kinetic incidents
- **Political (P)**: Diplomatic rupture, escalatory rhetoric, peace signaling, leadership instability
- **Economic (E)**: Sanctions, energy coercion, trade disruption, defense-industrial surge
- **Information (I)**: Cyber operations, information warfare, gray-zone acts, rumors
- **Humanitarian (H)**: Displacement, civilian harm, civil unrest, emergency strain
- **Baseline (B)**: Historical conflict propensity, border disputes, state fragility

### 3. Confidence Scoring
- Source reliability (0-1)
- Evidence quality (0-1)
- Independent source count
- Data freshness and coverage
- Rumor detection and penalty

### 4. Real-time Dashboard
- Top hotspots by risk score
- Risk trend indicators (24h, 7d, 30d)
- Top contributing factors for each region
- Source transparency (show what's driving the score)

## UI/UX Requirements

### Modern Design
- Dark theme with high contrast
- Smooth color transitions for risk levels
- Responsive layout (desktop + mobile)
- Professional cartographic map (Leaflet/Mapbox)

### Information Display
- Clear risk score (large, prominent)
- Momentum indicator with arrow (↑↓→)
- Confidence percentage with visual meter
- Top 3-5 risk drivers listed
- Source attribution

## Technical Stack (Existing)
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **Database**: PostgreSQL
- **Map**: Leaflet/Mapbox

## Acceptance Criteria
1. Map displays all countries with color-coded risk levels
2. Clicking a country shows detailed risk information
3. Risk scores update based on multi-factor analysis
4. Confidence level reflects data quality
5. Top risk drivers are displayed for transparency
6. Modern, responsive UI
7. API endpoints for scores, details, and trends

---

*Framework: Spec-Kit (Spec-Driven Development)*
*Based on: RESEARCH_SIGNALS.md, RESEARCH_UI.md, DATA_MODEL.md*