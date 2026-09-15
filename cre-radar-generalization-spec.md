# CRE-Radar — Unified Architecture Spec (Draft, Pre-Validation)

## Goal
One system, not a collection of scripts. The BOS-128 logic — permit search,
registry cross-check, owner resolution, negative check, client profiling,
outreach drafting — becomes a single pipeline parameterized by **location**
and **asset class**, instead of hardcoded to Waltham/industrial. Feed it
"South Boston, office" and it runs the same architecture BOS-128 already
proved out, end to end, without you having to know which script does which
piece six months from now.

## Confirmed scope decisions
- **Geography: Massachusetts only, for now.** No multi-state build until MA is
  validated. This also matches a real technical constraint: the massrecords-api
  tool only works on `masslandrecords.com` districts (Suffolk, Middlesex South,
  Worcester, Dukes confirmed; several others unconfirmed or on a separate
  domain — see existing README). Expanding geography later is partly a research
  task (confirm new districts) and partly new registry integration work for
  districts not on that platform.
- **Execution model: semi-automated with resumable handoff.** Code (Claude Code
  CLI + existing scripts) does everything programmatically reachable. Anything
  that can't be reached programmatically hands off to you, then resumes from
  the same point once you've completed the manual step — no restarting the
  whole pipeline.
- **Asset class: not fixed at discovery, filtered at matching.** Parcel
  discovery (Stage 1) scans a target town without locking to one asset
  class up front. Client profiling (Stage 8) and Financial/Activity
  scoring (Stage 7) run independently of each other. A property is only
  ever pitched to clients whose known focus fits it — the filtering
  happens once, at Stage 9, not by narrowing the search earlier.

## One pipeline, in the order the .md records actually show it running

BOS-128's real sequence was property-first, all the way through verification,
with client matching applied afterward. This spec follows that order:
property discovery and verification run without needing client data first;
client profiling runs independently and is used purely as a **matching
filter at the end** — so a verified industrial asset only ever gets pitched
to clients whose known focus is industrial, never to a tenant-rep firm or an
office-only buyer.

**Stage 1 — Parcel discovery**
MassGIS Property Tax Parcels FeatureServer query, scoped to the target
town/neighborhood. Not asset-class-locked at the search stage — scans
whatever's there, since asset class filtering happens later at matching, not
at discovery. Automatable.

**Stage 2 — Permit signal search**
Municipal permit portal for the target town. No single statewide system
exists — every town runs its own, falling into categories discovered so
far (each new town gets checked once and the result cached, per the
documentation requirement below, not rediscovered every run):

- **Hard-blocked, permanent manual handoff** — same category as the
  registry: nothing programmatic works, ever. (masslandrecords.com is the
  confirmed example; no permit vendor has hit this yet, but a town could.)
- **Login-gated, plausibly automatable with setup** — e.g. **Citizenserve**
  (confirmed on Revere, Brockton, Medway): searchable once an account
  exists, but requires registering and holding credentials. Treat this as
  its own handoff type: the *account setup* is a one-time manual step per
  town/vendor, and if credentials can be safely stored and reused,
  subsequent searches may be automatable — this needs to actually be
  tried before assuming either way.
- **Public but JS-rendered** — e.g. **PermitEyes** (confirmed on Falmouth,
  Chelmsford, Mashpee, North Reading, and shared across all of Berkshire
  County under one login-free portal): no login wall, and the field
  structure is fully public (Owner, Applicant, Parcel No., Street,
  Description, Permit Number, Issue Date), but data loads via JavaScript
  after page render — a plain fetch returns empty tables. Also has a
  visible "Export to Excel" function, suggesting a rendered-browser
  interaction (Claude in Chrome triggers search + export, reads the
  result) or reverse-engineering the underlying AJAX call are both worth
  trying before treating this as a handoff.
- **Static/parseable** — e.g. Waltham's PDF permit reports, or any town
  with a queryable structured database. Automatable outright, or a parse
  step, not a handoff.

The vendor a given town uses is unknown until checked — this is itself a
lookup Stage 2 performs once per new town and records permanently (see
documentation requirement).

**Stage 3 — Owner entity resolution**
MA Secretary of the Commonwealth, Corporations Division search. Automatable
via web search/fetch.

**Stage 4 — Registry cross-check** (deeds, mortgages, SNDAs)
Via masslandrecords.com, where the district is on that platform. This is a
**permanent, by-design handoff** — Incapsula blocks headless/automated
access outright, and the session-assisted userscript approach (you browse,
the script captures) is the only working method. Not a gap to close later;
a structural constraint of the source.

**Stage 5 — Signer identity corroboration**
Cross-check signer names against the resolved entity (as done for Fox/
Gerrity, Gottlieb/Hill, Provost). LinkedIn-dependent checks stay a manual
handoff — see constraint below.

**Stage 6 — Negative check**
LoopNet/CBRE/Cushman/Newmark listing search, to rule out signals that are
already public market activity. Automatable via search; borderline cases
(like WAL-008's stale Showcase.com listing) need your judgment call. Feeds
the Activity track's hard gate below.

**Stage 7 — Two independent tracks, not one merged score**

Every parcel gets scored by both tracks, independently. Neither track's
internal logic is softened to accommodate the other.

- **Financial Distress track** — cre_sop's existing 5 signals (tax
  delinquency, ownership/lien change with 12-18mo recency, secured debt
  filing, legal distress, institutional distress), its 2-signal minimum,
  its Advance / Advance-with-caveat / DO NOT ADVANCE verdict. This verdict
  is internal only — never shown to the client (see Stage 9).
- **Activity Signal track** — BOS-128's pattern: Stage 6's negative check
  clear (hard gate), owner not a large diversified public REIT/portfolio
  operator, at least one dated recent event (permit/financing/ownership-
  structure change/lease change/assembly), the event tied to a plausible
  reason it might matter. **This is a starting heuristic, not a finalized
  rule** — treat it the way cre_sop treated Signal 2 before v12: apply it,
  watch what it actually filters in and out across real runs, and correct
  it the first time a real case doesn't fit, rather than trying to perfect
  it on paper first.

**Stage 8 — Client/prospect profiling (automated, gated by one review)**
Independent of Stages 1–7 — can run before, during, or after the property
chain, since it doesn't feed the search itself. Given a target market,
identify local CRE agencies and infer their asset-class focus and
buyer/broker type — automatically, from company websites, press, SEC
filings, and MA SOC filings (no LinkedIn automation — see constraint below).
Some entries auto-classify cleanly, some need a manual read; you get one
confirmation checkpoint showing the whole list — ready and flagged entries
together, not gated on the stragglers — before this feeds Stage 9.

**Stage 9 — Match and draft**
Activity is the only gate — a property is pitched only if it passes the
Activity track (Stage 6 clear, Stage 7's Activity criteria met). Financial
Distress never blocks a pitch, regardless of its verdict.

For a property that's being pitched, Financial Distress data is included
as **client-facing supporting facts, not a verdict**: dated, factual
statements only ("recorded 2016, resolved 2019"), no characterization or
inference about what it means, no advance/do-not-advance label surfaced to
the client — matching cre_sop's own existing guiding principle ("documents
recorded facts... and nothing else. It never explains, predicts, or
characterizes.").

Then: filter Stage 8's prospect list to clients whose profiled asset-class
focus and buyer/broker type fit, apply the competitive grouping (no
repeated asset within a competing buyer group), and draft outreach in the
proven format — blinded activity entries, hedged signal language, locked
owner/contact pending reply, financial facts included as supporting
context once unlocked.

## Resumable state requirement
Every parcel and every prospect carries a per-stage status (done /
needs-handoff / blocked) in one tracked state, the same shape as the
existing `leads.csv` status field, just extended across all 9 stages instead
of a single final status. This is what lets Claude Code report "12 parcels
found, 4 ready for your registry capture pass, 8 still mid-pipeline" and
resume exactly where a handoff left off — one system tracking one run,
never several disconnected scripts you'd have to reassemble by memory.

## Constraint: no automated LinkedIn scraping
LinkedIn's terms of service prohibit automated scraping, and BOS-128 relied
on manual LinkedIn checks repeatedly (Fox/Gerrity, Gottlieb/Hill, Provost) to
confirm signer identity. That's fine as occasional manual lookups;
automating it at scale risks account flags/blocks. Stage 8 relies on sources
safe to automate — company sites, press, SEC filings, SOC filings — and
routes any LinkedIn-dependent identity check (Stage 5) to a manual handoff
instead.

## Explicitly not in scope yet
- Any geography outside Massachusetts
- Any registry platform other than masslandrecords.com's districts
- Full autonomy with no handoff steps — Stage 4's Incapsula block makes this
  structurally impossible, not just a current limitation

## Standing requirement: every source gets documented, permanently

This is not optional and not scoped to permit portals specifically — it
applies to every external source the pipeline touches across all 9 stages:
masslandrecords.com districts, municipal permit vendors, MA SOC search,
MassGIS, negative-check sources (LoopNet/CBRE/etc.), anything new
encountered later.

**The failure mode this prevents:** without a persistent record, a future
session (yours or Claude Code's) re-discovers the same thing from scratch —
re-tries a fetch against Citizenserve without knowing it needs login,
re-hits PermitEyes expecting static HTML, re-learns that masslandrecords.com
blocks automation. That's wasted time repeating "let's try this" loops that
already have a known answer. The existing massrecords-api README already
does this correctly for registry districts (a **Districts** table: confirmed
working, confirmed wrong domain, unconfirmed) — this requirement extends
that same discipline to every other source category.

**What Claude Code CLI must maintain, updated every time a new
town/vendor/source is touched:**

A site/source registry (e.g. `data/source-registry.md`, one entry per
distinct source) recording, at minimum:
- **Source name and URL** (e.g. "Citizenserve — Revere",
  "PermitEyes — Falmouth", "masslandrecords.com — Suffolk")
- **Access category** — one of: hard-blocked / login-gated / public-but-
  JS-rendered / static-parseable / open-API — using the categories
  established for permit vendors above, extended as new categories emerge
- **What was tried** — the specific approach attempted (plain fetch,
  authenticated request, browser automation, session-assisted capture,
  etc.), not just the conclusion
- **What worked / what didn't**, in enough detail that a future session
  doesn't repeat a failed approach — e.g. "plain HTTP fetch returns empty
  table (JS-rendered); Export-to-Excel button not yet tested" is a usable
  note, "doesn't work" is not
- **Current recommended approach**, if one exists yet, and **open
  questions**, if it doesn't
- **Date last verified** — vendors change platforms, towns migrate
  systems; a stale confirmation should be visibly stale, not silently
  trusted

This registry is read before attempting a new source, not just written
after — the pipeline checks it first so a town already characterized
(e.g. "Revere = Citizenserve, login-gated, untested automation") isn't
re-investigated from zero on a later run.
