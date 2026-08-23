import { useEffect, useState } from 'react'
import { deleteDraft as deleteDraftApi, fetchDrafts } from '../api.js'

function timeAgo(isoString) {
  const diff = (Date.now() - new Date(isoString).getTime()) / 1000
  if (diff < 60) return 'just now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  return `${Math.floor(diff / 86400)}d ago`
}

export default function HistoryDrawer({ open, onClose, onLoad, siteKinds, palettes, activeDraftId }) {
  const [drafts, setDrafts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [deletingId, setDeletingId] = useState(null)

  useEffect(() => {
    if (!open) return
    setLoading(true)
    setError(null)
    fetchDrafts()
      .then((data) => setDrafts(data.drafts))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [open])

  useEffect(() => {
    function onKeyDown(e) {
      if (e.key === 'Escape') onClose()
    }
    if (open) document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [open, onClose])

  async function handleDelete(id) {
    if (!window.confirm("Delete this draft? This can't be undone.")) return
    setDeletingId(id)
    try {
      await deleteDraftApi(id)
      setDrafts((prev) => prev.filter((draft) => draft.id !== id))
    } catch (err) {
      setError(err.message)
    } finally {
      setDeletingId(null)
    }
  }

  if (!open) return null

  return (
    <div className="drawer-overlay" onClick={onClose}>
      <aside className="drawer" onClick={(e) => e.stopPropagation()}>
        <div className="drawer-header">
          <h2>Drafts</h2>
          <button type="button" className="drawer-close" onClick={onClose} aria-label="Close drafts panel">
            &times;
          </button>
        </div>

        {loading && <p className="drawer-status">Loading&hellip;</p>}
        {error && <p className="error-text">{error}</p>}
        {!loading && drafts.length === 0 && !error && (
          <p className="drawer-status">
            No saved drafts yet. Generate a site and it&rsquo;ll show up here automatically.
          </p>
        )}

        <ul className="drawer-list">
          {drafts.map((d) => {
            const kind = siteKinds[d.site_kind]
            const typeLabel = kind?.types.find((t) => t.id === d.type_id)?.label || d.type_id
            const paletteColor = palettes.find((p) => p.id === d.palette_id)?.vars['--color-primary']
            return (
              <li key={d.id} className={`drawer-item ${activeDraftId === d.id ? 'active' : ''}`}>
                <button type="button" className="drawer-item-main" onClick={() => onLoad(d.id)}>
                  <span className="drawer-item-dot" style={{ background: paletteColor || '#666' }} />
                  <span className="drawer-item-text">
                    <strong>{d.title}</strong>
                    <span>{kind?.label || d.site_kind} &middot; {typeLabel} &middot; {timeAgo(d.updated_at)}</span>
                  </span>
                </button>
                <button
                  type="button"
                  className="drawer-item-delete"
                  aria-label={`Delete draft for ${d.title}`}
                  onClick={() => handleDelete(d.id)}
                  disabled={deletingId === d.id}
                >
                  {deletingId === d.id ? '\u2026' : '\u00d7'}
                </button>
              </li>
            )
          })}
        </ul>
      </aside>
    </div>
  )
}
