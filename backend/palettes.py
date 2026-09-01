"""Curated color palettes for generated sites.

Each palette exposes CSS custom properties consumed by base.css.jinja.
Add a new palette here and it shows up automatically as a swatch in the UI.
"""

PALETTES = {
    "brass-gold": {
        "name": "Brass & Gold",
        "description": "Deep charcoal with warm brass accents - premium and upscale.",
        "vars": {
            "--color-bg": "#12100e",
            "--color-surface": "#1c1916",
            "--color-primary": "#c9a25b",
            "--color-text": "#f4efe8",
            "--color-text-muted": "#b8ac9c",
            "--color-border": "#332e28",
        },
    },
    "ocean-teal": {
        "name": "Ocean Teal",
        "description": "Deep navy with a bright teal accent - trustworthy and modern.",
        "vars": {
            "--color-bg": "#0b1622",
            "--color-surface": "#122436",
            "--color-primary": "#2dd4bf",
            "--color-text": "#eef6f5",
            "--color-text-muted": "#9db4c2",
            "--color-border": "#1e3548",
        },
    },
    "sage-cream": {
        "name": "Sage & Cream",
        "description": "Soft sage green on warm cream - calm and approachable.",
        "vars": {
            "--color-bg": "#faf7f0",
            "--color-surface": "#ffffff",
            "--color-primary": "#5c7a5e",
            "--color-text": "#2b2e2a",
            "--color-text-muted": "#6b7268",
            "--color-border": "#e4ddcc",
        },
    },
    "rose-charcoal": {
        "name": "Rose & Charcoal",
        "description": "Muted rose against charcoal - soft but confident.",
        "vars": {
            "--color-bg": "#1a1418",
            "--color-surface": "#241c22",
            "--color-primary": "#d98a97",
            "--color-text": "#f6eef0",
            "--color-text-muted": "#b8a4ab",
            "--color-border": "#38292f",
        },
    },
    "classic-blue": {
        "name": "Classic Blue",
        "description": "Navy and white - safe, professional, works for any local business.",
        "vars": {
            "--color-bg": "#ffffff",
            "--color-surface": "#f4f6f9",
            "--color-primary": "#1e3a5f",
            "--color-text": "#1a1f26",
            "--color-text-muted": "#5a6472",
            "--color-border": "#dde3ea",
        },
    },
    "deep-emerald": {
        "name": "Deep Emerald",
        "description": "Forest green with a warm gold accent - grounded and trustworthy.",
        "vars": {
            "--color-bg": "#0f1f18",
            "--color-surface": "#17291f",
            "--color-primary": "#d4b06a",
            "--color-text": "#eef5ef",
            "--color-text-muted": "#9db3a5",
            "--color-border": "#24392d",
        },
    },
    "slate-amber": {
        "name": "Slate & Amber",
        "description": "Cool graphite with an amber accent - sturdy and no-nonsense.",
        "vars": {
            "--color-bg": "#1a1d24",
            "--color-surface": "#23272f",
            "--color-primary": "#d9a441",
            "--color-text": "#f0f1f3",
            "--color-text-muted": "#9599a3",
            "--color-border": "#2e323c",
        },
    },
    "plum-blush": {
        "name": "Plum & Blush",
        "description": "Deep plum with a soft blush accent - warm and a little glamorous.",
        "vars": {
            "--color-bg": "#1f1420",
            "--color-surface": "#2a1c2c",
            "--color-primary": "#e0a9b5",
            "--color-text": "#f6eef2",
            "--color-text-muted": "#b39aa8",
            "--color-border": "#3a2838",
        },
    },
}

_CUSTOM_KEYS = {
    "primary": "--color-primary",
    "background": "--color-bg",
    "surface": "--color-surface",
    "text": "--color-text",
    "textMuted": "--color-text-muted",
    "border": "--color-border",
}


def resolve_palette(palette_id, custom=None):
    """Return a CSS-vars dict for the given palette id, with optional custom overrides.

    `custom`, if provided, is a dict with any of: primary, background, surface,
    text, textMuted, border (hex strings). Unset keys fall back to the base
    palette (or classic-blue if no palette_id is given either).
    """
    base = PALETTES.get(palette_id or "classic-blue", PALETTES["classic-blue"])
    result = base["vars"].copy()
    if custom:
        for key, css_var in _CUSTOM_KEYS.items():
            if custom.get(key):
                result[css_var] = custom[key]
    return result
