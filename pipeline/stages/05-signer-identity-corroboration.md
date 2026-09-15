# Stage 5 — Signer identity corroboration

**Source:** registry documents already captured in Stage 4 (primary);
company websites, press, SEC/SOC filings (secondary); LinkedIn (fallback
only, manual).
**Automatable:** mostly — document-to-document matching and the secondary
corroboration sources are; the LinkedIn fallback is a permanent manual
handoff.
**Writes to:** `data/entities.csv` (signer/manager corroboration notes),
`data/pipeline/parcel-state.csv` (`stage5_*`).

## What this stage does

Cross-checks signer names recorded on registry documents (Stage 4) or SOC
Annual Reports (Stage 3) against the resolved owner entity — confirming a
signer is actually who they claim to be in that business capacity (as done
for Fox/Gerrity, Gottlieb/Hill, Provost in BOS-128).

## Corroboration order

1. **Document-to-document signature match (primary).** Check whether Stage
   4 already captured a *second* registry document — a different instrument
   type (mortgage, SNDA, discharge, etc.) — signed by the same name in the
   same capacity for this entity. This was the actual primary corroboration
   method used across WAL-006, WAL-007, and WAL-009 in `leads.csv`: the
   evidence is already captured from Stage 4, costs nothing extra to check,
   and doesn't depend on any external source. Always try this first.
2. **Company website / press / SEC filings (secondary).** If no second
   document exists, or the names don't match cleanly, corroborate via
   company "team"/"about" pages, press mentions, or SEC filings (if a
   public entity is involved).
3. **LinkedIn (fallback only).** Only if neither (1) nor (2) resolves it —
   see the constraint below.

## Why LinkedIn stays a manual handoff, and last in order

Per `cre-radar-generalization-spec.md`'s LinkedIn constraint: LinkedIn's
terms of service prohibit automated scraping. BOS-128 relied on manual
LinkedIn checks repeatedly; that's fine as occasional manual lookups, but
automating it at scale risks account flags/blocks. This is a firm
constraint, not a capability gap. Ordering it last also means the one
manual step in this stage is only reached when the automatable, already-
captured evidence (document match) and the automatable external sources
(website/press/SEC) don't settle it.

## Procedure

1. Identify the signer name(s) from Stage 3 (SOC managers) and/or Stage 4
   (registry document signatories).
2. Attempt document-to-document corroboration: search `data/signals.csv` /
   captured registry records for this entity for a second, differently-
   typed instrument signed by the same name in the same capacity.
3. If that's inconclusive, attempt company website/press/SEC corroboration.
4. If still inconclusive: hand off to the user for a manual LinkedIn check.
5. Record the corroboration outcome and its source in `entities.csv`
   `notes` (or add `linkedin_url`/`linkedin_title` if that lookup was
   done), and set `stage5_status` = `done` once any one of the three
   methods confirms the signer's business-capacity identity, else
   `needs-handoff` with `stage5_note` describing exactly what's
   unconfirmed.

## Handoff

LinkedIn-dependent checks only, always manual — see constraint above, and
only reached as a fallback per the corroboration order.
