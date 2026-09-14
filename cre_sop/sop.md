# CRE-SOP Standard Operating Procedure (v12)
**Scope Lock: Suffolk County / City of Boston, MA — Office Asset Class**
**Agents: Claude Code CLI + Antigravity CLI (`agy`)**
**Status: SOURCE OF TRUTH — do not deviate from listed tools/sources without explicit user approval**
**Revision note (v12):** The first fully-completed Seaport run (5 candidates, Steps 1-8) returned `DO NOT ADVANCE` across the board — and every one of the 5 cleared Signal 2 (ownership/lien change) regardless of whether the underlying instrument was current or a decade old. That means Signal 2, as written through v11, doesn't discriminate: any property with any deed/mortgage/lien history ever satisfies it, which is every commercial property that has ever existed. This version tightens Signal 2 to require recency. Also corrects Source #6's Housing Court division for Boston (Eastern, not Metro South — a mistake made and caught mid-run) and documents Source #1's confirmed manual-only status this session. See changelog at bottom.

**Guiding principle (unchanged):** This SOP documents recorded facts (liens, tax status, case existence, ownership changes) and nothing else. It never explains, predicts, or characterizes what a legal filing means procedurally or what happens next.

**Guiding principle (unchanged):** The agent does the work. The human is invoked only when automated retrieval genuinely fails — and when invoked, the human's job is narrow and mechanical: follow exact instructions, retrieve one specific piece of data, paste it back. The human is never asked to interpret, judge, or research on the SOP's behalf.

**Guiding principle (unchanged):** Avenue enumeration serves the workflow, not the other way around. Once a confirmed, working avenue exists for a source, do not keep chasing additional theoretical avenues to fully catalog them.

**Guiding principle (unchanged):** Research spent is never thrown away. Every property that reaches Signal Scoring — regardless of outcome — is permanently recorded with why it was pulled and what it did or didn't turn up. A `DO NOT ADVANCE` today is still useful information tomorrow.

---

## 0. WHY THIS SCOPE (do not re-litigate without new evidence)

Office is the selected asset class because Boston's office market currently shows genuine submarket dispersion — some pockets (e.g. Back Bay, downtown core) recovering while others (e.g. Seaport, some suburban clusters) continue to soften. That dispersion is what makes distress signals identifiable and clustered rather than uniform noise across the whole city.

This is a directional, qualitative rationale, not a fixed data point. **Before relying on this section to justify continued scope, re-verify the current vacancy/submarket trend using Section 2 sources or current market reporting** — vacancy figures move quarter to quarter and any specific percentage written here today will be stale by the time this SOP is next read. Do not cite a hard vacancy number from this section in a client-facing report.

**Citation discipline for market figures:** Overall Boston office vacancy figures diverge significantly by publisher because of methodology differences (CBD-only vs. metro-wide, direct vs. total availability, Class A vs. blended all-class). If a vacancy or submarket figure is ever used in a client-facing report (Section 6, Part 3), it must be attributed to a specific named report and its specific scope. Do not average or reconcile competing brokerage numbers yourself.

Do not expand to retail, industrial, or multifamily until this scope has produced at least one validated report (see Section 8 gate).

---

## 1. OPERATING RULES (BINDING ON BOTH AGENTS)

1. **One step at a time.** Never output more than one numbered step from Section 5 in a single response. Complete the step, present the output, then STOP.
2. **No auto-advance.** After every step, end your response with exactly: `AWAITING CONFIRMATION — reply "confirmed" to proceed to Step [N+1], or "revise" to redo this step.`
3. **No proceeding on silence or ambiguity.** If the user's reply doesn't clearly confirm, ask a clarifying question instead of guessing intent.
4. **No fabricated data.** Every factual claim about a property must cite a specific source from Section 2, with a URL, date accessed, and document/parcel ID where applicable. If a claim cannot be sourced from Section 2, mark it `UNVERIFIED` and do not include it in a client-facing report.
5. **No financial or legal modeling beyond what's filed.** Do not calculate or assert DSCR, cap rate, or refinance probability, and do not explain, predict, or characterize what a legal filing means procedurally or what a court process requires. Describe documented facts only — never the mechanism behind them.
6. **Confidence threshold — flattened.** No percentage scoring. Three outcomes only: **Advance** (2+ signals, clean matches), **Advance with caveat** (2+ signals, one relies on a close-variant name match), **DO NOT ADVANCE** (fewer than 2 signals, or a direct contradiction between sources).
7. **No scope creep.** Do not search asset classes, counties, or data sources outside Section 2/Section 0 without the user explicitly typing `expand scope`.
8. **Verify sources before relying on them, every session, no exceptions.** Every URL in Section 2 should be click-tested at the start of a new work session. Government and registry sites restructure without notice, and a prior confirmation is not evidence about today's state. Do not record a dated "verified as of [date]" claim in Section 2 — a source is either checked this session, or it isn't. Any avenue marked `UNCONFIRMED` gets tested at first genuine need, not assumed — but once a confirmed, sufficient avenue exists for a source, do not spend further effort verifying other theoretical avenues just to complete the catalog.
9. **Retrieval Protocol — agent-first, avenue-exhaustive, human as last resort.** For every data pull in Steps 1–5:
   - **Enumerate the avenues before starting.** Identify every genuinely distinct automated method available for a source before the first attempt.
   - **Try listed avenues until one works, not all of them for completeness.** Stop once an avenue succeeds. Only move to the next when the current one has actually failed.
   - **Do not retry an avenue that has already failed in the same way.**
   - **An `UNCONFIRMED` avenue gets tested only when actually needed.** A metadata-only response or a 404 downgrades it; move on.
   - **Connectivity avenue, `UNCONFIRMED`:** VPN/proxy routing is a legitimate avenue only for genuine rate-limiting or geographic-restriction failures — not confirmed to exist in either CLI's toolset, and explicitly excluded from use against a bot-detection gate, which is a structural block, not a connectivity problem.
   - **Fall back to manual only once every relevant avenue is exhausted.** Produce exact manual instructions — the precise URL, the exact field/menu/tab, the exact search term, and exactly what to copy. Instructions must assume no professional background in real estate, law, or GIS tools — write for a first-time user, not a professional shortcut: name the site in plain language *and* give the exact URL together, never one without the other.
   - **Wait for pasted data.** Do not proceed, guess, or fabricate a placeholder.
   - **Log which avenue succeeded (or which were tried before manual fallback)** in the evidence log.
   - This protocol governs data-fetching only. It does not change Rule 1 or Rule 2.
10. **Persistent record — nothing researched is discarded.** Every property that reaches Step 6 (Signal Scoring) in any run gets an entry in the persistent candidate log (Section 7), regardless of outcome. Before researching a newly pulled parcel in Step 1 of any run, check whether it already has an entry — if so, follow Section 7's re-check procedure rather than starting from scratch.
11. **Before escalating a stale-sounding report as an open question, check for a fresher one first.** If a source describes a property as "in progress," "under agreement," or similar (a sale rumored, not confirmed), search once for a more recent follow-up before treating it as ambiguous enough to require the operator's judgment call.
12. **Persist every completed step's output to a real file in the project root — never leave a run's working state only in `/tmp` or only in the conversation.** Scratch work during a step can live in `/tmp`, but the moment a step in Section 5 is complete, its full output must be written to a durable file before moving to the next step. State the file path in the step's output.
13. **A `DO NOT ADVANCE` result across an entire candidate pool is a legitimate, useful outcome — not itself grounds to loosen a signal definition.** Per Section 8, only revisit trigger definitions after zero survivors across two different submarkets. However, if a specific signal is found to be non-discriminating for a documentable, structural reason (as happened with Signal 2 in the first live run — see Section 4), that signal's definition should be corrected regardless of how many submarkets have been tried, since a non-discriminating signal produces no valid information about any candidate, in any submarket.

---

## 2. APPROVED FREE DATA SOURCES (Suffolk County / Boston — Office)

| # | Source | Use | URL | Known Avenues |
|---|---|---|---|---|
| 1 | Massachusetts Land Records | Deeds, mortgages, liens, ownership transfers (Suffolk District) | masslandrecords.com; successor/mirror `massrods.com/suffolk` found via suffolkdeeds.com's redirect | **No working automated avenue confirmed this session (2026-09-12)** — direct fetch and WebFetch both hit an Incapsula redirect loop on masslandrecords.com; the massrods.com/suffolk mirror returns a Cloudflare JS challenge. All 3 distinct paths tried, all blocked. Manual-only via the registry's Name Search web interface until re-verified. Re-test at the start of each new session per Rule 8 — a block today doesn't mean it's permanent, but don't assume it's resolved either. Manual retrieval may be captured via massrecords-api's Tampermonkey scripts (browse-and-click, not automated navigation) instead of raw paste, for structured/queryable storage — still counts as the manual avenue for Rule 9 purposes |
| 2 | Boston Property Lookup (Assessing Online) | Current assessed value, ownership, tax status per parcel | properties.boston.gov (client-rendered SPA; live backend confirmed at `us-central1-assessing-properties-prod.cloudfunctions.net`, callable functions include `fetchPropertyDetailsByParcelId` and the bulk `fetchPropertySummariesByParcelIds`) | Primary avenue: direct fetch against the confirmed backend Cloud Functions endpoint, parcel-ID keyed. Note: this source's schema carries no payment/delinquency/tax-title field — only assessed value, current-FY billed tax composition, ownership, and exemption/fine flags (e.g., `fine38d`, the MGL c.59 §38D non-filing penalty). Tax delinquency (Signal 1) may not be checkable through this source — see open item, Section 8 |
| 3 | Boston Assessing Parcel Data (ArcGIS FeatureServer) | Bulk/programmatic parcel + assessment data, including LU-code filtering | `gisportal.boston.gov/arcgis/rest/services/Assessing/ASG_PROPERTY_ASSESSMENT_PARCEL_JOIN_FY25/FeatureServer/0` — confirmed live and current (FY25 supersedes FY24; confirm at each new session whether a newer fiscal year exists); fields include `LU`, `LU_DESC`, `OWNER`, `FULL_ADDRESS`, `TOTAL_VALUE`, `GROSS_TAX`. Same delinquency-field gap as Source #2 | Primary avenue: direct query against this FeatureServer's `/query` endpoint, filtering by `LU`/`LU_DESC`. Secondary avenue: the Analyze Boston per-fiscal-year CSV download at data.boston.gov, filtered locally if the FeatureServer is unavailable |
| 4 | MassGIS Property Tax Parcels | Boston-specific parcel geometry and IDs (fallback only) | mass.gov/info-details/massgis-data-property-tax-parcels | Fallback only — not normally invoked (see note) |
| 5 | MA Secretary of the Commonwealth — UCC Search | UCC-1 filings naming an owner/entity as debtor | corp.sec.state.ma.us/CorpWeb/UCCSearch/UCCSearch.aspx | Direct form-submission fetch as the primary avenue when reachable; confirmed bot-gated (Incapsula redirect loop) in the same session Source #1 was also blocked — treat as likely manual-only alongside Source #1 until re-verified. **Coverage gap:** this source does not index UCC fixture filings recorded at the Registry of Deeds (Source #1) — a "none found" here does not rule out recorded UCC activity; Source #1 is a necessary cross-check for real-estate-collateral UCC filings |
| 6 | MassCourts (eCourts Public Portal / eAccess) | Civil case filings — name-searchable Trial Court dockets | masscourts.org | One known avenue, and it's blocked: gated behind an "I'm not a robot" checkbox before the search form loads. One attempt confirming the gate is sufficient to move to manual. This gate is not a connectivity problem — do not attempt the VPN/proxy avenue against this source. **Division correction (v12):** for Boston/Suffolk County, the correct Housing Court division is **Eastern Housing Court** — not Metro South, which covers Norfolk County towns and the Brockton area. This was searched incorrectly once mid-run before being caught; use Eastern Housing Court for any Boston-area Housing Court check going forward |
| 7 | SEC EDGAR Full-Text Search | Special servicing transfers, impairments, REIT disclosures (institutionally-owned buildings only) | efts.sec.gov / sec.gov/edgar/search | `efts.sec.gov` documented full-text-search API (primary avenue, confirmed working); `sec.gov/edgar/search` web interface as a second avenue if the API call fails. **Note:** Signal 5 requires specifically 8-K/10-K/10-Q language — a Form D or other filing type naming the entity does not satisfy Signal 5, even though it may still be useful corroborating context for institutional-ownership identification generally |
| 8 | LoopNet | Negative check — confirms whether a property is already publicly listed | loopnet.com | Direct fetch attempt; if blocked (including bot-detection challenges like Akamai/Cloudflare 403s — treat these as the avenue having failed, not something to retry per-candidate), the address-based web-search fallback (see note) counts as the second avenue |
| 9 | Crexi | Same purpose as Source #8 | crexi.com | Same avenues as Source #8 |

**Note on Source #2 (v11):** Confirmed to be a client-rendered app with a real backend API discovered by inspecting the frontend's own JavaScript bundle. Field labels/descriptions were also confirmed this way (e.g., `fine38d`'s title and description came from the bundle itself, not guessed).

**Note on Source #3:** FY24 was the version first verified; the first live run confirmed FY25 supersedes it. Confirm at the start of each new session whether a further fiscal year exists.

**Note on Source #4:** MassGIS's own parcel download table routes Boston to the city's open data portal (Source #3) rather than a MassGIS shapefile — use Source #3 as the primary parcel dataset for Boston, and treat Source #4 as a fallback only.

**Note on Source #7 (institutional-ownership heuristic and SPV addendum):** Before spending time on this source, check whether the owner entity name (from Step 4) matches, or clearly appears to be a subsidiary of, an identifiably publicly traded company. If not, skip Source #7 and note "not institutionally owned — skipped." SPV addendum: if Step 4's land-records pull surfaces a different corporate entity as lender, guarantor, or affiliated signer, run the heuristic against that name too, and note which name (if any) produced a match.

**Note on Sources #8/#9 (this is a disqualifying check, not a signal):** These do not add evidence toward the 2-signal minimum in Section 4 — they exist solely to reject candidates that are already visible to every other broker as a current opportunity. What counts as disqualifying:
- **Discards the candidate:** an active, currently-open whole-property sale listing; an active, currently-open listing marketing the entire building as vacant/available for lease; a confirmed in-progress sale process reported by a source dated close to the current session (per Rule 11, check for a fresher follow-up before treating a rumor-stage report as confirmed either way).
- **Does NOT discard the candidate:** ordinary for-lease marketing of individual suites within an otherwise-occupied, multi-tenant building; a completed, closed historical sale (however recent) — the deal is done, the building has a settled owner, and that owner is exactly who Steps 3-5 need to research.
Fallback: if direct site fetch fails, the address-based web search ("exact address" + "for sale OR for lease") is the second avenue, and only after that fails does manual fallback apply.

**Noise to exclude:** Do not use MassGIS data for other towns, do not use residential-only listing sites (Zillow/Redfin-type), do not use any paid aggregator (Reonomy, CoStar, Trepp, ATTOM) regardless of free-trial availability.

---

## 3. CANDIDATE POOL SIZE CAP AND DEFINITION

Step 1 must not return more than **25–30 parcels per run**. Source #3's FeatureServer supports SQL-style filtering directly — apply LU-code and submarket-boundary filters at query time; narrow with an additional filter (assessed value range, building age via `YR_BUILT`, specific streets/blocks) if the raw match exceeds the cap. **State which narrowing criterion was chosen and why, including what kind of candidate profile that criterion favors or excludes.**

**Pre-Step-1 requirement:** Before running Step 1, lock and state in the Step 1 output:
1. **Which `LU`/`LU_DESC` value(s) count as "office"** for this run.
2. **The exact geographic boundary of the named submarket**, or the concrete proxy used if no direct boundary field exists — state the proxy and its known imprecision openly.
3. **Check the persistent candidate log (Section 7) for any pulled parcel that already has an entry** — for those, follow the re-check procedure in Section 7 rather than treating them as new.
4. **Cross-source classification conflicts found later in a run** should be resolved in favor of whichever source's data is more current/directly authoritative for that field, and the affected parcel removed from the pool retroactively as an out-of-scope correction — not logged as a later step's finding.

---

## 4. TRIGGER SIGNAL DEFINITIONS (only these count as valid signals)

| Signal | Source(s) required | Minimum evidence |
|---|---|---|
| Tax delinquency | Source #2 or #3 | Delinquent status shown directly on parcel record — **see open item, Section 8: neither source currently exposes this field; this signal may be unusable through free sources pending further research** |
| Ownership/lien change | Source #1 | **Recorded instrument with doc number and date, dated within the trailing 12–18 months of the current session (v12 — tightened from "any instrument, any date").** An instrument older than 18 months does not satisfy this signal on its own, even if it appears in the candidate's document history — record it in the evidence log as historical context, but it does not count toward the 2-signal minimum |
| Secured debt filing | Source #5 | Active UCC-1 naming the property owner/entity |
| Legal distress | Source #6 | An **open** civil case involving the owner entity — existence and case number only. A resolved/dismissed/settled case does not satisfy this signal, regardless of how recently it closed — it existed, and it is now resolved, which is a different fact worth recording but not this signal |
| Institutional distress | Source #7 | Filed **8-K/10-K/10-Q** language specifically naming the property, its owning entity, or a lender/guarantor entity surfaced in Step 4 (see Section 2 SPV addendum). A Form D or other filing type does not satisfy this signal even if it confirms an institutional connection generally |

A candidate advances only if **2 or more** signals are independently confirmed. One signal alone = `DO NOT ADVANCE`.

**Why Signal 2 was tightened (v12):** the first fully-completed run found all 5 candidates in a pool satisfied Signal 2 via some recorded instrument, regardless of age — including instruments from 2016-2022 with no subsequent activity. A signal every property in a pool clears provides no discriminating information. Requiring recency (12-18 months, matching the window Waltham's parallel harvest process already uses successfully) makes this signal actually mean something: an instrument recorded recently is far more likely to reflect a live situation than one from years ago with nothing since.

**Data currency caveat:** Source #2/#3's tax-related fields are assessment/billing records, not a live payments ledger — they do not by themselves confirm or rule out delinquency. Note the access date on every check so staleness is auditable later.

---

## 5. STEP-BY-STEP WORKFLOW (execute strictly in order)

**Step 1 — Candidate Pool Definition**
Check the persistent log (Section 7) for any previously-seen parcels before treating the pull as entirely new. Query Source #3's FeatureServer directly, filtering by `LU`/`LU_DESC` and submarket boundary. Apply the pool cap, stating the narrowing criterion and what ownership/candidate profile it favors. Output: parcel IDs/addresses, LU values used, boundary/proxy used, narrowing filter and its known bias, which avenue succeeded, and which (if any) parcels already had a prior log entry. **Persist this output to a file in the project root per Rule 12.**

**Step 2 — Negative Check: Already Listed?**
Try Source #8 (LoopNet) and Source #9 (Crexi) direct fetch first, then the address-based web-search avenue if that fails. Apply the Section 2 discard criteria exactly. Per Rule 11, check for a fresher follow-up before flagging an in-progress-sounding report as an open question. Discard immediately any parcel meeting the actual discard criteria — log as rejected with a one-line reason (this rejection also gets a persistent log entry per Section 7). Output: filtered list of parcels with no active listing found. **Persist per Rule 12.**

**Step 3 — First-Pass Screen**
Try Source #2's known avenues for tax status. If a cross-source classification conflict surfaces for any parcel, resolve it per Section 3, requirement 4. Output: filtered list showing any irregular finding, with access date and avenue used. Discard the rest with a one-line reason logged. **Persist per Rule 12.**

**Step 4 — Ownership and Lien Check**
Try Source #1 and Source #5's known avenues. Note the date of every recorded instrument found — Step 6 will need to know which ones fall within the trailing 12-18 months for Signal 2 per Section 4's tightened definition. Note any lender, guarantor, or affiliated entity named on a recorded instrument — feeds the Source #7 SPV check in Step 5. Output: per-property findings with document numbers, dates, avenue used, or "none found." **Persist per Rule 12.**

**Step 5 — Legal and Institutional Check**
Source #6: confirm the gate once, then go straight to exact manual instructions, checking both Superior Court Civil and Eastern Housing Court (per the Section 2 division correction) for every candidate. For Source #7, apply the institutional-ownership heuristic (including the SPV addendum) before deciding whether to check it, and confirm any hit is specifically 8-K/10-K/10-Q per Section 4's tightened definition — a Form D or similar does not satisfy the signal. Output: per-property findings, avenue(s) used, case numbers/dates or "none found" (noting open vs. resolved status for any case found), and whether any match relied on a close-variant name. **Persist per Rule 12.**

**Step 6 — Signal Scoring**
Apply the Section 4 table exactly, including the tightened Signal 2 recency requirement and the Signal 4/5 specificity requirements. Output: Advance / Advance with caveat / DO NOT ADVANCE per property, with a one-line reason. **Every property scored here — regardless of outcome — gets appended to the persistent candidate log (Section 7) before proceeding**, in addition to the Rule 12 step-state file. If every candidate in a pool returns `DO NOT ADVANCE`, that is a complete, valid result — report it as such rather than treating it as an incomplete run.

**Step 7 — Evidence Log Compilation**
For every property that passed Step 6 (Advance or Advance with caveat only), compile a full evidence log per Section 6 format for the client-facing report. If no properties passed, state that plainly and stop — there is nothing to compile. **Persist per Rule 12.**

**Step 8 — Report Drafting**
Using only the evidence log from Step 7, draft the 5-part report (Section 6). If Step 7's log is empty, there is nothing to draft — say so and stop.

**Step 9 — Final QA Pass**
Check the drafted report against Section 1 rules 4–6 and 9. If no report was drafted (empty result), there is nothing to QA — say so and stop.

---

## 6. REPORT FORMAT (only after Step 9 passes — client-facing, Advance/Advance-with-caveat properties only)

```
[PROPERTY IDENTIFIER — Address, Parcel ID]

1. PROPERTY OVERVIEW
   Asset class, size, current owner of record (Source #2/#3, dated).

2. DOCUMENTED TRIGGER(S)
   List each confirmed signal with source, date, and document ID.
   State outcome: Advance / Advance with caveat, per Rule 1.6.

3. WHY IT MATTERS
   Plain-language statement of documented facts only. No invented metrics. No explanation,
   prediction, or characterization of legal or procedural mechanics. Any market/vacancy figure
   cited here must name the specific publisher and scope (Section 0).

4. EVIDENCE LOG
   Every source checked, including negative results, with links/IDs and access dates.
   Avenue used per source, and final retrieval method: auto-retrieved via [method],
   or manually retrieved by user (pasted [date]).
   Note any close-variant name matches used to satisfy the signal minimum.
   Note which entity name (owner vs. lender/guarantor) produced any Source #7 match, or that it was skipped.

5. SUGGESTED NEXT STEP
   Fact-based outreach angle referencing only documented findings. No legal advice, no procedural predictions.
```

---

## 7. PERSISTENT CANDIDATE LOG (cross-run record — internal only, never client-facing)

**Purpose:** Every property that reaches Step 6 is permanently recorded — pass, caveat, or `DO NOT ADVANCE` — so research already spent is never lost.

**Where it lives:** A single running file (e.g. `candidate_log.csv`), stored in the project root — see Rule 12 for the broader requirement this log is one part of.

**What gets logged, for every candidate reaching Step 6, regardless of outcome:**
- Date evaluated, submarket/run it came from
- PID, address, owner of record, `LU`/`LU_DESC`, assessed value
- Which narrowing filter (if any) surfaced or excluded it in Step 1, and that filter's noted bias
- Every signal type checked, with found/not-found/skipped status, source, and access date — including any instrument/case found but not counted due to age (Signal 2) or resolution status (Signal 4) or filing type (Signal 5)
- Final outcome (Advance / Advance with caveat / `DO NOT ADVANCE`) and the one-line reason
- Avenue/retrieval method used per source

**Re-check procedure for a previously-logged parcel:**
- Do not redo full research from scratch. State "previously evaluated [date], prior outcome: [X]."
- Re-check only what can meaningfully change over time. Ownership identity and LU classification don't need re-verification unless something specific suggests they've changed. A previously-old instrument (outside the 12-18 month Signal 2 window) doesn't need re-checking, but new instruments since the last check do.
- If the outcome changes on re-check, add a **new dated entry** rather than overwriting the old one.

---

## 8. GATE BEFORE SCALING

Do not process a second submarket, second asset class, or automate any step beyond manual/scripted lookup until:
- At least one property has passed all 9 steps and produced a complete report, and
- The user has explicitly reviewed and approved that report as representative of desired output quality.

If any step repeatedly produces zero surviving candidates across two different submarkets, stop and flag to the user that the trigger definitions in Section 4 may need revision — do not loosen the 2-signal minimum unilaterally. (Signal 2's recency requirement, above, was tightened based on a structural finding independent of this two-submarket threshold — see Rule 13.)

**Open item — Signal 1 usability:** Neither Source #2 nor Source #3 exposes a real tax-delinquency or tax-title field. Before relying further on Signal 1 as written, research whether Boston's Treasury/Collector's office (a separate department from Assessing) publishes any public delinquency or tax-title list. If none exists through free sources, Signal 1 should be treated as effectively unusable and the 2-signal minimum should be expected to rely on Signals 2–5 in practice.

**Maintenance note:** If Source #3's current fiscal-year FeatureServer is confirmed superseded by a newer one during any session, update Section 2 to reflect it. If Sources #1/#5's automated avenues are re-confirmed working in a future session, update their status accordingly rather than leaving the v12 "manual-only" note stale indefinitely.

---

## CHANGELOG

**v1 → v2:** Added citation discipline for market figures; operational confidence rubric; Source #6 re-verification note; LU-code/boundary pre-Step-1 requirement; tax-status currency caveat.

**v2 → v3:** Removed dated "verified" claim on Source #5; replaced non-functional Source #6 URL with masscourts.org; added institutional-ownership heuristic; added manual fallback for Sources #8/#9; strengthened Rule 8.

**v3 → v4:** Added Land Court/SCRA note to Source #6 and SPV/guarantor-name addendum to Source #7.

**v4 → v5:** Removed the Land Court/SCRA legal-procedure claim entirely; flattened confidence scoring to three plain outcomes; added an explicit prohibition on legal/procedural characterization; kept the SPV addendum.

**v5 → v6:** Added the Retrieval Protocol (agent-first automated retrieval with manual fallback).

**v6 → v7:** Removed a fixed attempt-count cap. Retrieval became avenue-exhaustive.

**v7 → v8:** Corrected Source #3's description from "Socrata-backed" to CKAN, with the actual API endpoint.

**v8 → v9:** Flagged Source #3's CKAN API avenue as `UNCONFIRMED`; added a possible `UNCONFIRMED` avenue for Source #2.

**v9 → v10:** Live-tested and confirmed a real avenue for Source #3 (ArcGIS FeatureServer); dropped the CKAN avenue; added an `UNCONFIRMED` VPN/proxy avenue.

**v10 → v11:** Added Rule 10 and Section 7 (persistent candidate log); added Rule 11 (check for fresher sources); added Rule 12 (persist step state to durable files); rewrote Source #8/#9 discard criteria; documented the confirmed Firebase backend for Source #2 and its missing delinquency field; added the Section 8 open item on Signal 1 usability.

**v11 → v12 (this version):**
- **Section 4, Signal 2 (Ownership/lien change): tightened to require an instrument dated within the trailing 12-18 months.** The first fully-completed run (5 Seaport candidates, Steps 1-9) found every candidate satisfied the un-tightened version regardless of instrument age, producing zero discriminating value. Older instruments are still recorded as historical context but no longer count toward the 2-signal minimum.
- **Section 4, Signal 4 (Legal distress): clarified that a resolved/dismissed case does not satisfy this signal**, even if it existed recently — surfaced when a case initially treated as an open signal turned out, on manual court lookup, to have been voluntarily dismissed months earlier.
- **Section 4, Signal 5 (Institutional distress): clarified that only 8-K/10-K/10-Q filings satisfy this signal** — a Form D or other filing type does not, even if it confirms a genuine institutional ownership connection.
- **Added Rule 13:** a full-pool `DO NOT ADVANCE` result is valid and doesn't itself justify loosening a signal, but a signal found to be structurally non-discriminating should be corrected regardless of the two-submarket threshold in Section 8.
- **Source #6 (Section 2): corrected the Housing Court division for Boston/Suffolk County to Eastern Housing Court** (not Metro South, which was used incorrectly once mid-run before being caught and corrected).
- **Sources #1 and #5 (Section 2): documented as confirmed manual-only this session** — all automated avenues tried for both were blocked by bot-detection (Incapsula/Cloudflare) in the same session. Not asserted as permanently broken; flagged for re-verification at the start of future sessions per Rule 8.
- Updated Steps 4-9 to reflect the tightened signal definitions and to explicitly treat a full-pool `DO NOT ADVANCE` as a complete, reportable result rather than an incomplete run.
