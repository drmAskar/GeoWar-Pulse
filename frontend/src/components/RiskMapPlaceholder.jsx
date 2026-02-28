import { bandForScore } from '../utils'

export function RiskMapPlaceholder({ hotspots, selected, onSelect }) {
  return (
    <div className="panel map-wrap">
      <div className="map-header">
        <h2>Global Risk Map</h2>
        <span className="updated">Updated 5m ago</span>
      </div>
      <div className="map-canvas" role="img" aria-label="World map risk placeholder">
        <div className="map-grid" />
        {hotspots.map((spot) => {
          const band = bandForScore(spot.riskScore)
          const isActive = selected.code === spot.code
          return (
            <button
              key={spot.code}
              className={`marker ${isActive ? 'active' : ''}`}
              style={{ left: `${spot.coords.x}%`, top: `${spot.coords.y}%`, backgroundColor: band.color }}
              onClick={() => onSelect(spot)}
              title={`${spot.country} — ${spot.riskScore}`}
            >
              <span>{spot.code}</span>
            </button>
          )
        })}
        <p className="map-caption">MVP map placeholder with interactive country markers.</p>
      </div>
    </div>
  )
}
