"""SQLite storage for drafts.

Every generated site is auto-saved here, so past work sticks around between
sessions instead of disappearing when the tab closes.

Business, portfolio, and dashboard drafts have very different input fields,
so those live in a single `fields_json` blob rather than one column per
field. `title`, `site_kind`, `type_id`, and the palette/logo columns are
shared across every kind and used to render the drafts list without needing
to parse the blob.

Raw sqlite3, no ORM, on purpose: this is a single-user local tool, and a
short-lived connection per call is simpler to reason about than pooling.
"""
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drafts.db")


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site_kind TEXT NOT NULL,
                type_id TEXT NOT NULL,
                title TEXT NOT NULL,
                palette_id TEXT,
                custom_colors TEXT,
                logo_data_uri TEXT,
                fields_json TEXT NOT NULL,
                copy_json TEXT NOT NULL,
                ai_generated INTEGER NOT NULL DEFAULT 0,
                ai_provider TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _row_to_dict(row):
    d = dict(row)
    d["custom_colors"] = json.loads(d["custom_colors"]) if d.get("custom_colors") else None
    d["fields"] = json.loads(d["fields_json"]) if d.get("fields_json") else {}
    d["copy"] = json.loads(d["copy_json"]) if d.get("copy_json") else None
    del d["fields_json"]
    del d["copy_json"]
    d["ai_generated"] = bool(d["ai_generated"])
    return d


def create_draft(data):
    now = _now()
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO drafts
               (site_kind, type_id, title, palette_id, custom_colors, logo_data_uri,
                fields_json, copy_json, ai_generated, ai_provider, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (data["site_kind"], data["type_id"], data["title"], data.get("palette_id"),
             json.dumps(data["custom_colors"]) if data.get("custom_colors") else None,
             data.get("logo_data_uri"), json.dumps(data.get("fields", {})),
             json.dumps(data.get("copy")), 1 if data.get("ai_generated") else 0,
             data.get("ai_provider"), now, now),
        )
        return cur.lastrowid


def update_draft(draft_id, data):
    with _connect() as conn:
        cur = conn.execute(
            """UPDATE drafts SET
               site_kind = ?, type_id = ?, title = ?, palette_id = ?, custom_colors = ?,
               logo_data_uri = ?, fields_json = ?, copy_json = ?, ai_generated = ?,
               ai_provider = ?, updated_at = ?
               WHERE id = ?""",
            (data["site_kind"], data["type_id"], data["title"], data.get("palette_id"),
             json.dumps(data["custom_colors"]) if data.get("custom_colors") else None,
             data.get("logo_data_uri"), json.dumps(data.get("fields", {})),
             json.dumps(data.get("copy")), 1 if data.get("ai_generated") else 0,
             data.get("ai_provider"), _now(), draft_id),
        )
        return cur.rowcount > 0


def get_draft(draft_id):
    with _connect() as conn:
        row = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
        return _row_to_dict(row) if row else None


def list_drafts():
    with _connect() as conn:
        rows = conn.execute(
            """SELECT id, site_kind, type_id, title, palette_id, updated_at
               FROM drafts ORDER BY updated_at DESC"""
        ).fetchall()
        return [dict(r) for r in rows]


def delete_draft(draft_id):
    with _connect() as conn:
        cur = conn.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))
        return cur.rowcount > 0
