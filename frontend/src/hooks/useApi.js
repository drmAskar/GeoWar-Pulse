import { useState, useEffect } from 'react';

/**
 * Custom hook to fetch hotspot data from the backend API
 * @returns {{
 *   hotspots: Array<{
 *     code: string,
 *     country: string,
 *     riskScore: number,
 *     momentum: string,
 *     confidence: number,
 *     drivers: string[],
 *     coords: { x: number, y: number }
 *   }>,
 *   loading: boolean,
 *   error: string|null
 * }}
 */
export function useApi() {
  const [hotspots, setHotspots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHotspots = async () => {
      try {
        setLoading(true);
        // Try to fetch from backend API - adjust URL based on your deployment
        const response = await fetch('http://localhost:8000/scores?window=24h');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Transform backend response to match frontend hotspot structure
        const transformedHotspots = data.items.map(item => ({
          code: item.country_code, // Use full 3-letter country code
          country: countryCodeToName(item.country_code),
          riskScore: Math.round(item.score),
          momentum: formatMomentum(item.delta_24h),
          confidence: Math.round(item.confidence),
          drivers: item.top_drivers || [],
          coords: getCoordinates(item.country_code)
        }));
        
        setHotspots(transformedHotspots);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch hotspots from API, using sample data:', err);
        // Fallback to sample data if API fails
        import('../data/sampleApiResponse.js').then(({ sampleHotspots }) => {
          setHotspots(sampleHotspots);
          setError(`API Error: ${err.message} - Using sample data`);
        }).catch(() => {
          setError('Failed to load any data');
        });
      } finally {
        setLoading(false);
      }
    };

    fetchHotspots();
    
    // Set up polling every 30 seconds for updates
    const intervalId = setInterval(fetchHotspots, 30000);
    
    return () => clearInterval(intervalId);
  }, []);

  return { hotspots, loading, error };
}

/**
 * Convert country code to country name (simplified - expand as needed)
 * @param {string} code - ISO country code (3 letters)
 * @returns {string} Country name
 */
function countryCodeToName(code) {
  const countryMap = {
    'UKR': 'Ukraine',
    'TWN': 'Taiwan',
    'ISR': 'Israel',
    'RUS': 'Russia',
    'CHN': 'China',
    'USA': 'United States',
    'IND': 'India',
    'PAK': 'Pakistan',
    'IRN': 'Iran',
    'SAU': 'Saudi Arabia',
    'GBR': 'United Kingdom',
    'FRA': 'France',
    'DEU': 'Germany',
    'JPN': 'Japan',
    'KOR': 'South Korea',
    'PRK': 'North Korea',
    'SYR': 'Syria',
    'YEM': 'Yemen',
    'AFG': 'Afghanistan',
    'IRQ': 'Iraq'
  };
  
  return countryMap[code] || code;
}

/**
 * Format delta value into momentum string
 * @param {number} delta - 24h delta value
 * @returns {string} Formatted momentum string
 */
function formatMomentum(delta) {
  const sign = delta >= 0 ? '+' : '';
  return `${sign}${delta.toFixed(1)} in 24h`;
}

/**
 * Get coordinates for a country (simplified mock coordinates)
 * @param {string} code - Country code
 * @returns {{x: number, y: number}} Coordinates
 */
function getCoordinates(code) {
  const coordMap = {
    'UKR': { x: 58, y: 34 },
    'TWN': { x: 77, y: 44 },
    'ISR': { x: 56, y: 42 }
  };
  
  return coordMap[code] || { x: 50, y: 50 };
}