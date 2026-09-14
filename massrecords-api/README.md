# Mass Land Records — local capture API

`masslandrecords.com` (Suffolk County Registry of Deeds, and every other MA
registry on the same "20/20 Perfect Vision" platform) has no public API. It's
pure ASP.NET WebForms, and the site is protected by Incapsula, which hard-blocks
scripted/headless browser access outright — not a CAPTCHA, an actual
"incident ID" refusal, and it does so specifically for automation-launched
browsers (CDP flags, `navigator.webdriver`), not for headless-ness or IP
reputation. Standalone Playwright/requests automation against this site was
tested and is a dead end short of deliberately spoofing the automation
fingerprint, which this project does not do — defeating a site's bot defenses
isn't something to route around quietly, regardless of how public the
underlying data is.

Instead, this is a **session-assisted** tool: you browse and search the site
exactly as a human, in your own real Chrome; a userscript running in that tab
reads the page you're already looking at and forwards it to a local API,
which parses it into structured JSON and lets you query it afterwards. No
part of this automates navigation against masslandrecords.com.

The tool is generalized across every district hosted on masslandrecords.com
— the userscripts wildcard-match any district path and tag every captured
record/image with the district read off the page URL, so data from
different districts never collides on shared book/page numbers in the local
database. See **Districts** below for exactly which districts that covers.

## Pieces

- `parser.py` — pure HTML → dict parsing (search-result rows, document detail
  panel, grantor/grantee parties). No network code.
- `store.py` — tiny SQLite persistence layer (stdlib `sqlite3`, no ORM).
- `api.py` — FastAPI app: `POST /ingest` (page HTML + district → parsed
  records), `POST /ingest-image` (scanned document page + district → stored
  image, auto-linked to a record), `GET /records`, `GET /records/{id}`,
  `GET /images`, `GET /images/{id}` (serves the file).
- `capture.user.js` — Tampermonkey userscript, active on any
  `<District>/D/Default.aspx` on masslandrecords.com. Adds a "Send to Local
  API" button.
- `capture-image.user.js` — Tampermonkey userscript, active on any
  `<District>/D/ImageViewerEx.aspx` (the scanned-document popup). Adds
  "Capture This Page" / "Capture All Pages" buttons.
- `query.py` — CLI over `GET /records` for quick lookups.

## Districts

MA registries of deeds all run the same "20/20 Perfect Vision" platform, but
not all of them are hosted at `masslandrecords.com` — these scripts only
fire on that domain, wildcarded across every district path on it.

- **Confirmed on masslandrecords.com** (these scripts work here): Suffolk,
  Middlesex South, Worcester, Dukes
- **Confirmed on a separate domain** (out of scope for these scripts):
  Barnstable, Berkshire North, Berkshire Middle, Berkshire South, Bristol
  North, Bristol Fall River, Essex North, Essex South, Franklin, Hampden,
  Hampshire, Worcester North
- **Unconfirmed** (not yet checked which domain they're on): Middlesex
  North, Norfolk, Plymouth, Nantucket

## Setup (any machine)

```bash
git clone https://github.com/viabolat/massrecords-api.git
cd massrecords-api
./serve.sh
```

`serve.sh` creates the venv and installs `requirements.txt` on first run,
then starts the API on `http://localhost:8787` (safe to re-run — no-ops if
already up). The service is local-only by design; each machine runs its own
copy, and no data or credentials are shared between them.

Install [Tampermonkey](https://www.tampermonkey.net/) in Chrome, then in its
dashboard use **Utilities → Import from file** to load both `capture.user.js`
and `capture-image.user.js` from the cloned repo (avoids copy/paste quote
corruption). Each is scoped via `@match` to only inject on its own page, so
they won't collide.

## Use

1. Go to `https://www.masslandrecords.com/<District>/D/Default.aspx` for
   whichever district you're working in (e.g. `Suffolk`, `MiddlesexSouth`,
   `Worcester`, `Dukes` — see **Districts** above) and search normally (Name
   Search, Document Search, etc.).
2. Click **"Send to Local API"**. This captures whatever's currently
   rendered — the results grid, and a document detail/parties panel if one
   is present on the page — tagged with the district read off the URL.
3. Click a record's **"View Details"** to open the scanned-document popup
   (`ImageViewerEx.aspx`). Click **"Capture This Page"** or **"Capture All
   Pages"** — each page's image is fetched from the same-origin,
   session-cookie-gated image URL and POSTed to `/ingest-image`. The script
   reads `tr.DataGridSelectedRow` off the opener tab to auto-link the image
   to the record you clicked into (book/page match, scoped to the same
   district) — no manual typing.
4. Captured images land in
   `images_captured/<District>/<Party-Name>/<book>-<page>/` (or
   `images_captured/<District>/_unlinked/` if book/page didn't resolve to a
   unique record).
5. Query what you've captured:

```bash
./query.py "Smith"
curl "http://localhost:8787/records/1"
curl "http://localhost:8787/images"
```

## Not in the repo

`records.db` and `images_captured/` are per-machine local data (gitignored)
— captured registry data, not code. A fresh clone starts empty; nothing
syncs between machines automatically.

## Known gaps

- Column mapping in `parser.py` (`SEARCH_COLUMNS`) reflects the standard
  Recorded Land Name Search grid. Other search types (Book Search, Property
  Search, Plans, …) may render a different column set — verify against a
  captured page before trusting the field mapping if you use those.
- `SEARCH_COLUMNS` was only verified against a live Suffolk County page.
  Other masslandrecords.com districts (Middlesex South, Worcester, Dukes)
  are assumed to render the same grid layout but haven't individually been
  spot-checked — verify against a captured page from each before trusting
  the field mapping there too.
- Detail-panel attachment is heuristic (attaches to the just-ingested row, or
  matches by book/page if only a detail panel was captured with no grid
  rows) — good enough for the click-through-then-capture workflow above, not
  a guaranteed-correct join for out-of-order capture.
- The `parties` table has not yet been observed to populate in practice —
  still confirming whether "View Details" actually renders an inline
  grantor/grantee panel on `Default.aspx` for `parse_document_detail()` to
  find.
