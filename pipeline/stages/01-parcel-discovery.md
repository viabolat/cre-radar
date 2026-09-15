# Stage 1 — Parcel discovery

**Source:** MassGIS Property Tax Parcels FeatureServer.
**Automatable:** yes.
**Writes to:** `data/pipeline/parcel-state.csv` (new rows).

## What this stage does

Query the MassGIS Property Tax Parcels FeatureServer scoped to the target
town/neighborhood. Not asset-class-locked at the search stage — scans
whatever parcels exist there. Asset-class filtering happens later, once, at
Stage 9 (see `cre-radar-generalization-spec.md`'s scope bullet: "not fixed
at discovery, filtered at matching").

## Open question before this can run for real

Ambiguity 2 in the generalization-spec plan review: the spec doesn't bound
this query by asset class, but an unfiltered "everything in a town" query is
unbounded, and `cre_sop`'s own SOP caps its candidate pool at 25–30 parcels
via an `LU`/`LU_DESC` filter for exactly this reason. Needs a decision on
what, if anything, bounds Stage 1's query (e.g. excluding purely
residential LU codes) short of reintroducing a fixed asset class. Until
decided, run this stage with a manually-chosen, documented bound per town
rather than an unfiltered query.

## Procedure

1. Confirm the target town's masslandrecords.com district status in
   `massrecords-api/README.md`'s **Districts** table — Stage 4 will need
   this later, and per ambiguity 7, it's worth knowing before sinking
   Stage 1–3 work into a town that can't clear Stage 4 (decision on whether
   to hard-block on this is still open; for now, flag it, don't block on
   it).
2. Query the MassGIS Property Tax Parcels FeatureServer for the target
   town/neighborhood, applying whatever bound was decided per the open
   question above.
3. For each parcel returned, write a new row to `data/pipeline/parcel-
   state.csv`: `parcel_id` (see ambiguity 1 — scheme not yet decided;
   until it is, use `<municipality-code>-<sequence>` and flag it),
   `municipality`, `submarket`, `asset_class_hint` (a hint only — not a
   filter), `apn_parcel_id`, `site_address`, `date_identified` = today,
   `current_stage` = `1`, `overall_status` = `active`, `stage1_status` =
   `done`, `stage1_date` = today, `stage1_note` = query bound used. All
   other `stageN_status` columns start `not-started`.

## Handoff

None — this stage is fully automatable.
