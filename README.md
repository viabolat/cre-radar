# CRE-Radar

Manual demand-validation for a curated off-market industrial & flex lead feed in Greater Boston.

**Current phase:** hand-harvest 10 real Route 128 (Waltham) assets from public registries, each
with a verified transition/distress signal and a resolved human owner, package them as a
"blinded" index, and pitch 5–10 boutique brokers / PE acquisition teams. No automation until
demand is proven.

## Layout

| Path | What it is |
|---|---|
| `runbook.md` | Step-by-step harvest checklist (the process to run) |
| `data/leads.csv` | One row per candidate asset |
| `data/signals.csv` | Intent signals (permits, liens, leases) — many per lead |
| `data/entities.csv` | Owner LLC → human decision-maker resolution |
| `data/field-dictionary.md` | Every column defined + allowed values |
| `data/evidence/<lead_id>/` | Screenshots + downloaded record PDFs (gitignored) |
| `templates/` | Blinded-index entry template, outreach message variants |
| `outreach/tracker.csv` | Every firm touch + response |
| `deliverables/blinded-index-BOS-128.md` | Generated sheet sent to firms |

## How to run

Follow `runbook.md` top to bottom. Each lead advances through
`identified → signal-found → entity-resolved → index-ready`. A lead only qualifies with at
least one signal backed by a real source reference, URL, and evidence file.

## Validation bar

- ≥2 firms request the blinded sheet → demand validated.
- ≥1 firm asks how to unmask owner rows → move to license/pricing conversation.
- 0 of 10 → revisit the signal thesis before building anything.

## Ground rules

- Manual browsing only in this phase. Check each portal's Terms of Use before any automation.
- The blinded index states only what public records show. Locked rows withhold identifiers;
  they never embellish the asset facts around them.
