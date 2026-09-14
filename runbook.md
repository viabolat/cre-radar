# Harvest Runbook — Route 128 / Waltham node

Goal: 10 leads at `index-ready` in `data/leads.csv`, each with ≥1 backed signal and a resolved
owner. Work one lead fully before starting the next. Save every screenshot / PDF to
`data/evidence/<lead_id>/`.

**Saving a Claude-in-Chrome screenshot to `data/evidence/<lead_id>/`**: the `computer` tool's
screenshot/zoom actions return an inline image by default. Pass `save_to_disk: true` on that
call to get a real file path (under a system temp dir); then copy it into
`data/evidence/<lead_id>/parcel.jpg` (Chrome saves as `.jpg`, not `.png`) with a shell `cp`.
Confirmed working 2026-09-12 for `BOS-SEA-001`/`002`/`003`.

Claude in Chrome drives navigation, reads PDFs, and extracts fields. The human handles:
CAPTCHAs and logins, the imagery judgment call on which roofs are industrial/flex, and a final
check of every value before it is written to a CSV.

---

## Tools

| Purpose | URL | Notes |
|---|---|---|
| Statewide parcels + imagery | https://maps.massgis.digital.mass.gov/MassMapper/MassMapper.html | Layer: **Property Tax Parcels**. Switch basemap to aerial. |
| Waltham parcel viewer (parcel + assessing + often permit history in one place) | https://walthamma.mapgeo.io/datasets/properties | Fastest per-parcel lookup for Waltham specifically. |
| Waltham assessor | https://waltham.patriotproperties.com/default.asp | Owner of record, year built, assessed value, building area. |
| Waltham issued permits | https://www.city.waltham.ma.us/1297/Issued-Permits | Permit `P########`, application `A########`. Also Permit Reports by Month/Year. |
| Waltham Building Dept (contact) | https://www.city.waltham.ma.us/1286/Building | 781-314-3275 / bldpermits@city.waltham.ma.us for records not online. |
| Deeds — Middlesex South | https://www.masslandrecords.com/ | Select **Middlesex South**. Property Search tab. |
| MA corporate entity search | https://corp.sec.state.ma.us/corpweb/CorpSearch/CorpSearch.aspx | Entity Name search → View Filings → latest Annual Report. |

Target frontage in Waltham (industrial / flex pockets): Third Ave, Fourth Ave, Fifth Ave,
Wyman St, Bear Hill Rd, Seyon St, Rumford Ave, Prospect St, Clematis Ave, Rear Cross St.

---

## Per-lead loop

### 1. Isolate the parcel  → `status = identified`
1. In MassMapper or the Waltham mapgeo viewer, pan the target frontage in aerial view.
2. Look for: large flat roof (≥ ~20,000 sqft), loading docks / dock doors, rooftop chillers,
   truck courts or large surface parking, low-rise concrete/brick R&D boxes.
3. Click the parcel. Record from the popup + assessor link:
   `site_address`, `apn_parcel_id`, `assessor_owner_name`, `zoning`, `lot_size_acres`,
   `year_built`, `assessed_value`, building footprint → `est_footprint_sqft`
   (set `footprint_source`; use the MassMapper measure tool if the assessor gives only gross
   floor area).
4. Classify `asset_class`: `industrial-logistics` (docks, clear-height warehouse) vs
   `flex-rd` (low-rise, office/lab-convertible, light manufacturing).
5. Write the `leads.csv` row. `date_identified` = today. Screenshot the parcel popup →
   `data/evidence/<lead_id>/parcel.png`.

### 2. Signal — permits  → `status = signal-found` (if a hit)
1. Search the address in the Waltham mapgeo viewer's permit tab, the Issued Permits lookup,
   and Permit Reports by Month/Year for the trailing 12 months.
2. Flag any permit whose description contains: `fit-out` / `fitout`, `cleanroom`,
   `lab` / `laboratory`, `HVAC`, `three-phase` / `3-phase`, `electrical service upgrade`,
   `tenant demolition` / `demo`, `white box`, `withdrawn` / `void` / `abandoned`.
3. For each hit write a `signals.csv` row: `signal_type`, `source = waltham-viewpoint`,
   `source_ref` = the `P`/`A` number, `source_url`, `date_recorded`, `dollar_amount`
   (permit valuation), `summary` (paraphrase the description), `confidence`. Screenshot →
   `data/evidence/<lead_id>/permit-<ref>.png`.
4. A withdrawn/abandoned permit after an active filing is a distress signal — `confidence`
   depends on how explicit the status is.

### 3. Signal — title  → confirms `signal-found`
1. masslandrecords.com → **Middlesex South** → Property Search → enter street number + name.
2. Walk the document timeline for the trailing 18 months. Flag: `tax lien` / `federal tax
   lien` / `municipal lien`, `lis pendens`, `notice of lease`, `lease` / `lease amendment`,
   `mortgage modification` / `loan modification` / `forbearance`.
3. For each: open the document, download the PDF → `data/evidence/<lead_id>/deed-<book>-<page>.pdf`.
   Write a `signals.csv` row: `source = masslandrecords-middlesex-south`,
   `source_ref = <book>/<page>` (or document number), `source_url`, `date_recorded`,
   `dollar_amount` if stated, `summary`, `confidence`.
4. A `notice of lease` often names the tenant and expiry — capture both in `summary`.

### 4. Qualify
- Advance only if the lead has **≥1 `signals.csv` row with a non-empty `source_ref`,
  non-empty `source_url`, and an `evidence_file` that opens.**
- If nothing surfaced after a genuine look at both sources → set `status = dropped`, note why,
  move to the next parcel. Do not manufacture a signal.

### 5. Resolve the owner  → `status = entity-resolved`
1. SOC entity search → paste the exact `assessor_owner_name` (try variants: with/without
   `LLC`, `L.L.C.`, `Realty`, `Trust`).
2. Open the entity record → View Filings → most recent **Annual Report** PDF.
3. Record in `entities.csv`: `legal_llc_name`, `soc_entity_id`, `entity_type`,
   `principal_office_address`, `domestic_state`, `absentee_flag` (`yes` if office outside MA),
   `managers` (`Name A; Name B`), `manager_titles`, `annual_report_date`, `annual_report_url`.
   Save the PDF → `data/evidence/<lead_id>/annual-report.pdf`.
4. Cross-reference the lead manager on LinkedIn (business capacity): `linkedin_url`,
   `linkedin_title`. Skip if no confident match — do not guess.
5. Note plainly, in `entities.csv` `notes`, whether the resolved owner reads as a large
   institutional operator / REIT / public-agency-adjacent lessee arrangement, versus a small
   private/family entity. This isn't a qualification gate — it doesn't block advancement — it
   just keeps the hypothesis text in the blinded index honest instead of framing routine
   institutional-owner activity (a fit-out, a lease-up) as a distress or disposition signal.

### 6. Mark `index-ready`
1. Negative check: search `site_address` + `"for sale OR for lease"`, spot-check LoopNet/Crexi
   if accessible. Applies only to a listing for the whole asset or a clear sale process — not
   ordinary partial-space leasing inside an occupied multi-tenant building (normal for campuses
   like WAL-002 through WAL-005). If the asset is already an active, publicly known opportunity,
   note it in `leads.csv` and pull the lead from the index rather than pitching it as proprietary.
2. Set `leads.status = index-ready` once steps 1–5 are complete, every evidence file opens, and
   the negative check is clear.

---

## When 10 are `index-ready`
Before assembling, confirm each lead's most recent trigger date is still current — a quick check
against the same sources already used, not a full loop re-run. A stale trigger doesn't disqualify
a lead but should be noted, and if something more recent has happened, incorporated.

Assemble `deliverables/blinded-index-BOS-128.md` (see `templates/blinded-index-entry.md`),
then run the outreach in `templates/outreach-message.md` and log every touch in
`outreach/tracker.csv`.

## Compliance
Manual browsing only. Do not script requests against masslandrecords.com, the SOC portal, or
the Waltham systems in this phase — several prohibit automated access in their terms. Any
automation is a separate plan with a terms-of-use review first.

## Access status (2026-09-10)
- **masslandrecords.com** and **corp.sec.state.ma.us** return a Secretary of the
  Commonwealth IT Division block page ("IP address flagged as a potential security risk")
  from a default connection and from CLI WebFetch. Not a CAPTCHA — a network/IP-reputation
  block. **Fix: run a VPN with a Boston exit node**, then drive the portals in a browser
  (Claude for Chrome). CLI WebFetch cannot use that VPN, so steps 3 and 5 stay a browser
  task done by a human.
- Parcel facts (step 1) came from the MassGIS Property Tax Parcels FeatureServer; permit
  signals (step 2) from the City of Waltham Q1-2026 permit report PDF. Both still reachable.
- **SEC EDGAR full-text search** (efts.sec.gov) is open and is a partial substitute for
  step 3 on assets with public-company tenants: e.g. "275 Wyman LLC" appears as the named
  landlord in SEC-filed leases by Pegasystems (2021), Chiasma (2017), and Altus Pharma
  (2007, 2009) — a notice-of-lease equivalent for WAL-003.
- **Registry document images are a dead end even with the VPN.** The masslandrecords.com
  image viewer returns 200 OK but never renders under remote/automated access (confirmed
  across two Chrome sessions; the popup-viewer toggle resets the search). The registry index
  gives book/page, doc number, party names, and page count — enough for a signal row — but
  **not** dollar amounts or lease terms. To get those: a records request to the Middlesex
  South Registry by mail / phone / in person (print + download are free). Do not spend more
  time on the viewer.
- SOC CorpSearch finds LLCs and corporations only. A **nominee/realty trust** owner (e.g.
  WAL-008, "Zee Em Trust II") has no SOC record by design — resolve the trustee with a
  registry **Name Search** for the Declaration of Trust + later trustee instruments.

---

## Seaport / South Boston Waterfront node (`BOS-SEA-###`)

Same per-lead loop as above, same qualifying bar (`asset_class`, signal + entity resolution
before `index-ready`). Different city, different tools, one extra ownership wrinkle below.

**Boundary** (as given for this node):
- West: Fort Point Channel
- North and East: Boston Harbor
- South: the historic South Boston residential neighborhood, roughly the line at First Street

### Tools

| Purpose | URL | Notes |
|---|---|---|
| Boston parcel viewer (parcel + assessor fields, address search) | https://taxparcelviewer.boston.gov (Esri Experience Builder app) | Supersedes the deprecated `app01.cityofboston.gov/parcelviewer/`. Address search works (type → click the specific suggestion → click the resulting "Search result" item to actually pan/geocode — a single click on the suggestion alone does not move the map). A geocode or click can return a "1 of N" cycling popup (`<`/`>` arrows) covering several nearby parcels — useful for surveying a cluster in fewer clicks. Does **not** surface a zoning code — use `zoning = TBD` for Boston-node leads. **Two-click identify quirk**: the first click after closing a popup is often swallowed; click the same spot again to actually open a new identify popup. Two clicks fired too fast at the same spot register as a double-click and zoom the map in instead — space clicks apart (a `wait` step between them), and if it zooms unexpectedly, use the "−" control to zoom back out. |
| Boston Assessing Online | https://www.cityofboston.gov/assessing/search/ | Owner of record, year built, assessed value — alternate to the parcel viewer's popup, which already sources from the Assessing Department. |
| Boston Permit Finder | https://permitfinder.boston.gov/ | Boston's equivalent of Waltham's Issued Permits lookup. `source = boston-permit-finder` in `signals.csv`. Not yet used this node — permit signal step still open for all BOS-SEA leads. |
| Deeds — Suffolk County | https://www.masslandrecords.com/ → **Suffolk** | Parallel to Middlesex South for Waltham. `source = masslandrecords-suffolk`. Same VPN/IP-block caveat as Middlesex South applies (see Access status above) — not yet exercised this node. |
| MA corporate entity search | https://corp.sec.state.ma.us/corpweb/CorpSearch/CorpSearch.aspx | Same statewide tool as Waltham. |

Target zone within the boundary (industrial pocket): the **Raymond L. Flynn Marine Industrial
Park** — Drydock Ave, Black Falcon Ave, Fid Kennedy Ave, Seafood Way. Most of the rest of the
Seaport boundary is now office/lab/hotel stock that does not qualify as `industrial-logistics`
or `flex-rd`.

### BPDA / Massport public-land ownership wrinkle

Several Marine Industrial Park parcels sit on land owned by the Boston Planning & Development
Agency (recorded as "ECONOMIC DEVELOPMENT AND INDUSTRIAL CORP OF BOSTON" / EDIC/BPDA) or by
Massport, with `Land Use = BOST REDEVELOP AUTH` / `OTHER PUBLIC LAND`. Two distinct cases:

1. **Lessee named directly in the `Owner` field** (e.g. `25 FID KENNEDY LLC LESSEE`,
   `8 SEAFOOD WAY LLC - SUB LESSEE`) — resolves cleanly via SOC CorpSearch exactly like a
   normal LLC owner. No extra step needed.
2. **Only the public authority is named, no lessee** (e.g. 5-11 Drydock Ave, parcel
   `0602674175`, Total Value $29,764,000; 306 Northern Ave, parcel `0602674225`, Total Value
   ~$16,744,000) despite a non-zero Building Value implying a real tenant exists — SOC search
   on the authority's name will not surface a private operator. **Not yet resolved this
   session**; the analogous fix to Waltham's trust-owner path (WAL-008, resolved via a registry
   Name Search instead of SOC) is likely a **BPDA Marine Industrial Park tenant/lease directory
   lookup** rather than SOC or a registry Property Search — not yet attempted. These two
   parcels are deferred (not written to `leads.csv`) until that path is worked out.

### Status (2026-09-12)
Parcel-isolation survey (`status = identified`) complete for 3 candidates: `BOS-SEA-001`
(25 Fid Kennedy Dr), `BOS-SEA-002` (1 Seafood Wy), `BOS-SEA-003` (8 Seafood Wy) — each written
to `leads.csv` with a saved parcel-popup screenshot at `data/evidence/<lead_id>/parcel.jpg`.
Permit signals, title signals, and SOC entity resolution not yet started for any of the three.
The Fort Point Channel-adjacent warehouse blocks (Necco Court / Melcher St area) have not yet
been surveyed.

---

## Status log (2026-09-14)

Gap-closure pass on the 6 open items flagged when the BOS-128 deliverable was re-blinded
(2026-09-13):

- **Kadima email domain — closed.** `zm@kadimare.com` confirmed correct (Kadima's own site +
  RocketReach email-format match). The "verify domain" flag in `outreach/draft-emails.md` was
  itself the error (truncated display) — removed.
- **LinkedIn cross-reference of named managers — closed, logged in `data/leads.csv` notes
  per lead.** Confirmed: Gottlieb (President/CEO) + Hill (VP & Chief Counsel), both Hobbs
  Brook Real Estate (WAL-003/010); Provost, SVP Leasing at BXP (WAL-008); Reingardt, CFO
  Northwood Investors (WAL-001). Not found: Fox, Gerrity (WAL-006). **Discrepancy flagged:**
  Parsekian and Patel (WAL-009) show as Founder/Principal, Azad Legacy Partners on LinkedIn,
  not KHS Management as filed with SOC — likely the same people, but the KHS Management tie
  is unconfirmed and should be re-verified before it's used as the current operating sponsor.
- **Zoning (WAL-001, 002, 003, 005, 006) — closed 2026-09-14.** Confirmed via
  walthamma.mapgeo.io's Zoning theme in a real browser session (the headless WebFetch
  attempt earlier that day couldn't reach it). Result: WAL-001/002/005/006 = `COMMERCIAL`;
  WAL-003 = `LIM COMM`. Note the earlier corridor-pattern guess (all five `LIM COMM`) was
  wrong for 4 of 5 — good that `leads.csv` held `TBD` instead of writing the guess in.
- **Registry document images — partially closed 2026-09-14.** `masslandrecords.com` is still
  hard-blocked (403, headless) confirming the 2026-09-10 finding stands. But for the two
  public-company tenants, lease terms were sourced directly from SEC filings/press releases
  instead of the registry image - actually better data than the registry would have given
  (registry notices don't carry rent):
  - WAL-002 Akebia: ~43,474 SF, $898,317 initial annual rent, signed 2026-01-27 (SEC 10-K
    exhibit). WAL-002 Madrigal: ~45,000 SF (BXP/press).
  - WAL-004 Boston Dynamics: ~320,000 SF, long-term, phased move-in from mid-2027 (BXP press
    release).
  All three registry-only financing items (WAL-006, WAL-007, WAL-009) are now closed via
  `massrecords-api` capture - see entries below. **No financing amounts remain unconfirmed
  for any of the 10 leads.**
- **WAL-006 registry document (bk85492/240) - closed 2026-09-14** using `massrecords-api`
  (the project's own local capture tool - Tampermonkey userscript + FastAPI ingest server;
  see `massrecords-api/README.md`). User captured all 13 page images live via the "Capture
  All Pages" button on the ImageViewerEx.aspx popup; images landed in
  `massrecords-api/images_captured/Middlesexsouth/_unlinked/` (unlinked because the
  Default.aspx search-result page wasn't separately sent to the API, so there was no record
  to match book/page against - images are still fully readable directly by file path).
  Document is a **Subordination, Non-Disturbance and Attornment Agreement (SNDA)**, not a
  lending/mortgage agreement: Kreocs Lending I LLC (lender, pre-existing 2021-05-26 mortgage)
  + BP3-BOS6 21 Hickory LLC (landlord, signed by Michael Gerrity) + Bonito Biosciences Inc
  (tenant, signed by Brant Binder, President), subordinating Bonito's 2026-01-20 lease to
  Kreocs' mortgage. No dollar figure - SNDAs don't state loan/rent amounts by design, so this
  is a closed gap, not a residual one. Bonus: Gerrity's landlord-side signature independently
  corroborates the SOC-filed signer name (LinkedIn had found no match for him).
- **WAL-007 registry document (bk85206/84) - closed 2026-09-14** using `massrecords-api`.
  26 pages captured. Document is a **Mortgage (Secures Future Advances)**: MAG RE
  Holdings-Waltham LLC (mortgagor) to Ally Bank, Utah-chartered, Cranberry Township PA
  (mortgagee), securing a loan **not to exceed $14,100,000.00** under a Commercial Real
  Estate Loan and Security Agreement/Promissory Note. Exhibit A confirms the blanket/portfolio
  scope (also covers 1345-1347-1349 Main St, consistent with the earlier registry-index
  finding). Signed by **Matthew McGovern as Manager**, notarized 2026-02-03 in Middlesex
  County MA - a direct signature match to the SOC-filed manager name (stronger than the
  earlier sister-entity Bloomberg LEI corroboration).
- **WAL-009 registry document (bk85256/295) - closed 2026-09-14** using `massrecords-api`.
  17 pages captured. Document is an **Amended and Restated Mortgage and Security Agreement**,
  dated 2026-02-20: BH Waltham I LLC (mortgagor) to **Beacon Bank & Trust** (mortgagee),
  securing **$6,000,000.00**. Sec. 34 shows this amends/restates a prior mortgage dated
  2021-07-02 (bk78178/184) - the same lender relationship carried forward and upsized, not a
  new lender as the earlier "refi/cash-out" phrasing implied. Signed by **Robert Parsekian**
  as Authorized Person of BH Waltham I LLC, notarized 2026-02-11 Middlesex County MA - a
  direct signature match to the SOC-filed signer name, independent of the earlier LinkedIn
  work.
- **massrecords-api code bug found and fixed 2026-09-14 (root cause, not just a workaround):**
  `_image_file_path()` in `api.py` only used book/page for foldering when a DB `record` row
  had matched via `find_record_by_book_page()` - which requires `capture.user.js`'s "Send to
  Local API" button to have been clicked on the search-results row first. But the image-capture
  script already sends raw `book`/`page` on every capture regardless (`selectedBookPage()`
  reads them straight off the opener's highlighted row, no linking needed) - the server was
  just discarding that data whenever there was no DB match, so *every* un-linked batch, from
  every different document, fell into one shared `<District>/_unlinked/` folder with generic
  `p<n>_of_<total>` filenames and collided (this happened twice: WAL-006/WAL-007, then
  WAL-007/WAL-009). **Fix:** `_image_file_path()` now falls back to the raw `req.book`/
  `req.page` the browser sent when there's no DB record match, and only lands in `_unlinked/`
  when neither is available (e.g. truly no unique row was selected on the opener). Applied in
  `massrecords-api/api.py`, server restarted to pick it up. Existing misfiled batches
  (WAL-007's 26 pages, WAL-009's 17 pages) were sorted by hand into `_unlinked/<book>-<page>/`
  subfolders before this fix landed; new captures should now auto-land in
  `<Party Name>/<book>-<page>/` even without clicking "Send to Local API" first, as long as
  exactly one row is highlighted on the search-results tab at capture time.
- **massrecords-api "Send to Local API" parser bug found and fixed 2026-09-14 (root cause):**
  clicking "Send to Local API" on the WAL-009 (bk85256/295) Book/Page Search results page
  reported "Parsed 0 row(s)" despite one visible result row. Added debug-capture logging to
  `/ingest` (dumps raw HTML to `debug_captures/` whenever `parse_search_results()` returns zero
  rows) and used the saved `debug_captures/Middlesexsouth-20260914-143236.html` to diagnose
  without needing another round-trip through the user. Root cause: `parser.py`'s
  `SEARCH_COLUMNS` contract (11 `<td>` cells: select/type/name/book/page/type_desc/file_date/
  street_number/property_descr/view_img/add_to_basket) was reverse-engineered from a Suffolk
  County *Name* Search grid; a *Book/Page* Search grid instead renders a narrower 7-cell row
  (select/file_date/book_page-combined/type_desc/town/view_img/add_to_basket), so
  `len(cells) < len(SEARCH_COLUMNS)` silently `continue`d past every row. A second, related bug
  surfaced during the fix: `tr.DataGridRow` also matches rows inside the `DocDetails1_*`
  document-detail panel (already parsed separately by `parse_document_detail`) when a detail
  view is open alongside the grid, so an 8-cell `DocDetails1_GridView_Details` row was initially
  being misread as a 7-column Book/Page result. **Fix (both in `massrecords-api/parser.py`):**
  (1) added a `SEARCH_COLUMNS_BOOK_PAGE` contract and pick it via cell count when a row has 7-10
  cells, splitting the combined `book_page` cell on `/` into `book`/`page`; (2) skip any row
  whose nearest ancestor-with-id starts with `DocDetails` before column-matching it. Verified
  by re-running `parse_search_results()` against the saved debug HTML (now returns exactly 1
  row: `book=85256, page=295, type_desc=MORTGAGE, town=WALTHAM`) and by replaying the same HTML
  through the live, restarted `/ingest` endpoint (`{"parsed_rows":1,"inserted":1,"updated":0,
  "detail_attached":true}`) — the resulting DB record independently corroborates doc_no 19391,
  consideration `6000000.00`, status `Verified/Certified` for WAL-009, matching the $6,000,000
  figure already extracted from the document images. Server restarted to pick up the fix.
- **massrecords-api image-capture browser bug found and fixed 2026-09-14 (third, distinct bug):**
  after the two fixes above, a live re-capture of WAL-009's images still landed in
  `Middlesexsouth/Unknown/MORTGAGE-WALTHAM/` instead of a real book/page folder. Root cause was
  in `capture-image.user.js`, not Python: `selectedBookPage()` read the opener's selected row's
  book/page from hardcoded `cells[3]`/`cells[4]`, which is only correct for the 11-column Name
  Search grid. On the 7-column Book/Page Search grid, `cells[3]` is Type Desc. ("MORTGAGE") and
  `cells[4]` is Town ("WALTHAM") — so the script sent those as book/page, matched no DB record,
  and `_image_file_path()` (correctly, given the bad input) fell back to `Unknown/MORTGAGE-
  WALTHAM/`. **Fix:** `selectedBookPage()` now branches on `cells.length` the same way
  `parser.py` does — 11+ cells uses the old separate-column indices, 7-10 cells reads the
  combined Book/Page cell at index 2 and splits on `/`. Bumped `@version` to 2.1. Also gave
  Book/Page Search rows a usable `name` in `parser.py`: since that grid has no party-name
  column at all, the Town cell is now reused as `record.name` (dynamically read per-row, not
  hardcoded — confirmed nothing named after any specific town appears in `api.py`/`parser.py`/
  `store.py`/either userscript via `grep`) so records/folders read e.g. `Waltham` instead of
  `Unknown`. Backfilled the one pre-existing null-name WAL-009 DB row to match. Deleted a
  17-image duplicate batch that had already landed in the wrong `Unknown/MORTGAGE-WALTHAM/`
  folder under the old script version (images 57-73 in `images.db`) since it duplicated the
  already-correctly-filed `_unlinked/85256-295/` batch. **Still needs a live re-verification**:
  the browser tab is running the pre-fix script version — next "Capture All Pages" click must
  use the updated `capture-image.user.js` (re-paste it, or reload if Tampermonkey-managed) to
  confirm it now folders under `Middlesexsouth/Waltham/85256-295/`.
- **Outreach drafts — sender info filled in** (Ahmet Bolat, ahmet@viabolat.com) across all 6
  drafts in `outreach/draft-emails.md`. Drafts are send-ready; nothing has been sent yet —
  `outreach/tracker.csv` still has 0 of 7 rows with a `date_sent`.
- **Outreach funnel design decided 2026-09-14 — read this before drafting/sending anything:**
  the user does not want calls; the goal of the first touch is a reply signaling interest,
  nothing more. Explicit 3-stage funnel, decided in conversation (not yet applied to any real
  send):
    1. **Feeler email** (new: `outreach/feeler-emails.md`) — teases ONE specific lead's signal
       story (assembly/financing/permit sequence, etc.) with no identifying facts (no address,
       parcel ID, permit number, tightened dollar figures, or owner/manager name) and no
       attached data. Only ask: reply if interested. No call requested anywhere in the funnel.
    2. **On reply** — send that lead's blinded index entry (the existing
       `deliverables/blinded-index-BOS-128.md` format: metrics + signal timeline, owner still
       `[LOCKED]`).
    3. **Only after payment** — send the full unmasked lead (owner entity, decision-maker
       contact).
  **Why:** user's own words — "i dont want to lose a client from not having the 3 leads masked
  at the same time dont want to be pushy there is that fine line" and "Iam looking for
  acceptance first then the masked data later and if they are interested the full lead after
  payment" — i.e. never let the masked data or the full lead leak into a stage that hasn't been
  paid/earned yet, and keep the very first ask as low-friction as possible (a reply, not a
  meeting).
  **How this relates to the existing `outreach/draft-emails.md` (Variant C) drafts:** those 6
  drafts predate this funnel decision — they pitch "10 Route 128/Waltham assets" as a feed
  rather than one specific lead's story, though they already avoid a call-ask and already don't
  attach masked data. They have NOT been superseded or deleted; whether to rewrite them into the
  single-lead feeler style before ever sending, or keep both variants for different prospects, is
  an **open decision for the user** — don't unilaterally pick one over the other.
  **Skill idea raised, not yet built:** user asked whether a slash-command skill (e.g.
  `/emailcheck`) that takes a qualified-leads round + `deliverables/` and generates a relevant
  feeler draft per lead would make sense once this funnel is stable. Agreed it's a reasonable
  fit *once proven* — recommended drafting a few more feelers by hand first (this is only the
  first one, for WAL-007/Kadima) to lock in voice/format/the no-identifying-facts constraint,
  then encode it as a skill so it isn't automating a first guess. Not built; revisit after the
  next lead-qualifying round if the user still wants it.
