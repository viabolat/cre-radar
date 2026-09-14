"""SQLite persistence for captured masslandrecords.com records.

Kept deliberately tiny (stdlib sqlite3, no ORM) — this is a single-user local
tool, not a multi-tenant backend.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent / "records.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district TEXT,
    type TEXT,
    name TEXT,
    book TEXT,
    page TEXT,
    type_desc TEXT,
    file_date TEXT,
    street_number TEXT,
    property_descr TEXT,
    doc_no TEXT,
    rec_time TEXT,
    num_pages TEXT,
    consideration TEXT,
    doc_status TEXT,
    source_query TEXT,
    captured_at TEXT DEFAULT (datetime('now')),
    UNIQUE (district, book, page, type, name)
);

CREATE TABLE IF NOT EXISTS parties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER NOT NULL REFERENCES records(id) ON DELETE CASCADE,
    name TEXT,
    role TEXT
);

CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER REFERENCES records(id) ON DELETE SET NULL,
    page_num INTEGER,
    total_pages INTEGER,
    viewer_url TEXT,
    opener_title TEXT,
    file_path TEXT NOT NULL,
    captured_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_records_name ON records(name);
CREATE INDEX IF NOT EXISTS idx_records_book_page ON records(book, page);
CREATE INDEX IF NOT EXISTS idx_records_district_book_page ON records(district, book, page);
CREATE INDEX IF NOT EXISTS idx_images_record ON images(record_id);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def upsert_result_row(
    conn: sqlite3.Connection, row: dict, source_query: str | None, district: str
) -> tuple[int, bool]:
    """Insert or update a search-result row. Returns (record_id, was_inserted)."""
    existing = conn.execute(
        "SELECT id FROM records WHERE district IS ? AND book IS ? AND page IS ? AND type IS ? AND name IS ?",
        (district, row.get("book"), row.get("page"), row.get("type"), row.get("name")),
    ).fetchone()
    if existing:
        conn.execute(
            """UPDATE records SET type_desc=?, file_date=?, street_number=?,
               property_descr=?, source_query=COALESCE(?, source_query)
               WHERE id=?""",
            (
                row.get("type_desc"),
                row.get("file_date"),
                row.get("street_number"),
                row.get("property_descr"),
                source_query,
                existing["id"],
            ),
        )
        return existing["id"], False

    cur = conn.execute(
        """INSERT INTO records (district, type, name, book, page, type_desc, file_date,
           street_number, property_descr, source_query)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            district,
            row.get("type"),
            row.get("name"),
            row.get("book"),
            row.get("page"),
            row.get("type_desc"),
            row.get("file_date"),
            row.get("street_number"),
            row.get("property_descr"),
            source_query,
        ),
    )
    return cur.lastrowid, True


def attach_detail(conn: sqlite3.Connection, record_id: int, detail: dict) -> None:
    summary = detail.get("summary") or {}
    conn.execute(
        """UPDATE records SET doc_no=?, rec_time=?, num_pages=?,
           consideration=?, doc_status=? WHERE id=?""",
        (
            summary.get("doc"),
            summary.get("rec_time"),
            summary.get("of_pgs"),
            summary.get("consideration"),
            summary.get("doc_status"),
            record_id,
        ),
    )
    conn.execute("DELETE FROM parties WHERE record_id=?", (record_id,))
    for party in detail.get("parties", []):
        # party dicts have one name-ish key and one role-ish key; grab by position
        values = list(party.values())
        name = values[0] if len(values) > 0 else None
        role = values[1] if len(values) > 1 else None
        conn.execute(
            "INSERT INTO parties (record_id, name, role) VALUES (?, ?, ?)",
            (record_id, name, role),
        )


def find_record_by_book_page(
    conn: sqlite3.Connection, district: str | None, book: str | None, page: str | None
) -> sqlite3.Row | None:
    """Returns the matching record (id, name, ...) or None — caller decides which fields it needs."""
    if not district or not book or not page:
        return None
    return conn.execute(
        "SELECT * FROM records WHERE district=? AND book=? AND page=? ORDER BY captured_at DESC LIMIT 1",
        (district, book, page),
    ).fetchone()


def save_image(
    conn: sqlite3.Connection,
    *,
    file_path: str,
    page_num: int | None,
    total_pages: int | None,
    viewer_url: str | None,
    opener_title: str | None,
    record_id: int | None = None,
) -> int:
    """Store one captured scanned-document page image.

    record_id is resolved by the caller from the book/page the capture script
    read off the opener tab's DataGridSelectedRow — pass None if that lookup
    didn't produce an unambiguous match, and the image is stored unlinked.
    """
    cur = conn.execute(
        """INSERT INTO images (record_id, page_num, total_pages, viewer_url, opener_title, file_path)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (record_id, page_num, total_pages, viewer_url, opener_title, file_path),
    )
    return cur.lastrowid


def list_images(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM images ORDER BY captured_at DESC").fetchall()


def get_image(conn: sqlite3.Connection, image_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM images WHERE id = ?", (image_id,)).fetchone()


def query_records(
    conn: sqlite3.Connection,
    name: str | None = None,
    book: str | None = None,
    page: str | None = None,
    type_: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[sqlite3.Row]:
    clauses = []
    params: list = []
    if name:
        clauses.append("name LIKE ?")
        params.append(f"%{name}%")
    if book:
        clauses.append("book = ?")
        params.append(book)
    if page:
        clauses.append("page = ?")
        params.append(page)
    if type_:
        clauses.append("type = ?")
        params.append(type_)
    if date_from:
        clauses.append("file_date >= ?")
        params.append(date_from)
    if date_to:
        clauses.append("file_date <= ?")
        params.append(date_to)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.extend([limit, offset])
    sql = f"SELECT * FROM records {where} ORDER BY captured_at DESC LIMIT ? OFFSET ?"
    return conn.execute(sql, params).fetchall()


def get_record(conn: sqlite3.Connection, record_id: int) -> dict | None:
    record = conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
    if not record:
        return None
    parties = conn.execute(
        "SELECT name, role FROM parties WHERE record_id = ?", (record_id,)
    ).fetchall()
    return {**dict(record), "parties": [dict(p) for p in parties]}
