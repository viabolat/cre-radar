# Stage 7 — Two independent tracks, not one merged score

**Sources:** `cre_sop/sop.md` Section 4 (Financial Distress track — see
below); Stage 2/4/5's already-captured signals plus Stage 6's negative-check
result (Activity Signal track).
**Automatable:** yes, once Stages 1–6 have produced the underlying data for
a parcel — this stage is an evaluation over existing state, not a new
external search.
**Writes to:** `data/pipeline/parcel-state.csv` (`stage7_fd_*`,
`stage7_activity_*`).

## Why two tracks, not one

Every parcel gets scored by both tracks, independently. Neither track's
internal logic is softened to accommodate the other — a parcel can score
DO NOT ADVANCE on Financial Distress and still pass Activity (or vice
versa), and Stage 9 only gates on one of them (see that doc).

## Track 1 — Financial Distress

**Source of truth: `cre_sop/sop.md` Section 4 — referenced, not forked.**
This doc does not redefine the 5 signals, the 2-signal minimum, or the
Advance / Advance-with-caveat / DO NOT ADVANCE verdict logic. Apply
`cre_sop/sop.md` Section 4 exactly as written there.

**Discipline on future `cre_sop/sop.md` revisions:** because this track
references rather than forks, a future revision to `cre_sop/sop.md`
Section 4 (e.g. v12→v13) is not automatically inherited here without a
check. Before applying any such revision to this track, explicitly
determine whether the change is general to Financial Distress as a concept,
or specific to the Suffolk/Boston-office context `cre_sop` was built for
(e.g. a recency window or signal definition tuned to that office's deal
flow). Only changes confirmed general apply here; changes confirmed
context-specific do not, and should be noted in this doc's `stage7_fd_note`
guidance instead. Never silently propagate a `cre_sop` revision as-is.

**Discipline on source geographic coverage — evaluable vs. satisfied:**
several of `cre_sop`'s numbered sources (Section 2) are Boston/Suffolk-
specific, not statewide, because `cre_sop` was built for a Boston-office
scope:
- **Source #2** (Boston Property Lookup / properties.boston.gov) and
  **Source #3** (Boston Assessing Parcel Data / gisportal.boston.gov) are
  both explicitly Boston-only. Signal 1 (tax delinquency) is defined
  against these two sources.
- **Source #6** (court records) is checked against a specific division —
  currently Eastern Housing Court plus Superior Court Civil for Suffolk
  County — which is a Suffolk-specific division choice; a parcel in a
  different county needs the equivalent division for *that* county, not
  Eastern Housing Court by default.

Before evaluating any signal whose source is Boston/Suffolk-specific for a
parcel outside that geography: confirm whether an equivalent source exists
and covers the target municipality/county. If it does not (or hasn't been
confirmed to), mark that signal `not-evaluable`, never `not-satisfied` —
these are different things, and an unavailable data source must not
silently count as a clean signal. Record which source was checked and why
it was judged not-evaluable in `stage7_fd_note`.

This is separate from — and in addition to — `cre_sop/sop.md`'s own
existing open item (Section 8) that Signal 1 may be effectively unusable
even *within* Boston, since neither Source #2 nor #3 exposes a real
delinquency field there either. Outside Boston, Signal 1 is not-evaluable
for the added reason that the sources themselves don't cover the geography
at all.

**Output:** internal only. `stage7_fd_verdict` (`advance |
advance-with-caveat | do-not-advance`) is never copied into any
client-facing output, per `cre_sop`'s own principle and Stage 9's handling
below.

**Procedure:**
1. For each of the 5 signals, first confirm source coverage for the
   parcel's municipality/county per the discipline above. Mark any
   signal `not-evaluable` if its source doesn't cover that geography (or
   coverage hasn't been confirmed) — do not evaluate it as absent.
2. For signals with confirmed coverage, evaluate the parcel's entity/
   registry data (Stages 3–5) against `cre_sop/sop.md` Section 4's
   definitions.
3. Apply the 2-signal minimum and verdict logic exactly as defined there,
   counting only evaluable signals toward the minimum.
4. Set `stage7_fd_status` = `done`, `stage7_fd_date` = today,
   `stage7_fd_verdict` = the resulting verdict, `stage7_fd_note` = which
   signals were met, not-satisfied, or not-evaluable (and why, for
   not-evaluable cases) — for internal audit only.
5. If evaluation can't complete (missing underlying data from an earlier
   stage still in `needs-handoff`), set `stage7_fd_status` =
   `needs-handoff` with `stage7_fd_note` describing what's missing.

## Track 2 — Activity Signal

**This is a starting heuristic, not a finalized rule.** Apply it, watch
what it actually filters in and out across real runs, and correct it the
first time a real case doesn't fit — the same approach `cre_sop` took with
its own Signal 2 before v12. Do not treat this criteria list as settled.

**Criteria (all required):**
1. `stage6_pass = yes` — negative check explicitly clear (hard gate; not
   merely `stage6_status = done`, which also covers the case where an
   active listing was found — see `06-negative-check.md`).
2. The resolved owner (Stage 3) is not a large diversified public REIT/
   portfolio operator — the same judgment BOS-128 applied to correctly drop
   WAL-002/004/005 as "no thesis beyond routine BXP activity."
3. At least one dated recent event tied to the parcel (permit, financing,
   ownership-structure change, lease change, assembly) from Stages 2–5.
4. That event is tied to a plausible reason it might matter — not just
   logged as a bare fact.

**Procedure:**
1. Check `stage6_pass`. If `no`, fail immediately: `stage7_activity_status`
   = `done`, `stage7_activity_pass` = `no`, `stage7_activity_note` =
   "failed Stage 6 negative check."
2. If `yes`, evaluate criteria 2–4 against Stages 2–5's recorded data.
3. Set `stage7_activity_status` = `done`, `stage7_activity_date` = today,
   `stage7_activity_pass` = `yes` or `no`, `stage7_activity_note` =
   which criteria were met/failed and why.
4. If evaluation can't complete (missing underlying data), set
   `stage7_activity_status` = `needs-handoff` with `stage7_activity_note`
   describing what's missing.

## Handoff

None structurally — this stage evaluates data already captured by Stages
1–6. A `needs-handoff` status here only reflects an earlier stage's
handoff still being open, not a new manual step of its own.
