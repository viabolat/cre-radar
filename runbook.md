# Harvest Runbook — Route 128 / Waltham node

Goal: 10 leads at `index-ready` in `data/leads.csv`, each with ≥1 backed signal and a resolved
owner. Work one lead fully before starting the next. Save every screenshot / PDF to
`data/evidence/<lead_id>/`.

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

### 6. Mark `index-ready`
Set `leads.status = index-ready` once steps 1–5 are complete and every evidence file opens.

---

## When 10 are `index-ready`
Assemble `deliverables/blinded-index-BOS-128.md` (see `templates/blinded-index-entry.md`),
then run the outreach in `templates/outreach-message.md` and log every touch in
`outreach/tracker.csv`.

## Compliance
Manual browsing only. Do not script requests against masslandrecords.com, the SOC portal, or
the Waltham systems in this phase — several prohibit automated access in their terms. Any
automation is a separate plan with a terms-of-use review first.

## Access status (2026-09-10)
- **masslandrecords.com** and **corp.sec.state.ma.us** both return a Secretary of the
  Commonwealth IT Division block page ("IP address flagged as a potential security risk")
  from the Claude-for-Chrome session's connection and from the CLI's WebFetch. Persisted on
  retry. Not a CAPTCHA — a network/IP-reputation block. Steps 3 and 5 are on hold until
  those portals are reachable from a clean network (no VPN, residential IP, or a different
  machine), done by a human.
- Parcel facts (step 1) came from the MassGIS Property Tax Parcels FeatureServer; permit
  signals (step 2) from the City of Waltham Q1-2026 permit report PDF. Both still reachable.
- **SEC EDGAR full-text search** (efts.sec.gov) is open and is a partial substitute for
  step 3 on assets with public-company tenants: e.g. "275 Wyman LLC" appears as the named
  landlord in SEC-filed leases by Pegasystems (2021), Chiasma (2017), and Altus Pharma
  (2007, 2009) — a notice-of-lease equivalent for WAL-003.
