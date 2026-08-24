import { LayoutDashboard, Store, UserRound } from 'lucide-react'

const KIND_ICONS = {
  business: Store,
  portfolio: UserRound,
  dashboard: LayoutDashboard,
}

export default function KindSelector({ siteKinds, activeKind, onChange }) {
  const kindIds = Object.keys(siteKinds)
  if (kindIds.length === 0) return null

  return (
    <div className="kind-selector">
      {kindIds.map((id) => {
        const Icon = KIND_ICONS[id]
        return (
          <button
            type="button"
            key={id}
            className={`kind-tab ${activeKind === id ? 'active' : ''}`}
            onClick={() => onChange(id)}
          >
            <span className="kind-tab-icon-wrap">
              {Icon && <Icon aria-hidden="true" />}
            </span>
            <span className="kind-tab-text">
              <strong>{siteKinds[id].label}</strong>
              <span>{siteKinds[id].description}</span>
            </span>
          </button>
        )
      })}
    </div>
  )
}
