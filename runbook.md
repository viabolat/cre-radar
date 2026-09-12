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
