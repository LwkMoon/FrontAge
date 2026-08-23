"""Static configuration for each supported portfolio type.

Structurally simpler than business_types.py: portfolios don't have AI-invented
"highlights" (that would mean fabricating project history), so fallback_copy
only needs headline/tagline/about/cta_text. Skills and projects are always
the person's own input, never AI-generated.
"""

PORTFOLIO_TYPES = {
    "developer": {
        "label": "Developer",
        "cta_default": "View my work",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M8 6 3 12l5 6M16 6l5 6-5 6"/></svg>'
        ),
        "fallback_copy": {
            "headline": "I build software that works",
            "tagline": "Full-stack development focused on clean, maintainable code.",
            "about": (
                "I work across the stack, from backend APIs to polished frontend "
                "interfaces. I care about writing code that's easy to read and easy "
                "to change, not just code that works today."
            ),
            "cta_text": "View my work",
        },
    },
    "designer": {
        "label": "Designer / Creative",
        "cta_default": "See my portfolio",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M3 21l3-1 12-12-2-2L4 18z"/><path d="M14 6l4 4"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Design that says something",
            "tagline": "Visual work built around clarity, not decoration.",
            "about": (
                "I design with a simple goal: make the message obvious and the "
                "experience effortless. Every project starts with understanding what "
                "the work actually needs to do before it starts looking like anything."
            ),
            "cta_text": "See my portfolio",
        },
    },
    "freelancer": {
        "label": "Freelancer / Consultant",
        "cta_default": "Work with me",
        "icon_svg": (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<rect x="3" y="8" width="18" height="12" rx="2"/>'
            '<path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>'
        ),
        "fallback_copy": {
            "headline": "Freelance help that fits your project",
            "tagline": "Flexible, focused work without the agency overhead.",
            "about": (
                "I take on a small number of projects at a time so each one gets "
                "real attention. Clear scope, clear timelines, and direct "
                "communication throughout."
            ),
            "cta_text": "Work with me",
        },
    },
}
