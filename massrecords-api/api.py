"""Local REST API over masslandrecords.com data captured from a real browser session.

Run with: .venv/bin/uvicorn api:app --port 8787 --reload

This service never talks to masslandrecords.com itself. It only accepts HTML
that capture.user.js POSTs from the user's own, human-driven browser tab
(Incapsula sees a normal browser doing a normal search — nothing here
automates or scripts that navigation), parses it with parser.py, and stores
the structured result so it can be queried over a normal REST API afterwards.
"""

from __future__ import annotations

import base64
import re
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import parser as mlr_parser
import store

app = FastAPI(title="Mass Land Records — local capture API")

IMAGES_DIR = Path(__file__).parent / "images_captured"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://www.masslandrecords.com"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
    # Chrome blocks/hangs a public https:// page's fetch() to http://localhost
    # unless the server answers the Private Network Access preflight with
    # Access-Control-Allow-Private-Network: true — confirmed empirically that
    # capture.user.js's fetch() never resolves without this.
    allow_private_network=True,
)


@app.on_event("startup")
def _startup() -> None:
    store.init_db()


class IngestRequest(BaseModel):
    html: str
    source_query: str | None = None
    district: str
    source_url: str | None = None


class IngestResponse(BaseModel):
    parsed_rows: int
    inserted: int
    updated: int
    detail_attached: bool


DEBUG_CAPTURES_DIR = Path(__file__).parent / "debug_captures"


@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest) -> IngestResponse:
    parsed = mlr_parser.parse_capture(req.html, req.source_query)
    rows = parsed["results"]
    detail = parsed["detail"]

    # The grid's column shape differs across search types/districts and the
    # parser's DOM contract is reverse-engineered from one example — when it
    # parses zero rows on a page that clearly has some, save the raw HTML so
    # the parser can be fixed from real data instead of guessing blind.
    if not rows:
        DEBUG_CAPTURES_DIR.mkdir(exist_ok=True)
        stamp = __import__("datetime").datetime.now().strftime("%Y%m%d-%H%M%S")
        dump_path = DEBUG_CAPTURES_DIR / f"{_slug(req.district)}-{stamp}.html"
        dump_path.write_text(req.html, encoding="utf-8")

    inserted = 0
    updated = 0
    detail_attached = False

    with store.get_conn() as conn:
        record_ids: list[int] = []
        for row in rows:
            record_id, was_inserted = store.upsert_result_row(conn, row, req.source_query, req.district)
            record_ids.append(record_id)
            if was_inserted:
                inserted += 1
            else:
                updated += 1

        # A detail-panel capture (no grid rows, one doc open) attaches to the
        # single most recently touched record for that book/page instead.
        if detail and detail.get("summary"):
            book_page = detail["summary"].get("book_page", "")
            book, _, page = book_page.partition("/")
            target_id = None
            if record_ids:
                target_id = record_ids[0]
            elif book and page:
                match = conn.execute(
                    "SELECT id FROM records WHERE district=? AND book=? AND page=? ORDER BY captured_at DESC LIMIT 1",
                    (req.district, book, page),
                ).fetchone()
                target_id = match["id"] if match else None
            if target_id is not None:
                store.attach_detail(conn, target_id, detail)
                detail_attached = True

    return IngestResponse(
        parsed_rows=len(rows),
        inserted=inserted,
        updated=updated,
        detail_attached=detail_attached,
    )


class ImageIngestRequest(BaseModel):
    image_base64: str
    content_type: str = "image/png"
    page_num: int | None = None
    total_pages: int | None = None
    viewer_url: str | None = None
    opener_title: str | None = None
    book: str | None = None
    page: str | None = None
    district: str


class ImageIngestResponse(BaseModel):
    image_id: int
    file_path: str
    record_id: int | None = None


_EXT_BY_CONTENT_TYPE = {"png": "png", "jpeg": "jpg", "jpg": "jpg", "gif": "gif", "tiff": "tif"}
_UNSAFE_PATH_CHARS = re.compile(r"[^A-Za-z0-9-]+")
_ACRONYMS = {"LLC", "INC", "LP", "LLP", "CORP", "CO", "PC", "LTD"}


def _slug(text: str) -> str:
    words = [w.capitalize() if w.upper() not in _ACRONYMS else w.upper() for w in text.split()]
    slug = _UNSAFE_PATH_CHARS.sub("-", "-".join(words))
    return slug.strip("-") or "unknown"


def _image_file_path(req: "ImageIngestRequest", ext: str, record: "sqlite3.Row | None") -> Path:
    """Group captures by <district>/<name>/<book>-<page> so the folder itself
    shows what belongs together.

    Foldering only needs book/page, which the capture script reads straight off
    the opener's selected search-result row on every capture — it does not
    require "Send to Local API" to have been clicked first (that only gets you
    a `record` match, which additionally supplies the party name). So: prefer
    the matched record's book/page/name when there is one, fall back to the
    raw book/page the browser sent when there isn't, and only land in the
    <district>/_unlinked bucket when neither is available (e.g. no unique
    selected row on the opener at all)."""
    short_id = uuid4().hex[:8]
    page_tag = f"p{req.page_num or 0}_of_{req.total_pages or '?'}"
    district_folder = Path(_slug(req.district))
    if record is not None:
        book, page, name = record["book"], record["page"], record["name"] or "unknown"
    else:
        book, page, name = req.book, req.page, "unknown"
    if book and page:
        book_page = _UNSAFE_PATH_CHARS.sub("-", f"{book}-{page}").strip("-")
        folder = district_folder / _slug(name) / book_page
    else:
        folder = district_folder / "_unlinked"
    directory = IMAGES_DIR / folder
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{page_tag}_{short_id}.{ext}"


@app.post("/ingest-image", response_model=ImageIngestResponse)
def ingest_image(req: ImageIngestRequest) -> ImageIngestResponse:
    IMAGES_DIR.mkdir(exist_ok=True)
    ext = next((v for k, v in _EXT_BY_CONTENT_TYPE.items() if k in req.content_type), "bin")

    with store.get_conn() as conn:
        record = store.find_record_by_book_page(conn, req.district, req.book, req.page)
        file_path = _image_file_path(req, ext, record)
        try:
            file_path.write_bytes(base64.b64decode(req.image_base64))
        except (base64.binascii.Error, ValueError) as exc:
            raise HTTPException(status_code=400, detail=f"Invalid image_base64: {exc}") from exc

        record_id = record["id"] if record is not None else None
        image_id = store.save_image(
            conn,
            file_path=str(file_path),
            page_num=req.page_num,
            total_pages=req.total_pages,
            viewer_url=req.viewer_url,
            opener_title=req.opener_title,
            record_id=record_id,
        )

    return ImageIngestResponse(image_id=image_id, file_path=str(file_path), record_id=record_id)


@app.get("/images")
def list_images():
    with store.get_conn() as conn:
        return [dict(r) for r in store.list_images(conn)]


@app.get("/images/{image_id}")
def get_image_file(image_id: int):
    with store.get_conn() as conn:
        row = store.get_image(conn, image_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(row["file_path"])


@app.get("/records")
def list_records(
    name: str | None = None,
    book: str | None = None,
    page: str | None = None,
    type: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 100,
    offset: int = 0,
):
    with store.get_conn() as conn:
        rows = store.query_records(
            conn,
            name=name,
            book=book,
            page=page,
            type_=type,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )
        return [dict(r) for r in rows]


@app.get("/records/{record_id}")
def get_record(record_id: int):
    with store.get_conn() as conn:
        record = store.get_record(conn, record_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Record not found")
        return record


@app.get("/health")
def health():
    return {"status": "ok"}
