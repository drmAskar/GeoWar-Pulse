import { bandForScore } from '../utils'

export function HotspotsList({ hotspots, onSelect }) {
  return (
    <div className="panel hotspots">
      <h3>Top Hotspots</h3>
      <ul>
        {hotspots.map((spot) => {
          const band = bandForScore(spot.riskScore)
          return (
            <li key={spot.code}>
              <button onClick={() => onSelect(spot)}>
                <div>
                  <strong>{spot.country}</strong>
                  <span>{spot.momentum}</span>
                </div>
                <span className="pill" style={{ backgroundColor: band.color }}>
                  {spot.riskScore}
                </span>
              </button>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
