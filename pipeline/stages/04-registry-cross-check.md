# Stage 4 — Registry cross-check

**Source:** masslandrecords.com (deeds, mortgages, SNDAs, discharges),
where the district is on that platform.
**Automatable:** no — permanent, by-design handoff.
**Writes to:** `data/signals.csv` (new signal rows for registry documents),
`data/pipeline/parcel-state.csv` (`stage4_*`).

## What this stage does

Cross-checks the resolved owner entity against masslandrecords.com for
deeds, mortgages, SNDAs, discharges, and other recorded instruments. This is
the generalized version of the work `massrecords-api/` already implements
for BOS-128.

## Why this stage is a structural handoff, not a gap

Per `massrecords-api/README.md`: Incapsula hard-blocks scripted/headless
access outright, specifically targeting automation-launched browsers (CDP
flags, `navigator.webdriver`), not IP reputation or headless-ness generally.
Standalone Playwright/requests automation was tested and is a dead end short
of deliberately spoofing the automation fingerprint, which this project does
not do. This is unlike Stage 3's conditional IP-block — here, no automated
path exists at all, by design of the source's bot defenses.

## Procedure

1. Check `data/source-registry.md` for the target parcel's district —
   confirm it's on masslandrecords.com (per `massrecords-api/README.md`'s
   **Districts** table: Suffolk, Middlesex South, Worcester, Dukes
   confirmed; others unconfirmed or on a separate domain).
2. If not on that platform: this stage cannot use `massrecords-api/` at all
   — set `stage4_status` = `blocked`, `stage4_note` = "district not on
   masslandrecords.com; no registered alternative source yet."
3. If on that platform: hand off to the user — browse and search
   masslandrecords.com as a human in real Chrome, using the resolved owner
   entity name and known parcel address. Use `massrecords-api`'s
   Tampermonkey userscripts (`capture.user.js`, `capture-image.user.js`)
   to send the rendered page and any document images to the local FastAPI
   service, per that tool's README.
4. Once documents are captured, query them via `massrecords-api`'s
   `query.py` / `GET /records`, and write a `data/signals.csv` row per
   document per `field-dictionary.md`'s schema (`signal_type` =
   `ownership-transfer`, `new-mortgage`, `mortgage-modification`,
   `financing-agreement`, `tax-lien`, `lis-pendens`, etc. as applicable;
   `source` = `masslandrecords-<district>`; `evidence_file` under `data/
   evidence/_registry/`).
5. Set `stage4_status` = `done`, `stage4_date` = today, once the expected
   set of documents for this parcel has been captured. See ambiguity 5
   (plan Section 4) for the open question of whether partial capture
   across sessions needs a sub-status beyond `stage4_note` free text — not
   yet decided; until it is, log partial progress in `stage4_note`.

## Handoff

Always, when the district qualifies. This is the pipeline's one confirmed
structural (not conditional) manual step.
