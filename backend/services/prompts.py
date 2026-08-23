"""Prompt construction for each site kind.

Kept separate from services/ai_provider.py on purpose: that module only
knows how to talk to a provider and parse JSON back. This module knows what
to ask for.
"""

TONE_GUIDANCE = {
    "professional": "confident and professional, no slang",
    "friendly": "warm and conversational, like a helpful neighbour",
    "premium": "polished and a little upscale, understated confidence",
}

LANGUAGE_GUIDANCE = {
    "english": "Write in clear, simple English.",
    "roman-urdu-mix": (
        "Write mostly in English but naturally sprinkle in a few common Roman Urdu "
        "words or phrases the way local businesses in Pakistan actually talk to "
        "customers. Keep it tasteful and not forced, and keep the headline itself "
        "in English."
    ),
}


def _tone(tone):
    return TONE_GUIDANCE.get(tone, TONE_GUIDANCE["professional"])


def _language(language_style):
    return LANGUAGE_GUIDANCE.get(language_style, LANGUAGE_GUIDANCE["english"])


def build_business_prompt(business_name, type_label, highlight_label, highlight_count,
                           tone, language_style, city=None):
    location_note = f" The business is located in {city}." if city else ""

    return f"""You are writing website copy for a small local business.

Business name: {business_name}
Business type: {type_label}
Tone: {_tone(tone)}
{_language(language_style)}{location_note}

Return ONLY a JSON object (no markdown fences, no preamble, no explanation) with this exact shape:
{{
  "headline": "short punchy hero headline, under 8 words",
  "tagline": "one supporting sentence, under 15 words",
  "about": "2-3 sentence about paragraph, warm and specific to this business type",
  "cta_text": "2-4 word call to action button label, e.g. 'Order on WhatsApp'",
  "highlights": [
    {{"title": "short title, 2-4 words", "description": "one sentence, under 18 words"}}
  ]
}}

The "highlights" array must contain exactly {highlight_count} items, written for a
section titled "{highlight_label}".

Do not invent specific prices, addresses, or phone numbers. Keep everything
generic enough that the business owner can lightly edit it before publishing."""


def build_portfolio_prompt(name, role, type_label, tone, bio_hint=None):
    hint_note = f" Here's what they told us about themselves: {bio_hint}" if bio_hint else ""

    return f"""You are writing personal-brand website copy for a portfolio site.

Name: {name}
Role: {role}
Portfolio type: {type_label}
Tone: {_tone(tone)}
Write in clear, simple English.{hint_note}

Return ONLY a JSON object (no markdown fences, no preamble, no explanation) with this exact shape:
{{
  "headline": "short punchy hero headline about what they do, under 9 words",
  "tagline": "one supporting sentence, under 16 words",
  "about": "2-3 sentence first-person-friendly about paragraph",
  "cta_text": "2-4 word call to action button label, e.g. 'Get in touch'"
}}

Do not invent specific project names, employers, numbers, or achievements you
weren't given. Keep it grounded and editable, not a fabricated resume."""


def build_dashboard_prompt(product_name, type_label, tone, description_hint=None):
    hint_note = f" Context on what it does: {description_hint}" if description_hint else ""

    return f"""You are writing the welcome copy for the home screen of a product dashboard.

Product name: {product_name}
Dashboard type: {type_label}
Tone: {_tone(tone)}
Write in clear, simple English.{hint_note}

Return ONLY a JSON object (no markdown fences, no preamble, no explanation) with this exact shape:
{{
  "headline": "short tagline for the product, under 8 words",
  "tagline": "one supporting sentence, under 16 words",
  "welcome_message": "one short, friendly welcome line shown at the top of the dashboard, under 14 words",
  "cta_text": "2-3 word demo action button label, e.g. 'View Report'"
}}

This is a UI mockup, not real marketing copy for launch, so keep it clean and
generic rather than hyping up specific features you weren't told about."""
