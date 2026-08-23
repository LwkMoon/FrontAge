"""Quick sanity check: renders every type across all three site kinds,
verifies AI-provider auto-detection, and checks the SQLite draft round-trip.
Works even without any API key set (falls back to placeholder copy), so
it's a fast way to confirm your setup works.

Run with: python selftest.py
"""
import os

from app import _build_site
from db import delete_draft, get_draft
from services import ai_provider
from services.images import generate_monogram_favicon
from site_kinds import SITE_KINDS

SAMPLE_FIELDS = {
    "business": {
        "businessName": "Test Cafe", "phone": "03001234567", "city": "Rawalpindi",
        "address": "123 Mall Road", "hours": "Mon-Sat 10am-8pm",
        "tone": "friendly", "languageStyle": "english",
    },
    "portfolio": {
        "name": "Jane Dev", "role": "Full-Stack Developer", "location": "Rawalpindi",
        "bioHint": "loves building open source tools", "skills": "React, Python, Docker",
        "projects": [{"name": "Project Alpha", "description": "A tool that does things.", "url": "https://example.com"}],
        "github": "https://github.com/janedev", "email": "jane@example.com", "tone": "professional",
    },
    "dashboard": {
        "productName": "MetricFlow", "descriptionHint": "analytics for small SaaS teams",
        "navItems": "Overview, Analytics, Settings", "statLabels": "MRR, Active Users, Churn Rate",
        "tone": "professional",
    },
}

PALETTE_BY_KIND = {"business": "brass-gold", "portfolio": "ocean-teal", "dashboard": "slate-amber"}

created_ids = []

for kind_id, kind in SITE_KINDS.items():
    for type_id in kind["types"]:
        payload = {
            "siteKind": kind_id,
            "typeId": type_id,
            "paletteId": PALETTE_BY_KIND[kind_id],
            "fields": SAMPLE_FIELDS[kind_id],
        }
        result = _build_site(payload)
        assert "<html" in result["html"], f"{kind_id}/{type_id}: missing <html>"
        assert 'name="description"' in result["html"], f"{kind_id}/{type_id}: missing meta description"

        draft_id = result["draftId"]
        assert draft_id, f"{kind_id}/{type_id}: expected a draftId"
        stored = get_draft(draft_id)
        assert stored is not None and stored["site_kind"] == kind_id
        created_ids.append(draft_id)

        # Regenerating with the same draftId should update in place, not duplicate.
        result2 = _build_site({**payload, "draftId": draft_id})
        assert result2["draftId"] == draft_id, f"{kind_id}/{type_id}: regenerate created a new draft"

        print(f"OK  {kind_id:10s} {type_id:16s} ai_generated={str(result['aiGenerated']):<5} draft_id={draft_id}")

# Kind-specific content checks
business_payload = {"siteKind": "business", "typeId": "restaurant", "paletteId": "brass-gold", "fields": SAMPLE_FIELDS["business"]}
b = _build_site(business_payload)
assert "123 Mall Road" in b["html"] and "Mon-Sat 10am-8pm" in b["html"]
delete_draft(b["draftId"])

portfolio_payload = {"siteKind": "portfolio", "typeId": "developer", "paletteId": "ocean-teal", "fields": SAMPLE_FIELDS["portfolio"]}
p = _build_site(portfolio_payload)
assert "Project Alpha" in p["html"] and "React" in p["html"]
delete_draft(p["draftId"])

dashboard_payload = {"siteKind": "dashboard", "typeId": "saas-analytics", "paletteId": "slate-amber", "fields": SAMPLE_FIELDS["dashboard"]}
d = _build_site(dashboard_payload)
assert "MRR" in d["html"] and "SAMPLE DATA" in d["html"]
delete_draft(d["draftId"])

print("OK  kind-specific content checks (business/portfolio/dashboard)")

# Provider auto-detection priority: anthropic > openai > gemini
_original_env = {k: os.environ.get(k) for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "AI_PROVIDER")}
try:
    for k in _original_env:
        os.environ.pop(k, None)
    assert ai_provider.active_provider() is None

    os.environ["GEMINI_API_KEY"] = "test"
    assert ai_provider.active_provider() == "gemini"

    os.environ["OPENAI_API_KEY"] = "test"
    assert ai_provider.active_provider() == "openai"

    os.environ["ANTHROPIC_API_KEY"] = "test"
    assert ai_provider.active_provider() == "anthropic"

    os.environ["AI_PROVIDER"] = "gemini"
    assert ai_provider.active_provider() == "gemini"

    os.environ["AI_PROVIDER"] = "openai"
    assert ai_provider.active_provider() == "openai"
    print("OK  AI provider auto-detection and override priority")
finally:
    for k, v in _original_env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v

favicon = generate_monogram_favicon("Al-Madina Foods", "#c9a25b", "#12100e")
assert favicon.startswith("data:image/svg+xml;base64,")
print("OK  favicon generation")

for draft_id in created_ids:
    delete_draft(draft_id)
assert get_draft(created_ids[0]) is None
print(f"OK  cleaned up {len(created_ids)} test drafts")

total_types = sum(len(k["types"]) for k in SITE_KINDS.values())
print(f"\nAll {total_types} types across {len(SITE_KINDS)} site kinds rendered and persisted successfully.")
