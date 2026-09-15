# Pipeline — generalized CRE-Radar architecture

This directory holds the generalized version of the BOS-128 process:
`cre-radar-generalization-spec.md` (project root) is the design; the docs
under `stages/` are the procedure a Claude Code session follows to run it
for any town + asset class, not just Waltham/industrial.

## How it works

Each file under `stages/` documents one of the 9 stages from the spec: what
it does, what source(s) it touches, what's automatable vs. a manual handoff,
and what it writes back to state. There's no pipeline code yet — every stage
today is a well-specified procedure a session executes by hand each run,
the same pattern `runbook.md` already uses for the Waltham/Seaport process.
A stage only gets promoted to real code (a future `pipeline/lib/` module) if
a procedure proves itself worth automating beyond what a session can just do
inline — see `cre-radar-generalization-spec.md`'s "Execution model" bullet.

Stage 4 (`04-registry-cross-check.md`) is the one stage with existing
implementation: it points at `massrecords-api/`, the session-assisted
capture tool for masslandrecords.com.

## State

Progress is tracked in three CSVs under `data/pipeline/`, one per entity
type: `parcel-state.csv` (Stages 1–7), `prospect-state.csv` (Stage 8),
`match-state.csv` (Stage 9). Each row carries a `stageN_status` of
`not-started | done | needs-handoff | blocked` per stage, so a session can
report exactly what's ready for a handoff and resume mid-pipeline instead
of restarting. See each CSV's header for the full column set, and
`data/field-dictionary.md`-equivalent documentation to be added there if
this schema stabilizes.

`overall_status`: derived convenience field — `active | needs-handoff |
blocked | dropped | pitchable`. Pitchable means `stage6_pass = yes`
(negative check explicitly clear, not merely `stage6_status = done`, since
`done` also covers the case where an active listing was found) AND
`stage7_activity_pass = yes`, regardless of `stage7_fd_verdict` — matching
the rule that Financial Distress never blocks a pitch. This is the field
Stage 9 actually queries to build its candidate list.

This is a separate state store from `data/leads.csv` — `leads.csv` remains
the historical record of BOS-128 itself (Waltham/Seaport, its own coarser
`status` enum) and isn't retrofitted to the 9-stage schema.

## Sources

Every external source touched by any stage (permit vendors, registries, MA
SOC, MassGIS, negative-check sites) gets one entry in
`data/source-registry.md`, checked before attempting a new source and
updated every time one is touched — see that file and
`cre-radar-generalization-spec.md`'s "Standing requirement" section.

## Signal scoring

Stage 7's Financial Distress track is not redefined here — `07-signal-
scoring.md` references `cre_sop/sop.md` Section 4 as the single source of
truth for the 5 signals, the 2-signal minimum, and the verdict. See that
file for the discipline that governs keeping the two in sync.
