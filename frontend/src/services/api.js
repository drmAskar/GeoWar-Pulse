// API client for GeoWar Pulse backend
// Transforms API responses to frontend format

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

// Transform API CountryScore to frontend hotspot format
function transformHotspot(apiCountry) {
  return {
    code: apiCountry.country_code,
    country: apiCountry.country_name || apiCountry.country_code,
    riskScore: Math.round(apiCountry.risk_score),
    riskBand: apiCountry.risk_band,
    momentum: apiCountry.momentum, // 'escalating', 'stable', 'de-escalating'
    confidence: Math.round(apiCountry.confidence),
    delta: apiCountry.delta,
    drivers: apiCountry.top_drivers || [],
  };
}

// Transform API CountryDetail to frontend format
function transformCountryDetail(apiDetail) {
  return {
    code: apiDetail.country.country_code,
    country: apiDetail.country.country_name,
    riskScore: Math.round(apiDetail.country.risk_score),
    riskBand: apiDetail.country.risk_band,
    momentum: apiDetail.country.momentum,
    confidence: Math.round(apiDetail.country.confidence),
    delta24h: apiDetail.country.delta_24h,
    delta7d: apiDetail.country.delta_7d,
    drivers: apiDetail.drivers.map(d => ({
      key: d.key,
      label: d.label,
      impact: d.impact,
      direction: d.direction,
    })),
    confidenceBreakdown: apiDetail.confidence_breakdown,
    latestEvidence: apiDetail.latest_evidence.map(e => ({
      eventId: e.event_id,
      timestamp: e.timestamp,
      signal: e.signal,
      summary: e.summary,
      source: e.source.source_name,
      sourceType: e.source.source_type,
      verified: e.verified,
    })),
  };
}

// Transform timeline API response
function transformTimeline(apiTimeline) {
  return apiTimeline.points.map(p => ({
    ts: p.ts,
    riskScore: Math.round(p.risk_score),
    confidence: Math.round(p.confidence),
  }));
}

// API methods
export const api = {
  // Health check
  async health() {
    return fetchJson(`${API_BASE}/health`);
  },

  // Get map snapshot - all countries for map
  async getMapSnapshot(window = '24h', minConfidence = 0) {
    const url = `${API_BASE}/map/snapshot?window=${window}&min_confidence=${minConfidence}`;
    const data = await fetchJson(url);
    return {
      asOf: data.as_of,
      window: data.window,
      hotspots: data.countries.map(transformHotspot),
      meta: data.meta,
    };
  },

  // Get country detail
  async getCountry(countryCode, window = '24h') {
    const url = `${API_BASE}/countries/${countryCode}?window=${window}`;
    const data = await fetchJson(url);
    return transformCountryDetail(data);
  },

  // Get country timeline
  async getTimeline(countryCode, window = '30d', bucket = 'day') {
    const url = `${API_BASE}/countries/${countryCode}/timeline?window=${window}&bucket=${bucket}`;
    const data = await fetchJson(url);
    return transformTimeline(data);
  },

  // Legacy endpoints (for backward compatibility)
  async getScores(window = '24h') {
    const url = `${API_BASE}/scores?window=${window}`;
    const data = await fetchJson(url);
    return {
      window: data.window,
      count: data.count,
      items: data.items.map(transformHotspot),
    };
  },

  async getScore(countryCode, window = '24h') {
    const url = `${API_BASE}/scores/${countryCode}?window=${window}`;
    const data = await fetchJson(url);
    return transformHotspot(data);
  },
};

export default api;