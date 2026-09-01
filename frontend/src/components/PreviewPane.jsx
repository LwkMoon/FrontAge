import { CircleAlert, Download, LayoutTemplate, Loader2, Lock, RotateCw } from 'lucide-react'

const PROVIDER_LABELS = { anthropic: 'Claude', openai: 'OpenAI', gemini: 'Gemini' }

function currentTitle(form) {
  const f = form.fields
  if (form.siteKind === 'business') return f.businessName
  if (form.siteKind === 'portfolio') return f.name
  if (form.siteKind === 'dashboard') return f.productName
  return ''
}

function fakeDomain(title) {
  const slug = (title || '').trim().toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
  return slug ? `${slug}.com` : 'yoursite.com'
}

export default function PreviewPane({ form, types, palettes, site, loading, downloading, error, onRegenerate, onDownload }) {
  const typeLabel = types.find((t) => t.id === form.typeId)?.label || '-'
  const paletteName = form.customColors ? 'Custom' : (palettes.find((p) => p.id === form.paletteId)?.name || '-')

  let copyStatus = '-'
  if (site) {
    copyStatus = site.aiGenerated
      ? `AI (${PROVIDER_LABELS[site.aiProvider] || site.aiProvider})`
      : 'PLACEHOLDER'
  }

  return (
    <section className="panel preview-panel">
      <h2 className="panel-title">
        <span className="step-tag">STEP 02</span> Preview
      </h2>

      <div className="title-block">
        <span className="title-block-tick tl" aria-hidden="true" />
        <span className="title-block-tick tr" aria-hidden="true" />
        <span className="title-block-tick bl" aria-hidden="true" />
        <span className="title-block-tick br" aria-hidden="true" />
        <div className="title-block-grid">
          <div className="title-block-field">
            <span>TITLE</span>
            <strong>{currentTitle(form) || '-'}</strong>
          </div>
          <div className="title-block-field">
            <span>TYPE</span>
            <strong>{typeLabel}</strong>
          </div>
          <div className="title-block-field">
            <span>PALETTE</span>
            <strong>{paletteName}</strong>
          </div>
          <div className="title-block-field">
            <span>COPY</span>
            <strong className={site?.aiGenerated ? 'copy-ai' : ''}>{copyStatus}</strong>
          </div>
        </div>
      </div>

      <div className="browser-frame">
        <div className="browser-chrome">
          <span className="chrome-dots">
            <span className="dot dot-red" />
            <span className="dot dot-amber" />
            <span className="dot dot-green" />
          </span>
          <div className="address-bar">
            <Lock aria-hidden="true" />
            <span>{fakeDomain(currentTitle(form))}</span>
          </div>
        </div>
        <div className="browser-viewport">
          {!site && !loading && (
            <div className="empty-state">
              <LayoutTemplate className="empty-state-icon" aria-hidden="true" />
              <p>Fill in the details and generate a site to preview it here.</p>
            </div>
          )}
          {loading && (
            <div className="empty-state">
              <Loader2 className="empty-state-icon spin" aria-hidden="true" />
              <p>Building your site&hellip;</p>
            </div>
          )}
          {site && !loading && (
            <iframe title="Site preview" srcDoc={site.previewHtml} className="preview-iframe" />
          )}
        </div>
      </div>

      {error && <p className="error-text"><CircleAlert aria-hidden="true" />{error}</p>}

      {site && (
        <div className="preview-actions">
          <button type="button" onClick={onRegenerate} disabled={loading}>
            <RotateCw aria-hidden="true" />
            Regenerate copy
          </button>
          <button type="button" className="primary" onClick={onDownload} disabled={downloading}>
            {downloading ? <Loader2 className="spin" aria-hidden="true" /> : <Download aria-hidden="true" />}
            {downloading ? 'Preparing ZIP\u2026' : 'Download ZIP'}
          </button>
        </div>
      )}
    </section>
  )
}
