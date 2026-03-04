import { useState, useEffect, useCallback } from 'react'
import { RiskMap } from './components/RiskMap'
import { CountryDetailPanel } from './components/CountryDetailPanel'
import { HotspotsList } from './components/HotspotsList'
import { RiskLegend } from './components/RiskLegend'
import api from './services/api'
import './styles.css'

// Fallback sample data if API unavailable
import { hotspots as sampleHotspots, riskBands } from './data/sampleApiResponse'

export default function App() {
  const [hotspots, setHotspots] = useState([])
  const [selected, setSelected] = useState(null)
  const [window, setWindow] = useState('24h')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [useSampleData, setUseSampleData] = useState(false)

  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.getMapSnapshot(window)
      setHotspots(data.hotspots)
      setUseSampleData(false)
    } catch (err) {
      console.error('API error, using sample data:', err)
      setError(err.message)
      // Fall back to sample data
      setHotspots(sampleHotspots)
      setUseSampleData(true)
    } finally {
      setLoading(false)
    }
  }, [window])

  useEffect(() => {
    loadData()
  }, [loadData])

  // Auto-refresh every 5 minutes
  useEffect(() => {
    const interval = setInterval(loadData, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [loadData])

  const handleSelect = (spot) => {
    setSelected(spot)
  }

  const handleCloseDetail = () => {
    setSelected(null)
  }

  const handleWindowChange = (newWindow) => {
    setWindow(newWindow)
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🌍 GeoWar Pulse</h1>
          <p className="subtitle">Real-time Global Conflict Risk Monitoring</p>
        </div>
        <div className="header-controls">
          <div className="window-selector">
            <button 
              className={window === '24h' ? 'active' : ''} 
              onClick={() => handleWindowChange('24h')}
            >
              24h
            </button>
            <button 
              className={window === '7d' ? 'active' : ''} 
              onClick={() => handleWindowChange('7d')}
            >
              7d
            </button>
            <button 
              className={window === '30d' ? 'active' : ''} 
              onClick={() => handleWindowChange('30d')}
            >
              30d
            </button>
          </div>
        </div>
      </header>

      <main className="app-main">
        {loading && hotspots.length === 0 ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading conflict risk data...</p>
          </div>
        ) : error && useSampleData ? (
          <div className="error-banner">
            <span>⚠️ Using cached data (API: {error})</span>
            <button onClick={loadData}>Retry</button>
          </div>
        ) : null}

        <div className="content-grid">
          <div className="map-section">
            <RiskMap 
              hotspots={hotspots} 
              selected={selected} 
              onSelect={handleSelect} 
            />
            <RiskLegend bands={riskBands} />
          </div>

          <div className="sidebar">
            <HotspotsList 
              hotspots={hotspots} 
              selected={selected}
              onSelect={handleSelect}
            />
          </div>
        </div>

        {selected && (
          <CountryDetailPanel 
            country={selected}
            onClose={handleCloseDetail}
          />
        )}
      </main>

      <footer className="app-footer">
        <span className="data-source">
          {useSampleData ? '📊 Sample Data' : '🔴 Live API'}
        </span>
        <span className="timestamp">
          Last updated: {new Date().toLocaleTimeString()}
        </span>
      </footer>
    </div>
  )
}