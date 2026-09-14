"""Parse masslandrecords.com (20/20 Perfect Vision) HTML into structured records.

Pure functions, no network/browser code. Operates on HTML captured from a real,
human-driven browser session (see capture.user.js) rather than fetching pages
itself — the site's Incapsula protection blocks scripted access outright, so
this module never talks to the site directly.

DOM contract this relies on (verified against a live Suffolk County Name
Search results page):
  - Result rows: <tr class="DataGridRow|DataGridAlternatingRow|DataGridSelectedRow">
    with 11 <td> cells in this fixed order for the standard search grid:
    select, type, name, book, page, type_desc, file_date, street_number,
    property_descr, view_img (button), add_to_basket (button).
  - A Book/Page Search grid (as opposed to Name Search) renders a narrower,
    7-cell row instead: select, file_date, book_page (combined "book/page"
    text), type_desc, town, view_img (button), add_to_basket (button).
    Confirmed from a captured Middlesex South Book/Page search where the
    11-column contract silently dropped every row via the `len(cells) <
    len(SEARCH_COLUMNS)` guard (see debug_captures/Middlesexsouth-20260914-143236.html).
  - Document detail / grantor-grantee panels: <table class="DataGridView">,
    first row is a header row, second+ rows are data — the first such table
    on the page is the document summary, any further ones are party grids.
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup
from bs4.element import Tag

ROW_SELECTOR = "tr.DataGridRow, tr.DataGridAlternatingRow, tr.DataGridSelectedRow"

SEARCH_COLUMNS = [
    "select",
    "type",
    "name",
    "book",
    "page",
    "type_desc",
    "file_date",
    "street_number",
    "property_descr",
    "view_img",
    "add_to_basket",
]

# Book/Page Search grids render a single combined "Book/Page" cell (e.g.
# "85256/295") in place of the separate type/name/book/page/street/property
# columns the Name Search grid has.
SEARCH_COLUMNS_BOOK_PAGE = [
    "select",
    "file_date",
    "book_page",
    "type_desc",
    "town",
    "view_img",
    "add_to_basket",
]


def _cell_text(td: Tag) -> str:
    return td.get_text(strip=True)


def _button_control_name(td: Tag) -> str | None:
    inp = td.find("input")
    return inp.get("name") if inp else None


def _slug(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "col"


def parse_search_results(html: str) -> list[dict]:
    """Parse a search-results grid page into a list of record dicts."""
    soup = BeautifulSoup(html, "lxml")
    rows = soup.select(ROW_SELECTOR)
    records = []
    for tr in rows:
        # reason: tr.DataGridRow also matches rows inside the DocDetails1_*
        # document-detail panel (id="DocDetails1_GridView_Details" etc, under
        # ContentContainer "DocDetails1_ContentContainer1") when a detail view
        # is open alongside the results grid — those are handled separately
        # by parse_document_detail and must not be read as search-result rows
        # (an 8-cell DocDetails1_GridView_Details row was being misparsed as
        # a 7-column Book/Page result before this check was added).
        container = tr.find_parent(id=True)
        if container is not None and container.get("id", "").startswith("DocDetails"):
            continue
        cells = tr.find_all("td", recursive=False)
        # reason: cell count alone tells the two known grid shapes apart —
        # match the longer (Name Search) contract first so an 11-cell row
        # never gets misread as the narrower Book/Page contract.
        if len(cells) >= len(SEARCH_COLUMNS):
            columns = SEARCH_COLUMNS
        elif len(cells) >= len(SEARCH_COLUMNS_BOOK_PAGE):
            columns = SEARCH_COLUMNS_BOOK_PAGE
        else:
            continue
        record: dict = {}
        for name, td in zip(columns, cells):
            if name == "select":
                continue
            if name in ("view_img", "add_to_basket"):
                record[f"{name}_control"] = _button_control_name(td)
            elif name == "book_page":
                book, _, page = _cell_text(td).partition("/")
                record["book"] = book.strip()
                record["page"] = page.strip()
            elif name == "town":
                # reason: Book/Page Search grids have no party-name column at
                # all, so "name" would otherwise stay null and every capture
                # would folder/dedupe under "Unknown" — reuse the town as the
                # record's name since it's the only identifying text this grid
                # shape actually offers.
                record["name"] = _cell_text(td)
            else:
                record[name] = _cell_text(td)
        records.append(record)
    return records


def _dedupe(names: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    out = []
    for name in names:
        if name in seen:
            seen[name] += 1
            out.append(f"{name}_{seen[name]}")
        else:
            seen[name] = 0
            out.append(name)
    return out


def _parse_kv_grid(table: Tag) -> list[dict]:
    rows = table.find_all("tr")
    if not rows:
        return []
    header_cells = rows[0].find_all(["th", "td"], recursive=False)
    # Header cells are often blank (e.g. the grantor/grantee grid has no
    # visible column labels) — dedupe so blank/duplicate headers don't
    # collapse distinct columns into a single overwritten dict key.
    headers = _dedupe([_slug(h.get_text(strip=True)) for h in header_cells])
    out = []
    for tr in rows[1:]:
        cells = tr.find_all("td", recursive=False)
        if not cells:
            continue
        out.append({h: _cell_text(c) for h, c in zip(headers, cells)})
    return out


def parse_document_detail(html: str) -> dict | None:
    """Parse the 'View Details' panel: doc summary + grantor/grantee parties."""
    soup = BeautifulSoup(html, "lxml")
    grids = soup.select("table.DataGridView")
    if not grids:
        return None
    summary_rows = _parse_kv_grid(grids[0])
    if not summary_rows:
        return None
    parties: list[dict] = []
    for grid in grids[1:]:
        parties.extend(_parse_kv_grid(grid))
    return {"summary": summary_rows[0], "parties": parties}


def parse_capture(html: str, source_query: str | None = None) -> dict:
    """Parse a full captured page: whatever combination of results/detail it has."""
    return {
        "source_query": source_query,
        "results": parse_search_results(html),
        "detail": parse_document_detail(html),
    }
