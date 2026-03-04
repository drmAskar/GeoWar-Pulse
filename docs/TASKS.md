# GeoWar Pulse - Actionable Tasks

## Sprint 1: Backend Core

### Task 1.1: Database Setup
- [ ] Create PostgreSQL schema with countries, events, scores tables
- [ ] Add indexes for frequently queried columns
- [ ] Set up connection pooling
- [ ] Create seed data script

### Task 1.2: Event Model Implementation
- [ ] Implement Event schema (category, signal_code, direction, severity)
- [ ] Add source reliability tracking
- [ ] Implement evidence quality scoring
- [ ] Create event validation rules

### Task 1.3: Signal Processing
- [ ] Build event classifier for M/P/E/I/H/B categories
- [ ] Implement severity scoring (0-1 scale)
- [ ] Add direction detection (escalatory/de-escalatory)
- [ ] Create confidence calculation function

### Task 1.4: Risk Calculation Engine
- [ ] Implement recency decay function
- [ ] Build category aggregation logic
- [ ] Create momentum calculations
- [ ] Implement normalization (robust z-score)
- [ ] Add rumor penalty system
- [ ] Finalize risk score formula

### Task 1.5: API Development
- [ ] Create GET /scores endpoint
- [ ] Create GET /scores/{country_code} endpoint
- [ ] Create GET /trends endpoint
- [ ] Add request validation
- [ ] Implement error handling

## Sprint 2: Frontend

### Task 2.1: Map Integration
- [ ] Install Leaflet/Mapbox dependencies
- [ ] Load world GeoJSON data
- [ ] Implement country color-coding by risk
- [ ] Add click handlers
- [ ] Optimize rendering performance

### Task 2.2: Dashboard Components
- [ ] Create RiskScore component (0-100 display)
- [ ] Build MomentumIndicator (↑↓→)
- [ ] Implement ConfidenceMeter
- [ ] Create TopDriversList component
- [ ] Add TrendChart component

### Task 2.3: UI/UX Implementation
- [ ] Set up dark theme
- [ ] Implement responsive layout
- [ ] Add loading skeletons
- [ ] Create error boundaries
- [ ] Add animations

### Task 2.4: API Integration
- [ ] Create API client service
- [ ] Implement data fetching hooks
- [ ] Add polling for updates
- [ ] Handle offline states

## Sprint 3: Integration & Testing

### Task 3.1: End-to-End Testing
- [ ] Test full data flow (API → Frontend)
- [ ] Verify map displays correctly
- [ ] Test country selection
- [ ] Verify score calculations

### Task 3.2: Demo Data
- [ ] Create realistic sample events
- [ ] Populate seed data for testing
- [ ] Verify all risk levels display

### Task 3.3: Documentation
- [ ] Document API endpoints
- [ ] Create user guide
- [ ] Document scoring methodology

---

## Quick Start Commands

```bash
# Backend
cd app
uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

## Dependencies to Install

### Backend
```bash
pip install fastapi uvicorn pydantic psycopg2-binary
```

### Frontend
```bash
cd frontend
npm install leaflet react-leaflet axios
```

---

*Framework: Spec-Kit (Spec-Driven Development)*
*Based on: PLAN.md, SPEC.md, CONSTITUTION.md*