const ICON_PATHS = {
  business: (
    <>
      <path d="M3 9l1-5h16l1 5" />
      <path d="M4 9v10h16V9" />
      <path d="M9 19v-6h6v6" />
    </>
  ),
  portfolio: (
    <>
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21c0-4 4-6 8-6s8 2 8 6" />
    </>
  ),
  dashboard: (
    <>
      <rect x="3" y="3" width="8" height="8" rx="1.5" />
      <rect x="13" y="3" width="8" height="8" rx="1.5" />
      <rect x="3" y="13" width="8" height="8" rx="1.5" />
      <rect x="13" y="13" width="8" height="8" rx="1.5" />
    </>
  ),
}

export default function KindSelector({ siteKinds, activeKind, onChange }) {
  const kindIds = Object.keys(siteKinds)
  if (kindIds.length === 0) return null

  return (
    <div className="kind-selector">
      {kindIds.map((id) => (
        <button
          type="button"
          key={id}
          className={`kind-tab ${activeKind === id ? 'active' : ''}`}
          onClick={() => onChange(id)}
        >
          <svg className="kind-tab-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7">
            {ICON_PATHS[id]}
          </svg>
          <span className="kind-tab-text">
            <strong>{siteKinds[id].label}</strong>
            <span>{siteKinds[id].description}</span>
          </span>
        </button>
      ))}
    </div>
  )
}
