# GeoWar Pulse - Implementation Plan

## Phase 1: Backend Core (Week 1-2)

### 1.1 Data Models & Schema
- [ ] Implement Event schema (from RESEARCH_SIGNALS.md)
- [ ] Create Region/Country model
- [ ] Set up PostgreSQL database with proper indexes
- [ ] Implement source reliability tracking

### 1.2 Signal Processing Pipeline
- [ ] Build event classifier (taxonomy M/P/E/I/H/B)
- [ ] Implement severity scoring algorithm
- [ ] Add direction detection (escalatory/de-escalatory)
- [ ] Create confidence calculation (C_e formula)
- [ ] Implement recency decay function

### 1.3 Risk Calculation Engine
- [ ] Implement category aggregation
- [ ] Build momentum calculations (24h vs 7d vs 30d)
- [ ] Create normalization (robust z-score)
- [ ] Implement rumor penalty system
- [ ] Final risk score formula (0-100)

### 1.4 API Endpoints
- [ ] GET /scores - List all country scores
- [ ] GET /scores/{country_code} - Detailed country score
- [ ] GET /trends - Historical trends
- [ ] GET /sources - Data source information
- [ ] POST /events - Submit new events (for testing)

## Phase 2: Frontend Development (Week 2-3)

### 2.1 Map Integration
- [ ] Integrate Leaflet/Mapbox
- [ ] Load world GeoJSON
- [ ] Color-code countries by risk score
- [ ] Add click handlers for country selection

### 2.2 Dashboard Components
- [ ] Risk score display component
- [ ] Momentum indicator (↑↓→)
- [ ] Confidence meter
- [ ] Top risk drivers list
- [ ] Trend charts (24h, 7d, 30d)

### 2.3 UI/UX
- [ ] Dark theme implementation
- [ ] Responsive design
- [ ] Loading states
- [ ] Error handling
- [ ] Animations/transitions

### 2.4 API Integration
- [ ] Connect frontend to backend API
- [ ] Implement polling for real-time updates
- [ ] Add caching layer
- [ ] Handle offline states

## Phase 3: Data & Testing (Week 3-4)

### 3.1 Data Ingestion
- [ ] Set up sample data generator
- [ ] Create mock events for testing
- [ ] Implement data validation
- [ ] Add seed data for demo

### 3.2 Quality Assurance
- [ ] Unit tests for scoring logic
- [ ] Integration tests for API
- [ ] E2E tests for user flows
- [ ] Performance testing

### 3.3 Documentation
- [ ] API documentation
- [ ] Scoring methodology docs
- [ ] User guide

## Technical Dependencies

### Backend
- Python 3.11+
- FastAPI
- PostgreSQL
- Pydantic
- SQLAlchemy (optional)

### Frontend
- React 18+
- Vite
- Leaflet or Mapbox GL
- Axios or Fetch
- CSS Modules or Tailwind

### Infrastructure
- Docker (optional)
- PostgreSQL database
- API server (uvicorn)

## Priority Order

1. **Backend scoring engine** - Core logic is most important
2. **Basic API** - Frontend needs data
3. **Simple map** - Visual representation
4. **Country detail panel** - Show detailed info
5. **Confidence display** - Transparency
6. **Trend charts** - Historical context
7. **Real-time updates** - Live data

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Complex scoring logic | Start with simplified MVP scoring |
| Data quality | Implement confidence scoring to filter noise |
| Map performance | Use vector tiles for large-scale rendering |
| Real-time updates | Use polling with caching, later WebSocket |

---

*Framework: Spec-Kit (Spec-Driven Development)*
*Based on: SPEC.md, CONSTITUTION.md*