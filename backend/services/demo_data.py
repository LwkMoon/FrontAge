"""Deterministic sample data for dashboard exports.

Numbers are seeded from the stat label text so the same draft shows the
same numbers on every regenerate instead of jumping around. This is demo
data for a UI mockup, never presented as real: the exported dashboard
carries a visible "Sample data" label pointing that out.
"""
import random

ACTIVITY_TEMPLATES = [
    "New signup",
    "Order #{n} completed",
    "Payment received",
    "New comment posted",
    "Support ticket closed",
    "Profile updated",
    "Subscription renewed",
    "File uploaded",
]

TIME_LABELS = ["Just now", "5 min ago", "22 min ago", "1 hour ago", "3 hours ago", "Yesterday"]

_RATE_HINTS = ("rate", "%", "churn", "conversion", "uptime")
_CURRENCY_HINTS = ("mrr", "revenue", "sales", "value", "arpu")


def _rng_for(seed_text):
    return random.Random(seed_text)


def stat_cards(labels, seed_prefix):
    """labels: list of up to 4 strings. Returns dicts with label, a
    formatted sample value, and a pre-formatted trend direction/percent
    (kept as plain strings so the template needs no numeric filters)."""
    cards = []
    for label in labels:
        rng = _rng_for(f"{seed_prefix}:{label}")
        lower = label.lower()
        if any(hint in lower for hint in _RATE_HINTS):
            value = f"{rng.uniform(1.5, 98.5):.1f}%"
        elif any(hint in lower for hint in _CURRENCY_HINTS):
            value = f"${rng.randint(2, 480)}K"
        else:
            value = f"{rng.randint(120, 48000):,}"
        cards.append({
            "label": label,
            "value": value,
            "trend_direction": "up" if rng.random() > 0.3 else "down",
            "trend_display": f"{rng.randint(1, 32)}%",
        })
    return cards


def weekly_bars(seed_prefix):
    rng = _rng_for(f"{seed_prefix}:weekly")
    return [rng.randint(25, 100) for _ in range(7)]


def recent_activity(seed_prefix, count=5):
    rng = _rng_for(f"{seed_prefix}:activity")
    rows = []
    for i in range(count):
        template = rng.choice(ACTIVITY_TEMPLATES)
        label = template.format(n=rng.randint(1000, 9999)) if "{n}" in template else template
        rows.append({"label": label, "time": TIME_LABELS[min(i, len(TIME_LABELS) - 1)]})
    return rows
