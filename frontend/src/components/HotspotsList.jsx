import { bandForScore } from '../utils'

export function HotspotsList({ hotspots, selected, onSelect }) {
  if (!hotspots || hotspots.length === 0) {
    return (
      <div className="panel hotspots-panel">
        <h3>Risk Hotspots</h3>
        <p className="empty-state">No hotspots to display</p>
      </div>
    )
  }

  const sorted = [...hotspots].sort((a, b) => b.riskScore - a.riskScore)

  const getMomentumIcon = (momentum) => {
    if (momentum === 'escalating') return '↗'
    if (momentum === 'de-escalating') return '↘'
    return '→'
  }

  return (
    <div className="panel hotspots-panel">
      <h3>Risk Hotspots ({hotspots.length})</h3>
      <div className="hotspots-list">
        {sorted.map((spot) => {
          const band = bandForScore(spot.riskScore)
          const isSelected = selected?.code === spot.code

          return (
            <div
              key={spot.code}
              className={`hotspot-item ${isSelected ? 'selected' : ''}`}
              onClick={() => onSelect(spot)}
              style={{ borderLeftColor: band.color }}
            >
              <div className="hotspot-main">
                <span className="hotspot-country">{spot.country}</span>
                <span className="hotspot-code">{spot.code}</span>
              </div>
              <div className="hotspot-score">
                <span className="score" style={{ color: band.color }}>
                  {spot.riskScore}
                </span>
                <span className="band">{band.label}</span>
              </div>
              <div className="hotspot-meta">
                <span className="confidence">{spot.confidence}% conf</span>
                <span className={`momentum momentum-${spot.momentum}`}>
                  {getMomentumIcon(spot.momentum)}
                </span>
              </div>
              {spot.drivers && spot.drivers.length > 0 && (
                <div className="hotspot-drivers">
                  {spot.drivers.slice(0, 2).map((d, i) => (
                    <span key={i} className="driver-tag">{d}</span>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}