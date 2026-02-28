import { bandForScore } from '../utils'

export function CountryDetailPanel({ country }) {
  const band = bandForScore(country.riskScore)

  return (
    <aside className="panel details">
      <h3>Country Detail</h3>
      <div className="country-head">
        <h2>{country.country}</h2>
        <span className="pill" style={{ backgroundColor: band.color }}>
          {band.label}
        </span>
      </div>

      <div className="metrics">
        <article>
          <span>Risk Score</span>
          <strong>{country.riskScore}</strong>
        </article>
        <article>
          <span>Momentum</span>
          <strong>{country.momentum}</strong>
        </article>
        <article>
          <span>Confidence</span>
          <strong>{country.confidence}%</strong>
        </article>
      </div>

      <div>
        <h4>Top Drivers</h4>
        <ul className="tag-list">
          {country.drivers.map((driver) => (
            <li key={driver}>{driver}</li>
          ))}
        </ul>
      </div>

      <p className="note">
        Risk indicates probability, not certainty. This panel is currently wired to
        sample API JSON for MVP validation.
      </p>
    </aside>
  )
}
