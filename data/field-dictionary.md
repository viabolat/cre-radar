# Field Dictionary

All three CSVs are UTF-8, comma-delimited, one header row. Quote any value containing a comma.
Dates are ISO `YYYY-MM-DD`. Leave a cell empty only where the column notes allow it.

---

## leads.csv

| Column | Required | Allowed values / format | Notes |
|---|---|---|---|
| `lead_id` | yes | `BOS-128-WAL-###` | Sequential from `001`. Never reused, even for dropped leads. |
| `status` | yes | `identified` \| `signal-found` \| `entity-resolved` \| `index-ready` \| `dropped` | Advances in order. `dropped` is terminal. |
| `site_address` | yes | `123 Example St, Waltham, MA 02451` | As shown in MassMapper / assessor. |
| `municipality` | yes | `Waltham` | Fixed for this phase. |
| `apn_parcel_id` | yes | assessor parcel ID string | From the MassMapper parcel popup. |
| `assessor_owner_name` | yes | free text | Usually an LLC. Verbatim from the record. |
| `asset_class` | yes | `industrial-logistics` \| `flex-rd` | `flex-rd` = low-rise R&D / lab-convertible. |
| `est_footprint_sqft` | no | integer | Gross building area (MassGIS `BLD_AREA`) or, where CAMA has not caught up with a new build, the GSF stated on the permit. Empty if neither is available yet. |
| `footprint_source` | yes | `assessor` \| `gis-measured` \| `massgis-l3-bld_area` \| `permit-description` | `massgis-l3-bld_area` = `BLD_AREA` from the MassGIS Property Tax Parcels FeatureServer; `permit-description` = GSF quoted in the building permit. |
| `zoning` | yes | zoning code string, or `TBD` | e.g. `LIM COMM`, `COMMERCIAL`. From the MassGIS parcel record or Waltham zoning map. `TBD` allowed until confirmed against the Waltham zoning map in a browser. |
| `lot_size_acres` | no | decimal | Empty if not shown. |
| `year_built` | no | `YYYY` | Empty if not shown. |
| `assessed_value` | no | integer USD, no separators | Total assessed value. |
| `date_identified` | yes | `YYYY-MM-DD` | Day the parcel was recorded here. |
| `notes` | no | free text | Anything the columns don't capture. |

---

## signals.csv

| Column | Required | Allowed values / format | Notes |
|---|---|---|---|
| `signal_id` | yes | `SIG-###` | Sequential. |
| `lead_id` | yes | matching `leads.lead_id` | |
| `signal_type` | yes | see list below | One value per row. |
| `source` | yes | `waltham-viewpoint` \| `masslandrecords-middlesex-south` | `waltham-viewpoint` covers the city's published permit reports (ViewPoint-backed). Add new sources here if the phase expands. |
| `source_ref` | yes | permit number, or `book/page`, or document number | **Never blank.** This is what lets a broker re-pull the record. |
| `source_url` | yes | full URL to the record or its search result | **Never blank.** |
| `date_recorded` | yes | `YYYY-MM-DD` | Date the permit/document was filed or recorded. |
| `dollar_amount` | no | integer USD | Permit valuation or lien amount if stated. |
| `summary` | yes | free text, 1–2 sentences | Factual paraphrase of the record only. No inference about intent beyond what the document says. |
| `evidence_file` | yes | path under `data/evidence/<lead_id>/`, or a shared file under `data/evidence/_permits/` | Screenshot or downloaded PDF. Must exist and open. A single permit-report PDF that covers many leads lives once under `_permits/` and is cited by page number in `summary`. |
| `confidence` | yes | `high` \| `med` \| `low` | `high` = document is explicit and current; `low` = ambiguous or stale. |

### `signal_type` values
- `permit-fitout` — general tenant fit-out
- `permit-lab-conversion` — cleanroom / lab build-out
- `permit-electrical-upgrade` — three-phase / heavy electrical
- `permit-hvac-upgrade`
- `permit-tenant-demo` — tenant demolition / white-boxing / data-center or fit-out strip-out (space give-back)
- `permit-demolition` — full building demolition (redevelopment / land-assembly signal)
- `permit-withdrawn` — permit filed then withdrawn/abandoned (distress)
- `tax-lien` — municipal, state, or federal tax lien
- `lis-pendens` — pending litigation / foreclosure notice
- `notice-of-lease` — recorded lease (exposes tenant / expiry)
- `lease-amendment`
- `mortgage-modification` — landlord renegotiated with lender

---

## entities.csv

| Column | Required | Allowed values / format | Notes |
|---|---|---|---|
| `entity_id` | yes | `ENT-###` | Sequential. |
| `lead_id` | yes | matching `leads.lead_id` | |
| `legal_llc_name` | yes | exact legal name | From the SOC record; until SOC is checked, the assessor's `OWNER1` string, flagged in `notes`. |
| `soc_entity_id` | SOC step | MA SOC entity ID number | Blank until the SOC CorpSearch step is done in a browser. |
| `entity_type` | no | `Domestic LLC` \| `Foreign LLC` \| `Domestic Corp` \| `Trust` \| ... | From the SOC record. |
| `principal_office_address` | yes | full address | Owner mailing address from the MassGIS parcel record now; replace with the Annual Report principal office once SOC is checked. |
| `domestic_state` | SOC step | 2-letter | State of formation. Blank until SOC is checked. |
| `absentee_flag` | yes | `yes` \| `no` | `yes` if the owner mailing / principal office is outside MA. |
| `managers` | SOC step | `Name A; Name B` | Managers / authorized signatories from the latest Annual Report. Blank until SOC is checked. |
| `manager_titles` | no | `Name A: Manager; Name B: Member` | If titles are given. |
| `annual_report_date` | SOC step | `YYYY-MM-DD` | Filing date of the report used. Blank until SOC is checked. |
| `annual_report_url` | SOC step | full URL to the PDF or filing page | Blank until SOC is checked. |
| `linkedin_url` | no | profile URL | Business-capacity cross-reference for the lead manager. |
| `linkedin_title` | no | free text | Current title / firm from LinkedIn. |
| `notes` | no | free text | |

### Interim rows (before the SOC step)
A row may be written with only the parcel-derived fields (`legal_llc_name` as the assessor
string, `principal_office_address` = owner mailing address, `absentee_flag`) so the ownership
picture is not lost. Columns marked "SOC step" stay blank and `notes` must say
`SOC + Annual Report lookup pending (browser)`. A lead cannot reach `entity-resolved` /
`index-ready` until those columns are filled.

### Handling personal information
Manager data is recorded in business capacity only. Include a residential address **only** if
the public Annual Report itself prints one, and never carry it into the blinded index or any
outreach material.
