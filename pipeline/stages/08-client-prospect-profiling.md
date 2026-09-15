# Stage 8 — Client/prospect profiling

**Source:** company websites, press, SEC filings, MA SOC filings.
**Automatable:** yes, with one confirmation checkpoint — no LinkedIn
automation.
**Writes to:** `data/pipeline/prospect-state.csv` (new/updated rows).

## What this stage does

Independent of Stages 1–7 — can run before, during, or after the property
chain, since it doesn't feed the search itself (per
`cre-radar-generalization-spec.md`'s scope bullet: asset class is filtered
at matching, not narrowed at discovery, and Stage 8 doesn't feed Stage 1/2).
Given a target market, identifies local CRE agencies, infers their
asset-class focus and buyer/broker type, and determines which of them
compete directly for the same deals.

## Procedure

1. Identify local CRE agencies operating in the target market from company
   websites, press coverage, SEC filings (for public entities), and MA SOC
   filings.
2. For each firm, infer: `firm_type` (e.g. developer, institutional buyer,
   tenant-rep broker, investment sales broker), `target_market`,
   `asset_class_focus`, and `source_basis` (which of the above sources the
   inference rests on).
3. **Determine competitive grouping**, once all firms in this run are
   profiled: two firms are grouped together in `competitive_group` only if
   they share the same `firm_type` *and* overlapping `asset_class_focus`/
   `target_market` — i.e. they'd realistically compete for the same deal.
   Firms of different `firm_type` (e.g. a principal buyer and a brokerage)
   are never grouped together, even if their market/asset-class focus
   overlaps — a brokerage doesn't compete with a buyer for the asset itself.
   This is the same analysis already done manually for BOS-128's 7 real
   prospects: Kadima and Berkeley grouped as competing buyers; R.W. Holmes,
   128 CRE, and Stubblebine grouped as competing brokerages (a separate
   group from the buyers); Cresa dropped entirely as not a fit at all
   (handled via `user_confirmed` = `no`, not a `competitive_group` value).
   Assign a free-text `competitive_group` label per cluster (e.g.
   "industrial-buyers-boston"); leave blank if a firm doesn't overlap with
   any other confirmed prospect in this run.
4. Some entries auto-classify cleanly from a single strong source (e.g. a
   firm's own site stating its focus explicitly); others need a manual
   read where sources conflict or are thin, or where competitive grouping
   is ambiguous. Write both kinds to `prospect-state.csv` with
   `stage8_status` = `done` for clean entries and `needs-handoff` for ones
   needing a manual read, `stage8_note` explaining which for the latter.
5. Present the whole list — ready and flagged entries together, not gated
   on the stragglers — as one confirmation checkpoint, including proposed
   `competitive_group` assignments for review. Set `user_confirmed` =
   `yes`, `user_confirmed_date` = today for each row once reviewed;
   entries (and their competitive-group assignment) can be confirmed,
   corrected, or dropped at this checkpoint.
6. Only confirmed rows (`user_confirmed = yes`) are eligible inputs to
   Stage 9, which reads `competitive_group` directly to apply the
   no-repeated-asset-within-a-competing-group rule rather than re-deriving
   it per match.

## Handoff

One confirmation checkpoint per profiling run (not per-entry) — see step 5.
No LinkedIn automation is used for this stage; if a classification would
otherwise depend on LinkedIn, that entry is flagged for manual read instead
(step 4), consistent with the LinkedIn constraint documented for Stage 5.
