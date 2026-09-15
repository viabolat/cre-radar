# Stage 9 — Match and draft

**Source:** `data/pipeline/parcel-state.csv` (`overall_status`),
`data/pipeline/prospect-state.csv` (confirmed rows), Stage 7's Financial
Distress track (factual record only, never its verdict).
**Automatable:** yes, up to producing a draft; the draft itself is always
reviewed before it leaves the pipeline — see Handoff.
**Writes to:** `data/pipeline/parcel-state.csv` (`asset_class_final`),
`data/pipeline/match-state.csv` (new rows), `deliverables/` and/or
`outreach/` (draft artifacts, per existing templates).

## What this stage does

The only place asset class and prospect focus meet. Stage 1 scans
unfiltered and Stage 8 profiles prospects independently of the parcel
chain — this stage is where a parcel's actual asset class (observed, not
just `asset_class_hint`) is checked against prospects' `asset_class_focus`,
and where the Activity-track pitch gate and competitive-group rule are
applied, before anything is drafted.

## Candidate list — gating

1. Query `parcel-state.csv` for `overall_status = pitchable`. Per
   `pipeline/README.md`'s definition, this already means `stage6_pass =
   yes` and `stage7_activity_pass = yes` — **this is the only gate.** A
   parcel with `stage7_fd_verdict = do-not-advance` is still eligible if
   `overall_status = pitchable`; Financial Distress never blocks a pitch,
   per the spec's Stage 9 rule (`cre-radar-generalization-spec.md` lines
   134-137: "Activity is the only gate — a property is pitched only if it
   passes the Activity Signal track... Financial Distress never blocks a
   pitch, regardless of its verdict.").
2. Non-pitchable parcels (`needs-handoff`, `blocked`, `dropped`, or
   `active` but not yet `pitchable`) are not considered — no partial or
   speculative matching against an incomplete parcel.

## Determining final asset class

3. For each pitchable parcel, determine its actual asset class from
   Stages 1–7's accumulated observations (assessor use code, permit
   description, any resolved use from Stage 2/4/5 evidence) — not just
   carrying forward Stage 1's `asset_class_hint` unchanged. Write the
   result to `parcel-state.csv`'s `asset_class_final` field (new field,
   separate from `asset_class_hint`), so a resumed or re-run Stage 9 reads
   the persisted determination instead of re-deriving it and risking a
   different answer on a second pass. This is the filtering step
   referenced in the spec's scope bullet: asset class was never fixed at
   discovery, and this is where it's finally fixed.

## Matching against prospects

4. Query `prospect-state.csv` for rows with `user_confirmed = yes`.
5. For each pitchable parcel, match against prospects whose
   `asset_class_focus` includes the parcel's `asset_class_final` and whose
   `target_market` includes the parcel's municipality/submarket.
6. **Competitive-group rule:** within a single `competitive_group`, don't
   pitch the same parcel to more than one prospect in that group — pick the
   single best-fit prospect in the group for that parcel (by closest
   `asset_class_focus`/`target_market` match; if genuinely tied, flag for a
   user call rather than guessing) rather than sending the same deal to
   direct competitors. Prospects with no `competitive_group` (or in
   different groups) have no such restriction against each other.
7. Write one `match-state.csv` row per resulting parcel × prospect pairing:
   `match_id`, `parcel_id`, `prospect_id` (matched using the parcel's
   persisted `asset_class_final`, not a re-derived value), `competitive_group`
   (copied from the prospect row, for audit), `stage9_status` =
   `not-started`.

## Drafting

8. For each match row, draft using the existing templates
   (`templates/blinded-index-entry.md` for the client-facing index entry,
   `templates/outreach-message.md` for the feeler email) — same format
   BOS-128 already produces, now parameterized by this match's parcel and
   prospect instead of hardcoded to Waltham.
9. **Financial Distress handling in the draft:** never surface
   `stage7_fd_verdict` or the Advance/Advance-with-caveat/DO NOT ADVANCE
   language anywhere client-facing. Where Track 1 found dated, verifiable
   facts (e.g. a recorded lien, a mortgage modification, a court filing),
   those facts may appear in the draft as plain supporting detail — the
   same way BOS-128's existing entries cite dated events — with no
   editorializing about what they imply for the owner's financial state.
   If Track 1 produced no evaluable signals (all `not-evaluable`) or found
   nothing, the draft simply omits any Financial Distress content; this is
   never treated as a gap to flag.
10. Set `stage9_status` = `done`, `stage9_date` = today, `draft_ref` =
    path to the produced draft artifact, once drafted. If drafting can't
    complete (e.g. missing a required field from an earlier stage), set
    `stage9_status` = `needs-handoff` with `stage9_note` describing what's
    missing.

## Handoff

Draft review before anything is sent externally — there is no rule in
`cre-radar-generalization-spec.md` naming an automated no-send gate; this
is the same manual-review practice BOS-128's existing outreach workflow
already follows (`outreach/tracker.csv`: drafts are tracked and reviewed
there before going out), applied here rather than a new spec-level
constraint. The competitive-group tie case in step 6 is also a manual
handoff when it occurs, flagged rather than auto-resolved.
