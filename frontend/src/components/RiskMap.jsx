import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { bandForScore } from '../utils'

// Coordinate mapping for countries
const COORD_MAP = {
  'UKR': [49.5, 31.5],    // Ukraine
  'ISR': [31.0461, 34.8516], // Israel
  'TWN': [23.6978, 120.9605], // Taiwan
  'RUS': [61.5240, 105.3188], // Russia
  'CHN': [35.8617, 104.1954], // China
  'USA': [37.0902, -95.7129], // USA
  'IND': [20.5937, 78.9629], // India
  'PAK': [30.3753, 69.3451], // Pakistan
  'IRN': [32.4279, 53.6880], // Iran
  'SAU': [23.8859, 45.0792], // Saudi Arabia
  'PRK': [40.3399, 127.5101], // North Korea
  'KOR': [35.9078, 127.7669], // South Korea
  'VEN': [6.4238, -66.5897], // Venezuela
  'BRA': [-14.2350, -51.9253], // Brazil
  'NGA': [9.0820, 8.6753], // Nigeria
  'EGY': [26.8206, 30.8025], // Egypt
  'SSD': [6.8770, 31.3070], // South Sudan
  'ETH': [9.1450, 40.4897], // Ethiopia
  'COL': [4.5709, -74.2973], // Colombia
  'MEX': [23.6345, -102.5528], // Mexico
}

export function RiskMap({ hotspots, selected, onSelect }) {
  if (!hotspots || hotspots.length === 0) {
    return (
      <div className="panel map-wrap">
        <div className="map-header">
          <h2>Global Risk Map</h2>
          <span className="updated">No data available</span>
        </div>
        <div className="map-canvas" style={{ height: '400px', background: '#1a1a1a' }}>
          <p style={{ textAlign: 'center', paddingTop: '180px', color: '#888' }}>
            Loading conflict risk data...
          </p>
        </div>
      </div>
    )
  }

  const getCoordinates = (code) => {
    return COORD_MAP[code] || [0, 0]
  }

  const getMomentumText = (momentum, delta) => {
    if (momentum === 'escalating') return `↑${delta > 0 ? '+' : ''}${delta} in 24h`
    if (momentum === 'de-escalating') return `↓${delta} in 24h`
    return '→ Stable'
  }

  return (
    <div className="panel map-wrap">
      <div className="map-header">
        <h2>Global Risk Map</h2>
        <span className="updated">Real-time risk visualization</span>
      </div>
      <div className="map-canvas">
        <MapContainer 
          center={[30, 0]} 
          zoom={2} 
          style={{ height: '400px', width: '100%', borderRadius: '8px' }}
          scrollWheelZoom={false}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {hotspots.map((spot) => {
            const band = bandForScore(spot.riskScore)
            const coords = getCoordinates(spot.code)
            const isSelected = selected?.code === spot.code
            
            return (
              <CircleMarker
                key={spot.code}
                center={coords}
                radius={12 + (spot.riskScore / 12)}
                pathOptions={{
                  fillColor: band.color,
                  color: isSelected ? '#fff' : '#666',
                  weight: isSelected ? 3 : 2,
                  opacity: 1,
                  fillOpacity: isSelected ? 0.9 : 0.7,
                }}
                eventHandlers={{
                  click: () => onSelect(spot),
                }}
              >
                <Popup>
                  <div style={{ textAlign: 'center', padding: '4px', minWidth: '120px' }}>
                    <strong style={{ fontSize: '14px' }}>{spot.country}</strong>
                    <br />
                    <span style={{ 
                      color: band.color, 
                      fontWeight: 'bold',
                      fontSize: '18px' 
                    }}>
                      {spot.riskScore}/100
                    </span>
                    <br />
                    <small style={{ color: '#666' }}>{band.label}</small>
                    <br />
                    <hr style={{ margin: '4px 0', borderColor: '#eee' }} />
                    Confidence: {spot.confidence}%
                    <br />
                    <span style={{ 
                      color: spot.momentum === 'escalating' ? '#E6534B' : 
                             spot.momentum === 'de-escalating' ? '#2FBF71' : '#888' 
                    }}>
                      {getMomentumText(spot.momentum, spot.delta || 0)}
                    </span>
                    {spot.drivers && spot.drivers.length > 0 && (
                      <>
                        <br />
                        <small style={{ color: '#888' }}>
                          Top: {spot.drivers.slice(0, 2).join(', ')}
                        </small>
                      </>
                    )}
                  </div>
                </Popup>
              </CircleMarker>
            )
          })}
        </MapContainer>
        <p className="map-caption">
          Interactive world map showing conflict risk scores. Click markers for details.
        </p>
      </div>
    </div>
  )
}