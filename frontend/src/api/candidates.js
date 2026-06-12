import { apiFetch } from './client'

export const SCORE_CATEGORIES = [
  'Technical Skills',
  'Communication',
  'Problem Solving',
  'Culture Fit',
  'Experience',
]

export const CANDIDATE_STATUSES = ['new', 'reviewed', 'hired', 'rejected']

export function fetchCandidates(filters, page, pageSize) {
  return apiFetch('/candidates', {
    params: { ...filters, page, page_size: pageSize },
  })
}

export function fetchCandidateDetail(id) {
  return apiFetch(`/candidates/${id}`)
}

export function submitScore(id, { category, score, note }) {
  return apiFetch(`/candidates/${id}/scores`, {
    method: 'POST',
    body: { category, score, note },
  })
}

export function updateNotes(id, internalNotes) {
  return apiFetch(`/candidates/${id}/notes`, {
    method: 'PATCH',
    body: { internal_notes: internalNotes },
  })
}

export function generateAiSummary(id) {
  return apiFetch(`/candidates/${id}/ai-summary`, { method: 'POST' })
}
