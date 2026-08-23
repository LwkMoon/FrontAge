"""Frontage backend.

Renders a starter static site (HTML + CSS) for one of three site kinds
(business, portfolio, dashboard) from a type config, a color palette, and
AI-written copy. Every generation is saved to a local SQLite database as a
draft.
"""
import json
import os
import re
import zipfile
from datetime import datetime
from io import BytesIO
from urllib.parse import quote

from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader

import db
from palettes import PALETTES, resolve_palette
from services import ai_provider, demo_data
from services.images import ImageError, generate_monogram_favicon, process_logo_upload
from services.prompts import build_business_prompt, build_dashboard_prompt, build_portfolio_prompt
from site_kinds import SITE_KINDS

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates_data")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024  # generous ceiling for exports carrying an embedded logo
CORS(app, expose_headers=["Content-Disposition"])

db.init_db()

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "site"


def whatsapp_link(number, prefill_text):
    digits = re.sub(r"[^0-9]", "", number or "")
    if not digits:
        return "#"
    # wa.me links need the full country code. Pakistani mobile numbers are
    # usually entered in local format (03XXXXXXXXX), so convert those to
    # international (92XXXXXXXXXX). Numbers already entered with a country
    # code pass through unchanged.
    if digits.startswith("0") and len(digits) == 11:
        digits = "92" + digits[1:]
    return f"https://wa.me/{digits}?text={quote(prefill_text)}"


def _safe_json_ld(data):
    dumped = json.dumps(data)
    # Escape so this stays safe inside a <script> tag regardless of autoescape,
    # matching how Flask's own tojson works.
    return dumped.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def _json_ld_business(business_name, config, phone, address, city, copy):
    data = {
        "@context": "https://schema.org",
        "@type": config["schema_type"],
        "name": business_name,
        "description": copy.get("tagline", ""),
    }
    if phone:
        data["telephone"] = phone
    if address or city:
        addr = {"@type": "PostalAddress"}
        if address:
            addr["streetAddress"] = address
        if city:
            addr["addressLocality"] = city
        data["address"] = addr
    return _safe_json_ld(data)


def _json_ld_person(name, role, socials, copy):
    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": name,
        "description": copy.get("tagline", ""),
    }
    if role:
        data["jobTitle"] = role
    same_as = [v for v in (socials.get("github"), socials.get("linkedin"), socials.get("twitter"), socials.get("website")) if v]
    if same_as:
        data["sameAs"] = same_as
    if socials.get("email"):
        data["email"] = socials["email"]
    return _safe_json_ld(data)


def _json_ld_software(product_name, copy):
    data = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": product_name,
        "description": copy.get("tagline", ""),
        "applicationCategory": "BusinessApplication",
    }
    return _safe_json_ld(data)


def _has_keys(data, keys):
    return isinstance(data, dict) and all(k in data for k in keys)


def _render(html_template_name, css_template_name, css_vars, context):
    html_template = jinja_env.get_template(html_template_name)
    css_template = jinja_env.get_template(css_template_name)
    css_content = css_template.render(vars=css_vars)
    export_html = html_template.render(inline_css=False, css_content=css_content, **context)
    preview_html = html_template.render(inline_css=True, css_content=css_content, **context)
    return export_html, preview_html, css_content


# ---------------------------------------------------------------------------
# Copy generation per kind
# ---------------------------------------------------------------------------

def _prepare_business_copy(fields, config):
    business_name = (fields.get("businessName") or "").strip()
    if not business_name:
        raise ValueError("businessName is required")
    city = (fields.get("city") or "").strip()
    tone = fields.get("tone", "professional")
    language_style = fields.get("languageStyle", "english")

    prompt = build_business_prompt(
        business_name, config["label"], config["highlight_section_label"],
        config["highlight_count"], tone, language_style, city or None,
    )
    data, provider = ai_provider.generate(prompt)
    if data and _has_keys(data, ["headline", "tagline", "about", "cta_text", "highlights"]):
        count = config["highlight_count"]
        highlights = list(data.get("highlights", []))[:count]
        while len(highlights) < count:
            highlights.append({"title": "Quality Service", "description": "We take care of every detail."})
        data["highlights"] = highlights
        return business_name, data, True, provider
    return business_name, config["fallback_copy"], False, None


def _prepare_portfolio_copy(fields, config):
    name = (fields.get("name") or "").strip()
    if not name:
        raise ValueError("name is required")
    role = (fields.get("role") or "").strip()
    tone = fields.get("tone", "professional")
    bio_hint = (fields.get("bioHint") or "").strip() or None

    prompt = build_portfolio_prompt(name, role or config["label"], config["label"], tone, bio_hint)
    data, provider = ai_provider.generate(prompt)
    if data and _has_keys(data, ["headline", "tagline", "about", "cta_text"]):
        return name, data, True, provider
    return name, config["fallback_copy"], False, None


def _prepare_dashboard_copy(fields, config):
    product_name = (fields.get("productName") or "").strip()
    if not product_name:
        raise ValueError("productName is required")
    tone = fields.get("tone", "professional")
    description_hint = (fields.get("descriptionHint") or "").strip() or None

    prompt = build_dashboard_prompt(product_name, config["label"], tone, description_hint)
    data, provider = ai_provider.generate(prompt)
    if data and _has_keys(data, ["headline", "tagline", "welcome_message", "cta_text"]):
        return product_name, data, True, provider
    return product_name, config["fallback_copy"], False, None


# ---------------------------------------------------------------------------
# Rendering per kind
# ---------------------------------------------------------------------------

def _render_business(business_name, config, css_vars, fields, copy, logo_data_uri):
    phone = (fields.get("phone") or "").strip()
    whatsapp = (fields.get("whatsapp") or phone or "").strip()
    city = (fields.get("city") or "").strip()
    address = (fields.get("address") or "").strip()
    hours = (fields.get("hours") or "").strip()

    favicon = logo_data_uri or generate_monogram_favicon(business_name, css_vars["--color-primary"], css_vars["--color-bg"])
    map_query = ", ".join(part for part in (address, city) if part)
    map_embed_url = f"https://www.google.com/maps?q={quote(map_query)}&output=embed" if map_query else None

    context = {
        "business_name": business_name,
        "city": city,
        "address": address,
        "hours": hours,
        "phone": phone,
        "whatsapp_link": whatsapp_link(whatsapp, f"Hi {business_name}, I'd like to know more!"),
        "copy": copy,
        "config": config,
        "year": datetime.now().year,
        "logo_data_uri": logo_data_uri,
        "favicon": favicon,
        "meta_description": (copy.get("tagline") or copy.get("about", ""))[:160],
        "map_embed_url": map_embed_url,
        "json_ld": _json_ld_business(business_name, config, phone, address, city, copy),
    }
    return _render("business.html.jinja", "base.css.jinja", css_vars, context)


def _render_portfolio(name, config, css_vars, fields, copy, logo_data_uri):
    role = (fields.get("role") or "").strip()
    location = (fields.get("location") or "").strip()
    skills = [s.strip() for s in (fields.get("skills") or "").split(",") if s.strip()]
    projects = [
        p for p in (fields.get("projects") or [])
        if isinstance(p, dict) and (p.get("name") or "").strip()
    ]
    socials = {
        "github": (fields.get("github") or "").strip() or None,
        "linkedin": (fields.get("linkedin") or "").strip() or None,
        "twitter": (fields.get("twitter") or "").strip() or None,
        "email": (fields.get("email") or "").strip() or None,
        "website": (fields.get("website") or "").strip() or None,
    }

    favicon = logo_data_uri or generate_monogram_favicon(name, css_vars["--color-primary"], css_vars["--color-bg"])

    context = {
        "name": name,
        "role": role,
        "location": location,
        "copy": copy,
        "config": config,
        "skills": skills,
        "projects": projects,
        "socials": socials,
        "year": datetime.now().year,
        "logo_data_uri": logo_data_uri,
        "favicon": favicon,
        "meta_description": (copy.get("tagline") or copy.get("about", ""))[:160],
        "json_ld": _json_ld_person(name, role, socials, copy),
    }
    return _render("portfolio.html.jinja", "base.css.jinja", css_vars, context)


def _render_dashboard(product_name, type_id, config, css_vars, fields, copy, logo_data_uri):
    nav_items = [s.strip() for s in (fields.get("navItems") or config["default_nav_items"]).split(",") if s.strip()]
    stat_labels = [s.strip() for s in (fields.get("statLabels") or config["default_stat_labels"]).split(",") if s.strip()][:4]

    seed_prefix = f"{type_id}:{product_name}"
    favicon = logo_data_uri or generate_monogram_favicon(product_name, css_vars["--color-primary"], css_vars["--color-bg"])

    context = {
        "product_name": product_name,
        "copy": copy,
        "config": config,
        "nav_items": nav_items,
        "stat_cards": demo_data.stat_cards(stat_labels, seed_prefix),
        "weekly_bars": demo_data.weekly_bars(seed_prefix),
        "activity_rows": demo_data.recent_activity(seed_prefix),
        "year": datetime.now().year,
        "logo_data_uri": logo_data_uri,
        "favicon": favicon,
        "meta_description": (copy.get("tagline") or "")[:160],
        "json_ld": _json_ld_software(product_name, copy),
    }
    return _render("dashboard.html.jinja", "dashboard.css.jinja", css_vars, context)


_RENDERERS = {
    "business": _render_business,
    "portfolio": _render_portfolio,
    "dashboard": _render_dashboard,
}

_COPY_PREPARERS = {
    "business": _prepare_business_copy,
    "portfolio": _prepare_portfolio_copy,
    "dashboard": _prepare_dashboard_copy,
}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/api/meta", methods=["GET"])
def meta_route():
    site_kinds = {}
    for kind_id, kind in SITE_KINDS.items():
        types = [{"id": tid, "label": cfg["label"]} for tid, cfg in kind["types"].items()]
        site_kinds[kind_id] = {"label": kind["label"], "description": kind["description"], "types": types}

    palettes = [
        {"id": pid, "name": p["name"], "description": p["description"], "vars": p["vars"]}
        for pid, p in PALETTES.items()
    ]

    return jsonify({
        "siteKinds": site_kinds,
        "palettes": palettes,
        "activeProvider": ai_provider.active_provider(),
        "providerDisplayNames": ai_provider.PROVIDER_DISPLAY_NAMES,
    })


@app.route("/api/upload-image", methods=["POST"])
def upload_image_route():
    try:
        data_uri = process_logo_upload(request.files.get("file"))
        return jsonify({"dataUri": data_uri})
    except ImageError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Upload failed: {e}"}), 500


def _build_site(payload):
    site_kind = payload.get("siteKind", "business")
    kind = SITE_KINDS.get(site_kind)
    if not kind:
        raise ValueError(f"Unknown site kind: {site_kind}")

    type_id = payload.get("typeId")
    config = kind["types"].get(type_id)
    if not config:
        raise ValueError(f"Unknown type '{type_id}' for site kind '{site_kind}'")

    palette_id = payload.get("paletteId")
    custom_colors = payload.get("customColors")
    css_vars = resolve_palette(palette_id, custom_colors)
    logo_data_uri = payload.get("logoDataUri") or None
    fields = payload.get("fields") or {}

    title, copy, ai_generated, provider = _COPY_PREPARERS[site_kind](fields, config)

    if site_kind == "dashboard":
        export_html, preview_html, css_content = _render_dashboard(title, type_id, config, css_vars, fields, copy, logo_data_uri)
    else:
        export_html, preview_html, css_content = _RENDERERS[site_kind](title, config, css_vars, fields, copy, logo_data_uri)

    draft_data = {
        "site_kind": site_kind,
        "type_id": type_id,
        "title": title,
        "palette_id": palette_id,
        "custom_colors": custom_colors,
        "logo_data_uri": logo_data_uri,
        "fields": fields,
        "copy": copy,
        "ai_generated": ai_generated,
        "ai_provider": provider,
    }
    draft_id = payload.get("draftId")
    if draft_id and db.get_draft(draft_id):
        db.update_draft(draft_id, draft_data)
    else:
        draft_id = db.create_draft(draft_data)

    return {
        "html": export_html,
        "previewHtml": preview_html,
        "css": css_content,
        "copy": copy,
        "aiGenerated": ai_generated,
        "aiProvider": provider,
        "title": title,
        "draftId": draft_id,
    }


@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        result = _build_site(request.get_json(force=True))
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Generation failed: {e}"}), 500


@app.route("/api/drafts", methods=["GET"])
def list_drafts_route():
    return jsonify({"drafts": db.list_drafts()})


@app.route("/api/drafts/<int:draft_id>", methods=["GET"])
def get_draft_route(draft_id):
    data = db.get_draft(draft_id)
    if not data:
        return jsonify({"error": "Draft not found"}), 404

    kind = SITE_KINDS.get(data["site_kind"])
    config = kind["types"].get(data["type_id"]) if kind else None
    if not config:
        return jsonify({"error": "This draft's type no longer exists"}), 400

    css_vars = resolve_palette(data["palette_id"], data["custom_colors"])
    fields = data["fields"]
    copy = data["copy"]

    if data["site_kind"] == "dashboard":
        export_html, preview_html, css_content = _render_dashboard(
            data["title"], data["type_id"], config, css_vars, fields, copy, data["logo_data_uri"]
        )
    else:
        export_html, preview_html, css_content = _RENDERERS[data["site_kind"]](
            data["title"], config, css_vars, fields, copy, data["logo_data_uri"]
        )

    return jsonify({
        "html": export_html,
        "previewHtml": preview_html,
        "css": css_content,
        "copy": copy,
        "aiGenerated": data["ai_generated"],
        "aiProvider": data["ai_provider"],
        "title": data["title"],
        "draftId": data["id"],
        "form": {
            "siteKind": data["site_kind"],
            "typeId": data["type_id"],
            "paletteId": data["palette_id"],
            "customColors": data["custom_colors"],
            "logoDataUri": data["logo_data_uri"],
            "fields": fields,
        },
    })


@app.route("/api/drafts/<int:draft_id>", methods=["DELETE"])
def delete_draft_route(draft_id):
    if not db.delete_draft(draft_id):
        return jsonify({"error": "Draft not found"}), 404
    return jsonify({"ok": True})


@app.route("/api/export", methods=["POST"])
def export():
    payload = request.get_json(force=True)
    html = payload.get("html")
    css = payload.get("css")
    title = payload.get("title", "site")

    if not html or not css:
        return jsonify({"error": "html and css are required"}), 400

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("index.html", html)
        zf.writestr("style.css", css)
        zf.writestr("README.txt", (
            f"Site export: {title}\n"
            "Generated with Frontage (https://github.com/LwkMoon/frontage).\n\n"
            "To use:\n"
            "1. Open index.html in a browser to preview.\n"
            "2. Edit the text directly in index.html if anything needs tweaking.\n"
            "3. Upload both files to any static host (Vercel, Netlify, GitHub Pages)\n"
            "   or hand off as a starting point for a fuller build.\n\n"
            "The logo/favicon (if any) is already baked into index.html as a data\n"
            "URI. No extra asset files needed.\n"
        ))
    buffer.seek(0)

    filename = f"{slugify(title)}-site.zip"
    return send_file(buffer, mimetype="application/zip", as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
