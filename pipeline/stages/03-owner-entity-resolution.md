# Stage 3 — Owner entity resolution

**Source:** MA Secretary of the Commonwealth, Corporations Division
(CorpSearch).
**Automatable:** conditionally. CorpSearch is a MA government site and, like
masslandrecords.com, enforces an IP-based access restriction — searches from
a non-MA-exit IP can be blocked, requiring a Boston-exit VPN. Where the
session's IP isn't blocked, the search is a plain automatable fetch; where it
is, this stage becomes a manual/browser handoff. Not a fixed answer — check
per session.
**Writes to:** `data/entities.csv` (new entity row), `data/pipeline/parcel-
state.csv` (`stage3_*`).

## What this stage does

For each parcel with a signal from Stage 2, resolve the assessor-listed
owner name to its SOC entity record: entity type, domestic state, principal
office address, managers/signers, absentee flag.

## Procedure

Follow `data/field-dictionary.md`'s existing `entities.csv` schema and
interim-row convention exactly (see `field-dictionary.md`, "### Interim rows
(before the SOC step)") — this stage is the generalized version of work
BOS-128 already does per-lead:

1. Search MA SOC CorpSearch for the assessor-listed owner name.
2. If the search is blocked by the IP restriction: write an interim
   `entities.csv` row with parcel-derived fields only (`legal_llc_name` =
   assessor string, `principal_office_address` = owner mailing address,
   `absentee_flag`), `notes` = `SOC + Annual Report lookup pending
   (browser)` exactly as `field-dictionary.md` specifies, and set
   `stage3_status` = `needs-handoff` in `parcel-state.csv` with
   `stage3_note` = "CorpSearch IP-blocked; needs VPN/browser session."
3. If the search succeeds (no block): fill `soc_entity_id`, `entity_type`,
   `domestic_state`, `managers`, `manager_titles`, `annual_report_date`,
   `annual_report_url` directly, and set `stage3_status` = `done`.
4. For a trust owner (no SOC registration), resolve via registry Name
   Search per `field-dictionary.md`'s Trust owners section instead of
   treating `soc_entity_id`/`domestic_state` as missing.
5. Once a handed-off row is completed (columns marked "SOC step" filled
   in), update `stage3_status` to `done`, `stage3_date` = today.

## Handling personal information

Per `field-dictionary.md`: manager data in business capacity only; a
residential address only if the public Annual Report itself prints one,
and never carried into any client-facing output.

## Handoff

Real, but conditional — not structural like Stage 4's Incapsula block.
Triggered only when the session's IP is subject to MA gov's access
restriction; resolved by completing the search from a Boston-exit VPN /
browser session and filling in the interim row per step 5.
