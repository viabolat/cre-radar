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

**Precedent (Revere, 2026-09-15):** a use-code-only bound (excluding 1xx
residential and 9xx government/institutional) still left 675 parcels —
workable as a discovery-stage pool, but too large to hand to Stage 2 as-is
when that town's permit vendor is itself a full manual handoff (see Stage
2's Citizenserve note): running Stage 2 unfiltered would just write ~675
near-identical `needs-handoff` rows for zero new signal. Decision: tighten
further at that point with a minimum assessed-value bound (`TOTAL_VAL`
field) sized to leave a queue a human can actually work through by hand —
$1M cut Revere to 257. Not promoted to a fixed rule here: whether this
second bound belongs in Stage 1 (tighten before writing) or is better left
as a documented post-hoc prune once Stage 2's vendor category is known
(as done for Revere) is itself worth revisiting if this recurs for another
manual-heavy-vendor town.

## Known limitation — logged, not reversed

The USE_CODE-9xx exclusion (government/institutional/charitable-exempt
parcels — municipal, housing authority, church, state/federal government)
applied as part of the query bound can rarely filter out a genuine
disposal-event signal: a city or authority selling a surplus property is
exactly the kind of dated, market-facing event Stage 7's Activity track
looks for, and that owner will never appear in this pool. Accepted
tradeoff, not worth reversing — the exclusion's purpose (no private owner
to pitch, for the overwhelming majority of 9xx parcels) still holds; this
is an acknowledged edge case, not a silent gap.

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
