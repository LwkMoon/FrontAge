import { useState } from 'react'
import { uploadImage } from '../api.js'

const COLOR_FIELDS = [
  ['primary', 'Primary'], ['background', 'Background'], ['surface', 'Surface'],
  ['text', 'Text'], ['textMuted', 'Muted text'], ['border', 'Border'],
]

export default function PortfolioForm({ form, setForm, types, palettes, onSubmit, loading }) {
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
  const projects = form.fields.projects || []

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

  function addProject() {
    updateField('projects', [...projects, { name: '', description: '', url: '' }])
  }

  function updateProject(index, key, value) {
    updateField('projects', projects.map((p, i) => (i === index ? { ...p, [key]: value } : p)))
  }

  function removeProject(index) {
    updateField('projects', projects.filter((_, i) => i !== index))
  }

  return (
    <form className="panel form-panel" onSubmit={onSubmit}>
      <h2 className="panel-title">
        <span className="step-tag">STEP 01</span> Portfolio details
      </h2>

      <div className="section-label">Identity</div>

      <div className="field-row">
        <label className="field">
          <span className="field-label">Name</span>
          <input type="text" value={form.fields.name} onChange={(e) => updateField('name', e.target.value)} placeholder="Jane Doe" required />
        </label>
        <label className="field">
          <span className="field-label">Role</span>
          <input type="text" value={form.fields.role} onChange={(e) => updateField('role', e.target.value)} placeholder="Full-Stack Developer" />
        </label>
      </div>

      <div className="field">
        <span className="field-label">Portfolio type</span>
        <div className="type-grid">
          {types.map((t) => (
            <button type="button" key={t.id} className={`type-chip ${form.typeId === t.id ? 'active' : ''}`} onClick={() => update('typeId', t.id)}>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <label className="field">
        <span className="field-label">Location (optional)</span>
        <input type="text" value={form.fields.location} onChange={(e) => updateField('location', e.target.value)} placeholder="Rawalpindi, Pakistan" />
      </label>

      <label className="field">
        <span className="field-label">A bit about you (optional \u2014 helps the AI write your bio)</span>
        <input type="text" value={form.fields.bioHint} onChange={(e) => updateField('bioHint', e.target.value)} placeholder="I like building tools and games" />
      </label>

      <div className="field">
        <span className="field-label">Photo / avatar (optional)</span>
        {form.logoDataUri ? (
          <div className="logo-preview">
            <img src={form.logoDataUri} alt="Uploaded avatar preview" />
            <button type="button" onClick={() => update('logoDataUri', null)}>Remove</button>
          </div>
        ) : (
          <label className="file-input">
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleLogoChange} disabled={uploadingLogo} />
            <span>{uploadingLogo ? 'Uploading\u2026' : 'Choose an image\u2026'}</span>
          </label>
        )}
        {uploadError && <p className="error-text small">{uploadError}</p>}
      </div>

      <div className="section-label">Appearance</div>

      <div className="field">
        <span className="field-label">Color palette</span>
        <div className="palette-mode-toggle">
          <button type="button" className={!isCustomColors ? 'active' : ''} onClick={() => update('customColors', null)}>Curated</button>
          <button type="button" className={isCustomColors ? 'active' : ''} onClick={enableCustomColors}>Custom</button>
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
                />
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
                <span>{label}</span>
              </label>
            ))}
          </div>
        )}
      </div>

      <div className="section-label">Skills</div>

      <label className="field">
        <span className="field-label">Comma-separated</span>
        <input type="text" value={form.fields.skills} onChange={(e) => updateField('skills', e.target.value)} placeholder="React, Node.js, Python, Docker" />
      </label>

      <div className="section-label">Projects</div>

      {projects.map((project, i) => (
        <div key={i} className="project-field-card">
          <div className="field-row">
            <label className="field">
              <span className="field-label">Name</span>
              <input type="text" value={project.name} onChange={(e) => updateProject(i, 'name', e.target.value)} placeholder="Project name" />
            </label>
            <label className="field">
              <span className="field-label">Link (optional)</span>
              <input type="text" value={project.url} onChange={(e) => updateProject(i, 'url', e.target.value)} placeholder="https://..." />
            </label>
          </div>
          <label className="field">
            <span className="field-label">Description</span>
            <input type="text" value={project.description} onChange={(e) => updateProject(i, 'description', e.target.value)} placeholder="What it does, in one line" />
          </label>
          <button type="button" className="remove-project-btn" onClick={() => removeProject(i)}>Remove project</button>
        </div>
      ))}
      <button type="button" className="add-project-btn" onClick={addProject}>+ Add project</button>

      <div className="section-label">Contact &amp; social</div>

      <div className="field-row">
        <label className="field">
          <span className="field-label">Email</span>
          <input type="email" value={form.fields.email} onChange={(e) => updateField('email', e.target.value)} placeholder="you@example.com" />
        </label>
        <label className="field">
          <span className="field-label">GitHub</span>
          <input type="text" value={form.fields.github} onChange={(e) => updateField('github', e.target.value)} placeholder="https://github.com/you" />
        </label>
      </div>
      <div className="field-row">
        <label className="field">
          <span className="field-label">LinkedIn</span>
          <input type="text" value={form.fields.linkedin} onChange={(e) => updateField('linkedin', e.target.value)} placeholder="https://linkedin.com/in/you" />
        </label>
        <label className="field">
          <span className="field-label">Website</span>
          <input type="text" value={form.fields.website} onChange={(e) => updateField('website', e.target.value)} placeholder="https://..." />
        </label>
      </div>

      <div className="section-label">Voice</div>

      <label className="field">
        <span className="field-label">Tone</span>
        <select value={form.fields.tone} onChange={(e) => updateField('tone', e.target.value)}>
          <option value="professional">Professional</option>
          <option value="friendly">Friendly</option>
          <option value="premium">Premium</option>
        </select>
      </label>

      <button type="submit" className="generate-btn" disabled={loading}>
        {loading ? 'Generating\u2026' : 'Generate site'}
      </button>
    </form>
  )
}
