import { useState, useEffect } from 'react'
import api from '../services/api'
import { bandForScore } from '../utils'

export function CountryDetailPanel({ country, onClose }) {
  const [detail, setDetail] = useState(null)
  const [timeline, setTimeline] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!country?.code) return

    const fetchDetail = async () => {
      setLoading(true)
      setError(null)
      try {
        const [detailData, timelineData] = await Promise.all([
          api.getCountry(country.code),
          api.getTimeline(country.code, '30d'),
        ])
        setDetail(detailData)
        setTimeline(timelineData)
      } catch (err) {
        console.error('Failed to fetch country detail:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchDetail()
  }, [country?.code])

  if (!country) return null

  const band = bandForScore(country.riskScore)

  const getMomentumIcon = (momentum) => {
    if (momentum === 'escalating') return '↗️'
    if (momentum === 'de-escalating') return '↘️'
    return '→'
  }

  return (
    <div className="country-detail-overlay" onClick={onClose}>
      <div className="country-detail-panel" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>×</button>
        
        <div className="detail-header" style={{ borderLeftColor: band.color }}>
          <h2>{country.country || country.code}</h2>
          <span className="risk-band" style={{ backgroundColor: band.color }}>
            {band.label}
          </span>
        </div>

        {loading ? (
          <div className="detail-loading">
            <div className="spinner"></div>
            <p>Loading country data...</p>
          </div>
        ) : error ? (
          <div className="detail-error">
            <p>Error: {error}</p>
            <p>Showing basic info only</p>
          </div>
        ) : (
          <>
            <div className="score-section">
              <div className="main-score">
                <span className="score-value" style={{ color: band.color }}>
                  {country.riskScore}
                </span>
                <span className="score-max">/100</span>
              </div>
              <div className="score-meta">
                <div className="meta-item">
                  <span className="meta-label">Confidence</span>
                  <span className="meta-value">{country.confidence}%</span>
                </div>
                <div className="meta-item">
                  <span className="meta-label">Momentum</span>
                  <span className={`meta-value momentum-${country.momentum}`}>
                    {getMomentumIcon(country.momentum)} {country.momentum}
                  </span>
                </div>
                {country.delta24h !== undefined && (
                  <div className="meta-item">
                    <span className="meta-label">24h Change</span>
                    <span className={`meta-value ${country.delta24h > 0 ? 'positive' : country.delta24h < 0 ? 'negative' : ''}`}>
                      {country.delta24h > 0 ? '+' : ''}{country.delta24h}
                    </span>
                  </div>
                )}
              </div>
            </div>

            {detail?.drivers && detail.drivers.length > 0 && (
              <div className="drivers-section">
                <h3>Top Drivers</h3>
                <div className="drivers-list">
                  {detail.drivers.map((driver, i) => (
                    <div key={i} className={`driver-item ${driver.direction}`}>
                      <span className="driver-direction">
                        {driver.direction === 'up' ? '↑' : '↓'}
                      </span>
                      <span className="driver-label">{driver.label}</span>
                      <span className="driver-impact">+{driver.impact}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {detail?.confidenceBreakdown && (
              <div className="confidence-section">
                <h3>Confidence Breakdown</h3>
                <div className="confidence-bars">
                  <div className="conf-bar">
                    <span>Source Reliability</span>
                    <div className="bar-track">
                      <div 
                        className="bar-fill" 
                        style={{ width: `${detail.confidenceBreakdown.source_reliability * 100}%` }}
                      />
                    </div>
                    <span>{Math.round(detail.confidenceBreakdown.source_reliability * 100)}%</span>
                  </div>
                  <div className="conf-bar">
                    <span>Corroboration</span>
                    <div className="bar-track">
                      <div 
                        className="bar-fill" 
                        style={{ width: `${detail.confidenceBreakdown.corroboration * 100}%` }}
                      />
                    </div>
                    <span>{Math.round(detail.confidenceBreakdown.corroboration * 100)}%</span>
                  </div>
                  <div className="conf-bar">
                    <span>Coverage</span>
                    <div className="bar-track">
                      <div 
                        className="bar-fill" 
                        style={{ width: `${detail.confidenceBreakdown.coverage * 100}%` }}
                      />
                    </div>
                    <span>{Math.round(detail.confidenceBreakdown.coverage * 100)}%</span>
                  </div>
                  {detail.confidenceBreakdown.rumor_penalty > 0 && (
                    <div className="conf-bar penalty">
                      <span>Rumor Penalty</span>
                      <div className="bar-track">
                        <div 
                          className="bar-fill" 
                          style={{ width: `${detail.confidenceBreakdown.rumor_penalty * 100}%` }}
                        />
                      </div>
                      <span>-{Math.round(detail.confidenceBreakdown.rumor_penalty * 100)}%</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {detail?.latestEvidence && detail.latestEvidence.length > 0 && (
              <div className="evidence-section">
                <h3>Latest Evidence</h3>
                <div className="evidence-list">
                  {detail.latestEvidence.map((ev, i) => (
                    <div key={i} className="evidence-item">
                      <div className="evidence-header">
                        <span className="evidence-signal">{ev.signal}</span>
                        {ev.verified && <span className="verified-badge">✓ Verified</span>}
                      </div>
                      <p className="evidence-summary">{ev.summary}</p>
                      <div className="evidence-meta">
                        <span>{ev.source}</span>
                        <span className="source-type">{ev.sourceType}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {timeline.length > 0 && (
              <div className="timeline-section">
                <h3>30-Day Trend</h3>
                <div className="timeline-chart">
                  {timeline.map((point, i) => (
                    <div 
                      key={i} 
                      className="timeline-point"
                      style={{ 
                        height: `${point.riskScore}%`,
                        backgroundColor: bandForScore(point.riskScore).color
                      }}
                      title={`${new Date(point.ts).toLocaleDateString()}: ${point.riskScore}`}
                    />
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}