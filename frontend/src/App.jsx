import { useEffect, useState } from 'react'
import { FilePlus2, History, WifiOff } from 'lucide-react'
import KindSelector from './components/KindSelector.jsx'
import BusinessForm from './components/BusinessForm.jsx'
import PortfolioForm from './components/PortfolioForm.jsx'
import DashboardForm from './components/DashboardForm.jsx'
import PreviewPane from './components/PreviewPane.jsx'
import HistoryDrawer from './components/HistoryDrawer.jsx'
import { fetchMeta, generateSite, exportSite, fetchDraft } from './api.js'
import { DEFAULT_FIELDS, emptyForm } from './defaults.js'

const FORM_COMPONENTS = {
  business: BusinessForm,
  portfolio: PortfolioForm,
  dashboard: DashboardForm,
}

export default function App() {
  const [meta, setMeta] = useState({ siteKinds: {}, palettes: [], activeProvider: null, providerDisplayNames: {} })
  const [form, setForm] = useState(emptyForm('business'))
  const [draftId, setDraftId] = useState(null)
  const [site, setSite] = useState(null)
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)
  const [error, setError] = useState(null)
  const [metaError, setMetaError] = useState(null)
  const [historyOpen, setHistoryOpen] = useState(false)

  useEffect(() => {
    fetchMeta()
      .then((data) => {
        setMeta(data)
        const firstType = data.siteKinds.business?.types[0]?.id || ''
        const firstPalette = data.palettes[0]?.id || ''
        setForm(emptyForm('business', firstType, firstPalette))
      })
      .catch((e) => setMetaError(e.message))
  }, [])

  function handleKindChange(newKind) {
    const firstType = meta.siteKinds[newKind]?.types[0]?.id || ''
    setForm((f) => ({
      ...f,
      siteKind: newKind,
      typeId: firstType,
      fields: { ...DEFAULT_FIELDS[newKind] },
    }))
    setSite(null)
    setDraftId(null)
    setError(null)
  }

  function currentTitle() {
    const f = form.fields
    if (form.siteKind === 'business') return f.businessName
    if (form.siteKind === 'portfolio') return f.name
    if (form.siteKind === 'dashboard') return f.productName
    return ''
  }

  async function handleGenerate(e) {
    e?.preventDefault()
    if (!currentTitle().trim() || !form.typeId) {
      setError('Fill in a name and pick a type before generating.')
      return
    }
    setLoading(true)
    setError(null)
    try {
      const result = await generateSite({ ...form, draftId })
      setSite(result)
      setDraftId(result.draftId)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleDownload() {
    if (!site) return
    setDownloading(true)
    setError(null)
    try {
      await exportSite({ html: site.html, css: site.css, title: site.title })
    } catch (err) {
      setError(err.message)
    } finally {
      setDownloading(false)
    }
  }

  async function handleLoadDraft(id) {
    setHistoryOpen(false)
    setLoading(true)
    setError(null)
    try {
      const result = await fetchDraft(id)
      setForm({
        siteKind: result.form.siteKind,
        typeId: result.form.typeId,
        paletteId: result.form.paletteId,
        customColors: result.form.customColors,
        logoDataUri: result.form.logoDataUri,
        fields: { ...DEFAULT_FIELDS[result.form.siteKind], ...result.form.fields },
      })
      setSite(result)
      setDraftId(result.draftId)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleNewSite() {
    const firstType = meta.siteKinds[form.siteKind]?.types[0]?.id || ''
    const firstPalette = meta.palettes[0]?.id || ''
    setForm(emptyForm(form.siteKind, firstType, firstPalette))
    setSite(null)
    setDraftId(null)
    setError(null)
  }

  const FormComponent = FORM_COMPONENTS[form.siteKind]
  const providerLabel = meta.activeProvider
    ? `Powered by ${meta.providerDisplayNames[meta.activeProvider] || meta.activeProvider}`
    : 'No AI key set - using placeholder copy'

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <span className="brand-mark-wrap">
            <svg className="brand-mark" width="20" height="20" viewBox="0 0 26 26" fill="none" stroke="currentColor" strokeWidth="1.5">
              <circle cx="13" cy="13" r="8" />
              <path d="M13 1v6M13 19v6M1 13h6M19 13h6" />
              <circle cx="13" cy="13" r="1.8" fill="currentColor" stroke="none" />
            </svg>
          </span>
          <div>
            <h1>Frontage</h1>
            <p className="brand-sub">SITES, PORTFOLIOS &amp; DASHBOARDS - DRAFT TO ZIP</p>
          </div>
        </div>
        <div className="header-actions">
          <span className={`provider-badge ${meta.activeProvider ? 'active' : ''}`}>
            <span className="badge-dot" aria-hidden="true" />
            <span>{providerLabel}</span>
          </span>
          <button type="button" className="header-btn" onClick={handleNewSite}>
            <FilePlus2 aria-hidden="true" />
            New site
          </button>
          <button type="button" className="header-btn" onClick={() => setHistoryOpen(true)}>
            <History aria-hidden="true" />
            Drafts
          </button>
        </div>
      </header>

      {metaError && (
        <div className="meta-error">
          <WifiOff className="meta-error-icon" aria-hidden="true" />
          <p>
            Couldn&rsquo;t reach the backend at the configured API URL. Make sure the Flask
            server is running (<code>python app.py</code> in <code>backend/</code>). ({metaError})
          </p>
        </div>
      )}

      <KindSelector siteKinds={meta.siteKinds} activeKind={form.siteKind} onChange={handleKindChange} />

      <main className="app-body">
        {FormComponent && (
          <FormComponent
            form={form}
            setForm={setForm}
            types={meta.siteKinds[form.siteKind]?.types || []}
            palettes={meta.palettes}
            onSubmit={handleGenerate}
            loading={loading}
          />
        )}
        <PreviewPane
          form={form}
          types={meta.siteKinds[form.siteKind]?.types || []}
          palettes={meta.palettes}
          site={site}
          loading={loading}
          downloading={downloading}
          error={error}
          onRegenerate={handleGenerate}
          onDownload={handleDownload}
        />
      </main>

      <HistoryDrawer
        open={historyOpen}
        onClose={() => setHistoryOpen(false)}
        onLoad={handleLoadDraft}
        siteKinds={meta.siteKinds}
        palettes={meta.palettes}
        activeDraftId={draftId}
      />
    </div>
  )
}
