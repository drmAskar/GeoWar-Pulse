export const riskBands = [
  { label: 'Low', range: '0-24', color: '#2FBF71' },
  { label: 'Elevated', range: '25-49', color: '#F2C14E' },
  { label: 'High', range: '50-74', color: '#F28C38' },
  { label: 'Critical', range: '75-100', color: '#E6534B' },
]

export const hotspots = [
  {
    code: 'UA',
    country: 'Ukraine',
    riskScore: 84,
    momentum: '+6 in 24h',
    confidence: 78,
    drivers: ['Border shelling', 'Drone strikes'],
    coords: { x: 58, y: 34 },
  },
  {
    code: 'IL',
    country: 'Israel',
    riskScore: 81,
    momentum: '+9 in 24h',
    confidence: 74,
    drivers: ['Rocket exchanges', 'Regional rhetoric'],
    coords: { x: 56, y: 42 },
  },
  {
    code: 'TW',
    country: 'Taiwan',
    riskScore: 68,
    momentum: '+4 in 24h',
    confidence: 69,
    drivers: ['Naval movements', 'Airspace activity'],
    coords: { x: 77, y: 44 },
  },
  {
    code: 'VE',
    country: 'Venezuela',
    riskScore: 52,
    momentum: '+3 in 24h',
    confidence: 61,
    drivers: ['Election tensions', 'Sanctions pressure'],
    coords: { x: 28, y: 49 },
  },
]
