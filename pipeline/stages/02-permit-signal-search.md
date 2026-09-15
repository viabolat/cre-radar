# Stage 2 — Permit signal search

**Source:** municipal permit portal for the target town (vendor unknown
until checked — see `data/source-registry.md`).
**Automatable:** depends on vendor category (see below).
**Writes to:** `data/signals.csv` (new signal rows), `data/pipeline/parcel-
state.csv` (`stage2_*`), `data/source-registry.md` (new/updated source
entry).

## What this stage does

No single statewide permit system exists — every town runs its own. Before
searching, check `data/source-registry.md` for the target town's vendor; if
already characterized, use the recorded approach and skip straight to
searching. If not, this stage performs that one-time lookup and records it
permanently.

## Vendor categories

- **Hard-blocked, permanent manual handoff** — same category as the
  registry (Stage 4): nothing programmatic works, ever.
- **Login-gated, plausibly automatable with setup** — e.g. Citizenserve
  (Revere, Brockton, Medway). Account setup is a one-time manual step per
  town/vendor. Whether subsequent searches can be automated with stored
  credentials is untested — see ambiguity 4 (no credential-storage
  mechanism decided yet). Until that's resolved, treat every Citizenserve
  town as a manual handoff for the search itself, not just account setup.
- **Public but JS-rendered** — e.g. PermitEyes (Falmouth, Chelmsford,
  Mashpee, North Reading, Berkshire County). No login wall, but a plain
  fetch returns empty tables — data loads via JS after render. Try, in
  order, before treating as a handoff: (1) the page's own "Export to Excel"
  function via a rendered-browser interaction; (2) reverse-engineering the
  underlying AJAX/XHR call.
- **Static/parseable** — e.g. Waltham's PDF permit reports, or any town with
  a queryable structured database. Automatable outright, or a parse step.

## Procedure

1. Read `data/source-registry.md` for the target town's permit vendor entry.
2. If absent: identify the vendor, categorize it per the list above, attempt
   the category's recommended approach, and write a new entry to
   `data/source-registry.md` regardless of outcome (per the Standing
   requirement — record what was tried even if it didn't work).
3. If the category allows automation: search for permits on parcels from
   Stage 1, and for each qualifying signal found, write a new row to
   `data/signals.csv` per `data/field-dictionary.md`'s existing schema
   (`signal_type`, `source`, `source_ref`, `source_url`, `date_recorded`,
   `summary`, `evidence_file`, `confidence`).
4. If the category is a handoff: set the parcel's `stage2_status` to
   `needs-handoff` in `parcel-state.csv`, with `stage2_note` describing
   exactly what's needed (e.g. "Citizenserve account required for
   <town>").
5. Once signals are recorded (automated or after a handoff resumes), set
   `stage2_status` = `done`, `stage2_date` = today.

## Handoff

Hard-blocked and (for now) login-gated vendors route here. See `data/
source-registry.md`'s Citizenserve entry for the open credential-storage
question (ambiguity 4) blocking further automation there.
