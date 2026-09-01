import { useState } from 'react'
import {
  Check,
  ChevronDown,
  CircleAlert,
  Columns3,
  IdCard,
  ImageUp,
  Loader2,
  Palette,
  Speech,
  SlidersHorizontal,
  SwatchBook,
  Trash2,
  Wand2,
} from 'lucide-react'
import { uploadImage } from '../api.js'

const COLOR_FIELDS = [
  ['primary', 'Primary'], ['background', 'Background'], ['surface', 'Surface'],
  ['text', 'Text'], ['textMuted', 'Muted text'], ['border', 'Border'],
]

export default function DashboardForm({ form, setForm, types, palettes, onSubmit, loading }) {
  const [uploadingLogo, setUploadingLogo] = useState(false)
  const [uploadError, setUploadError] = useState(null)

  function update(key, value) {
    setForm((f) => ({ ...f, [key]: value }))
  }

  function updateField(key, value) {
    setForm((f) => ({ ...f, fields: { ...f.fields, [key]: value } }))
  }

  const activePalette = palettes.find((p) => p.id === form.paletteId)
  const isCustomColors = !!form.customColors
  const activeType = types.find((t) => t.id === form.typeId)

  function enableCustomColors() {
    const base = activePalette || palettes[0]
    const vars = base?.vars || {}
    update('customColors', {
      primary: vars['--color-primary'] || '#1e3a5f',
      background: vars['--color-bg'] || '#ffffff',
      surface: vars['--color-surface'] || '#f4f6f9',
      text: vars['--color-text'] || '#1a1f26',
      textMuted: vars['--color-text-muted'] || '#5a6472',
      border: vars['--color-border'] || '#dde3ea',
    })
  }

  function updateCustomColor(key, value) {
    setForm((f) => ({ ...f, customColors: { ...f.customColors, [key]: value } }))
  }

  async function handleLogoChange(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setUploadingLogo(true)
    setUploadError(null)
    try {
      const { dataUri } = await uploadImage(file)
      update('logoDataUri', dataUri)
    } catch (err) {
      setUploadError(err.message)
    } finally {
      setUploadingLogo(false)
      e.target.value = ''
    }
  }

  return (
    <form className="panel form-panel" onSubmit={onSubmit}>
      <h2 className="panel-title">
        <span className="step-tag">STEP 01</span> Dashboard details
      </h2>

      <div className="section-label"><IdCard aria-hidden="true" />Identity</div>

      <label className="field">
        <span className="field-label">Product name</span>
        <input type="text" value={form.fields.productName} onChange={(e) => updateField('productName', e.target.value)} placeholder="MetricFlow" required />
      </label>

      <div className="field">
        <span className="field-label">Dashboard type</span>
        <div className="type-grid">
          {types.map((t) => (
            <button type="button" key={t.id} className={`type-chip ${form.typeId === t.id ? 'active' : ''}`} onClick={() => update('typeId', t.id)}>
              {t.label}
              {form.typeId === t.id && <Check className="type-chip-check" aria-hidden="true" />}
            </button>
          ))}
        </div>
      </div>

      <label className="field">
        <span className="field-label">What does it do? (optional - helps the AI write the welcome copy)</span>
        <input type="text" value={form.fields.descriptionHint} onChange={(e) => updateField('descriptionHint', e.target.value)} placeholder="Analytics for small SaaS teams" />
      </label>

      <div className="field">
        <span className="field-label">Logo (optional)</span>
        {form.logoDataUri ? (
          <div className="logo-preview">
            <img src={form.logoDataUri} alt="Uploaded logo preview" />
            <button type="button" onClick={() => update('logoDataUri', null)}>
              <Trash2 aria-hidden="true" />
              Remove
            </button>
          </div>
        ) : (
          <label className="file-input">
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleLogoChange} disabled={uploadingLogo} />
            {uploadingLogo ? <Loader2 className="spin" aria-hidden="true" /> : <ImageUp aria-hidden="true" />}
            <span>{uploadingLogo ? 'Uploading\u2026' : 'Choose an image\u2026'}</span>
          </label>
        )}
        {uploadError && <p className="error-text small"><CircleAlert aria-hidden="true" />{uploadError}</p>}
      </div>

      <div className="section-label"><Palette aria-hidden="true" />Appearance</div>

      <div className="field">
        <span className="field-label">Color palette</span>
        <div className="palette-mode-toggle">
          <button type="button" className={!isCustomColors ? 'active' : ''} onClick={() => update('customColors', null)}>
            <SwatchBook aria-hidden="true" />
            Curated
          </button>
          <button type="button" className={isCustomColors ? 'active' : ''} onClick={enableCustomColors}>
            <SlidersHorizontal aria-hidden="true" />
            Custom
          </button>
        </div>

        {!isCustomColors && (
          <>
            <div className="palette-row">
              {palettes.map((p) => (
                <button
                  type="button" key={p.id} title={p.name}
                  className={`palette-swatch ${form.paletteId === p.id ? 'active' : ''}`}
                  style={{ background: `linear-gradient(135deg, ${p.vars['--color-primary']} 50%, ${p.vars['--color-bg']} 50%)` }}
                  onClick={() => update('paletteId', p.id)}
                >
                  {form.paletteId === p.id && <Check className="palette-swatch-check" aria-hidden="true" />}
                </button>
              ))}
            </div>
            {activePalette && <p className="palette-caption">{activePalette.name} - {activePalette.description}</p>}
          </>
        )}

        {isCustomColors && (
          <div className="custom-color-grid">
            {COLOR_FIELDS.map(([key, label]) => (
              <label key={key} className="custom-color-field">
                <input type="color" value={form.customColors[key]} onChange={(e) => updateCustomColor(key, e.target.value)} />
                <span className="custom-color-field-text">
                  <span>{label}</span>
                  <span className="custom-color-hex">{form.customColors[key]}</span>
                </span>
              </label>
            ))}
          </div>
        )}
      </div>

      <div className="section-label"><Columns3 aria-hidden="true" />Layout</div>

      <label className="field">
        <span className="field-label">Sidebar nav items (comma-separated)</span>
        <input
          type="text" value={form.fields.navItems} onChange={(e) => updateField('navItems', e.target.value)}
          placeholder={activeType ? `e.g. ${activeType.label === 'SaaS Analytics' ? 'Overview, Analytics, Customers, Settings' : 'leave blank for defaults'}` : 'Overview, Analytics, Settings'}
        />
      </label>

      <label className="field">
        <span className="field-label">Stat card labels (comma-separated, up to 4)</span>
        <input type="text" value={form.fields.statLabels} onChange={(e) => updateField('statLabels', e.target.value)} placeholder="Revenue, Active Users, Conversion Rate, Churn Rate" />
        <p className="field-hint">Values shown are clearly-labeled sample data, not real numbers.</p>
      </label>

      <div className="section-label"><Speech aria-hidden="true" />Voice</div>

      <label className="field">
        <span className="field-label">Tone</span>
        <span className="select-wrap">
          <select value={form.fields.tone} onChange={(e) => updateField('tone', e.target.value)}>
            <option value="professional">Professional</option>
            <option value="friendly">Friendly</option>
            <option value="premium">Premium</option>
          </select>
          <ChevronDown className="select-chevron" aria-hidden="true" />
        </span>
      </label>

      <button type="submit" className="generate-btn" disabled={loading}>
        {loading ? <Loader2 className="spin" aria-hidden="true" /> : <Wand2 aria-hidden="true" />}
        {loading ? 'Generating\u2026' : 'Generate dashboard'}
      </button>
    </form>
  )
}
