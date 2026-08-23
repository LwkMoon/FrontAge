const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

async function request(path, options) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.error || `Request failed (${res.status})`)
  }
  return res
}

export async function fetchMeta() {
  const res = await request('/api/meta')
  return res.json()
}

export async function uploadImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_URL}/api/upload-image`, { method: 'POST', body: formData })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.error || `Upload failed (${res.status})`)
  }
  return res.json()
}

export async function generateSite(payload) {
  const res = await request('/api/generate', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  return res.json()
}

export async function fetchDrafts() {
  const res = await request('/api/drafts')
  return res.json()
}

export async function fetchDraft(id) {
  const res = await request(`/api/drafts/${id}`)
  return res.json()
}

export async function deleteDraft(id) {
  const res = await request(`/api/drafts/${id}`, { method: 'DELETE' })
  return res.json()
}

export async function exportSite({ html, css, title }) {
  const res = await fetch(`${API_URL}/api/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ html, css, title }),
  })

  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.error || `Export failed (${res.status})`)
  }

  const contentType = res.headers.get('Content-Type') || ''
  if (!contentType.includes('zip')) {
    throw new Error('The server did not return a valid zip file. Check the backend terminal for errors.')
  }

  const blob = await res.blob()
  if (!blob || blob.size === 0) {
    throw new Error('The exported file came back empty. Please try again.')
  }

  const disposition = res.headers.get('Content-Disposition') || ''
  const match = disposition.match(/filename="?([^"]+)"?/)
  const fallbackName = `${(title || 'site').trim().toLowerCase().replace(/\s+/g, '-')}-site.zip`
  const filename = match ? match[1] : fallbackName

  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}
