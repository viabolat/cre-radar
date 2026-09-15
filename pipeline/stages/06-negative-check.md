# Stage 6 — Negative check

**Source:** LoopNet, CBRE, Cushman & Wakefield, Newmark listing search (or
the equivalent active-broker listing platforms for the target market).
**Automatable:** mostly — the search itself is automatable; borderline
relevance calls need a manual read.
**Writes to:** `data/pipeline/parcel-state.csv` (`stage6_*`).

## What this stage does

Searches LoopNet/CBRE/Cushman/Newmark (and equivalent platforms) for an
active listing on the parcel, to rule out signals that are already public
market activity rather than an off-market opportunity — the same check
BOS-128 already runs per lead. This is a hard gate Stage 7's Activity track
reads directly (see `07-signal-scoring.md`).

## Procedure

1. Search LoopNet, CBRE, Cushman & Wakefield, Newmark (and any other
   broker platform active in the target market) for the parcel's
   address/APN.
2. If no active listing is found: set `stage6_pass` = `yes`,
   `stage6_status` = `done`, `stage6_date` = today, `stage6_note` = which
   platforms were checked.
3. If an active listing is found: set `stage6_pass` = `no`, `stage6_status`
   = `done` (the check completed — it found something, it didn't fail to
   complete), `stage6_date` = today, `stage6_note` = the listing URL and a
   short description.
4. Borderline cases — a stale listing (e.g. BOS-128's WAL-008 Showcase.com
   listing, months old with no other activity) — need a judgment call: use
   your read of the listing's staleness/relevance rather than an automatic
   fail. Record the reasoning in `stage6_note` either way.
5. `stage6_status` = `done` covers both outcomes (an active listing found,
   or confirmed none found) — `stage6_status` alone does not tell Stage 7
   which happened; `stage6_pass` is the field that does. Never leave
   `stage6_pass` blank once `stage6_status` = `done`.

## Handoff

Borderline/stale-listing judgment calls only (step 4) — the search itself
is automatable; only the relevance call is manual.
