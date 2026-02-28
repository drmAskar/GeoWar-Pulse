import { useMemo, useState } from 'react'
import { hotspots } from './data/sampleApiResponse'
import { RiskLegend } from './components/RiskLegend'
import { HotspotsList } from './components/HotspotsList'
import { CountryDetailPanel } from './components/CountryDetailPanel'
import { RiskMapPlaceholder } from './components/RiskMapPlaceholder'

export default function App() {
  const sortedHotspots = useMemo(
    () => [...hotspots].sort((a, b) => b.riskScore - a.riskScore),
    [],
  )
  const [selectedCountry, setSelectedCountry] = useState(sortedHotspots[0])

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>GeoWar Pulse</h1>
        <p>Map-first conflict-risk intelligence MVP</p>
      </header>

      <main className="layout">
        <section className="left-column">
          <RiskMapPlaceholder
            hotspots={sortedHotspots}
            selected={selectedCountry}
            onSelect={setSelectedCountry}
          />
          <div className="stack-two">
            <RiskLegend />
            <HotspotsList hotspots={sortedHotspots} onSelect={setSelectedCountry} />
          </div>
        </section>

        <CountryDetailPanel country={selectedCountry} />
      </main>
    </div>
  )
}
