import { riskBands } from '../data/sampleApiResponse'

export function RiskLegend() {
  return (
    <div className="panel risk-legend">
      <h3>Risk Legend</h3>
      <div className="legend-list">
        {riskBands.map((band) => (
          <div key={band.label} className="legend-item">
            <span className="swatch" style={{ backgroundColor: band.color }} />
            <div>
              <strong>{band.label}</strong>
              <p>{band.range}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
