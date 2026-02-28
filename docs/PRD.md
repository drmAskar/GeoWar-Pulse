# PRD — GeoWar Pulse (MVP)

## Problem
Decision-makers and the public struggle to rapidly understand where conflict risk is rising and why.

## Goal
Provide near-real-time, explainable conflict-risk scoring at country/region level.

## Non-Goals
- Predict exact start/end dates of wars.
- Provide tactical military advice.

## Users
- Analysts, journalists, researchers
- Businesses with regional exposure
- General public

## Functional Requirements
1. Global map with country-level risk colors.
2. Country panel: score, momentum, confidence, key drivers.
3. Timeline toggles: 24h / 7d / 30d.
4. Alerts when score crosses thresholds.
5. Source traceability for each score movement.

## Quality Requirements
- Explainability first
- Confidence tagging
- Graceful degradation on sparse data

## Success Metrics
- Latency from event ingestion to score update
- Coverage of priority countries
- User trust (low false-alarm rate, clear rationale)
