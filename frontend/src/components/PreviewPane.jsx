const PROVIDER_LABELS = { anthropic: 'Claude', openai: 'OpenAI', gemini: 'Gemini' }

function currentTitle(form) {
  const f = form.fields
  if (form.siteKind === 'business') return f.businessName
  if (form.siteKind === 'portfolio') return f.name
  if (form.siteKind === 'dashboard') return f.productName
  return ''
}

export default function PreviewPane({ form, types, palettes, site, loading, downloading, error, onRegenerate, onDownload }) {
  const typeLabel = types.find((t) => t.id === form.typeId)?.label || '\u2014'
  const paletteName = form.customColors ? 'Custom' : (palettes.find((p) => p.id === form.paletteId)?.name || '\u2014')

  let copyStatus = '\u2014'
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
        <div className="title-block-field">
          <span>TITLE</span>
          <strong>{currentTitle(form) || '\u2014'}</strong>
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

      <div className="browser-frame">
        <div className="browser-chrome">
          <span className="dot" /><span className="dot" /><span className="dot" />
        </div>
        <div className="browser-viewport">
          {!site && !loading && (
            <div className="empty-state">Fill in the details and generate a site to preview it here.</div>
          )}
          {loading && <div className="empty-state">Building your site&hellip;</div>}
          {site && !loading && (
            <iframe title="Site preview" srcDoc={site.previewHtml} className="preview-iframe" />
          )}
        </div>
      </div>

      {error && <p className="error-text">{error}</p>}

      {site && (
        <div className="preview-actions">
          <button type="button" onClick={onRegenerate} disabled={loading}>
            Regenerate copy
          </button>
          <button type="button" className="primary" onClick={onDownload} disabled={downloading}>
            {downloading ? 'Preparing ZIP\u2026' : 'Download ZIP'}
          </button>
        </div>
      )}
    </section>
  )
}
