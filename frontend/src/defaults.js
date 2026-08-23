export const DEFAULT_FIELDS = {
  business: {
    businessName: '', phone: '', whatsapp: '', city: '', address: '', hours: '',
    tone: 'professional', languageStyle: 'english',
  },
  portfolio: {
    name: '', role: '', location: '', bioHint: '', skills: '', projects: [],
    github: '', linkedin: '', twitter: '', email: '', website: '',
    tone: 'professional',
  },
  dashboard: {
    productName: '', descriptionHint: '', navItems: '', statLabels: '',
    tone: 'professional',
  },
}

export function emptyForm(siteKind, firstTypeId, firstPaletteId) {
  return {
    siteKind,
    typeId: firstTypeId || '',
    paletteId: firstPaletteId || '',
    customColors: null,
    logoDataUri: null,
    fields: { ...DEFAULT_FIELDS[siteKind] },
  }
}
