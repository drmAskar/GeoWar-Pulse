import { riskBands } from './data/sampleApiResponse'

export function bandForScore(score) {
  if (score >= 75) return riskBands[3]
  if (score >= 50) return riskBands[2]
  if (score >= 25) return riskBands[1]
  return riskBands[0]
}
