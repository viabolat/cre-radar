# CRE-SOP Checkpoint — Seaport/South Boston Waterfront, Office
**SOP version:** v10 (Steps 1-7) · **Session date:** 2026-09-12 · **Status:** RUN CLOSED — Steps 1-9 complete, full-pool DO NOT ADVANCE (0 of 25 candidates advanced), no report produced. See Section 8 gate for next-run guidance.

This file is a data checkpoint only — a persisted snapshot of confirmed findings so a future session doesn't have to re-derive them from ephemeral `/tmp` scratch files. It does not replace the SOP (`sop.md`), which remains source of truth for process/rules.

---

## Known gaps (do not paper over these — re-verify before relying on them)

1. **Step 1's exact locked boundary/LU statement** (the literal text stated in the original Step 1 output — which LU/LU_DESC values were declared "office" and the exact submarket boundary polygon/street-range) was not preserved verbatim through a prior context compaction. What's reconstructed below is derived from the underlying parcel data (all candidates carry `LU='C'` with an OFFICE-prefixed `LU_DESC`), which is consistent with but not a verbatim restatement of that original lock.
2. **Step 2's per-candidate avenue log** (which of LoopNet direct / Crexi direct / web-search fallback resolved each of the 25) did not survive compaction beyond the aggregate outcome. The specific identities behind the user's earlier reference to "#1, #11, #15, #16" (other completed-historical-sale candidates, same category as 1 Marina Park Dr) are **not** reliably recoverable from current context — flagged here rather than guessed. Per Rule 8, Step 2 avenues get re-verified fresh at evidence-log time (Step 7) regardless, so this is not fatal, but it means Step 2's output below is an aggregate disposition, not a full avenue-by-avenue log.
3. **Correction:** PID `0602643075` was mislabeled in this session's prior chat message as "280-294 Congress St." It is a distinct, separate parcel — assessor record has no street number (`ST_NAME="Congress ST"`, `ST_NUM=null`), owner "Seaport L Title Holder," lot size 24,888 sq ft. It is NOT part of the 280-294 Congress St Tower/Office building (that's PIDs `0302952018`+`0302952020`, owner BP Russia Wharf LLC — a different, separate candidate). Corrected in the tables below.

---

## Step 1 — Final Candidate Pool (25 buildings, post-Step-3 exclusion)

**Scope:** Suffolk County / City of Boston, Seaport / South Boston Waterfront, office asset class.
**LU filter used:** `LU='C'` with `LU_DESC` ∈ {OFFICE CLS A, OFFICE CLS A-, OFFICE CLS B+, OFFICE 3-9 STORY}.
**Source/avenue:** Source #3, ArcGIS FeatureServer direct query (per SOP Section 2/Step 1).
**Raw parcels:** 28 → merged to 26 buildings (280-294 Congress St Tower+Office = 1 building; 12-56/19-39 Thompson Pl = 1 building) → **25 buildings** after 10 Melcher St excluded at Step 3 (see below).

| # | Building | PID(s) | Owner | LU_DESC | Assessed Value |
|---|---|---|---|---|---|
| 1 | 245 Summer St | 0305364005 | 245 Summer Street LLC | OFFICE CLS A- | $379,407,540 |
| 2 | 200 Seaport Blvd | 0602672052 | Commonwealth Pier Trust II | OFFICE CLS A- | $365,399,458 |
| 3 | 1 Marina Park Dr | 0602671035 | CLPF One Marina Park Garage LLC | OFFICE CLS A | $337,800,600 |
| 4 | 556-624 Atlantic Ave | 0304340000 | Federal Reserve Bank of Boston | OFFICE CLS A | $333,237,900 |
| 5 | 280-294 Congress St (Tower+Office) | 0302952018, 0302952020 | BP Russia Wharf LLC | OFFICE CLS A | $320,015,200 + $84,765,400 |
| 6 | 90-110 Northern Ave | 0602671039 | 100 Northern Avenue LLC | OFFICE CLS A | $319,836,100 |
| 7 | 155 Seaport Blvd | 0602677010 | Commonwealth Flats Development 121A West LP | OFFICE CLS A- | $297,109,400 |
| 8 | 2 Seaport Ln | 0602679035 | Commonwealth Flats East | OFFICE CLS A- | $280,965,800 |
| 9 | 101 Seaport Blvd | 0602643022 | 101 Seaport Blvd LLC | OFFICE CLS A | $280,718,100 |
| 10 | 601 Congress St | 0602678701 | BRE-BMR Congress LLC | OFFICE CLS A | $262,661,864 |
| 11 | 121 Seaport Blvd (Comm. Garage) | 0602643042 | SVF Seaport Owner LLC | OFFICE CLS A | $261,410,400 |
| 12 | 1 Boston Wharf Rd | 0602643070 | Seaport L-5 Title Holder LLC | OFFICE CLS A | $190,870,600 |
| 13 | 474-466 Atlantic Ave | 0302956000 | NFLSRE 470 Atlantic LLC | OFFICE CLS A- | $139,926,700 |
| 14 | 12-56/19-39 Thompson Pl | 0602654010, 0602652010 | Fort Point Channel Investors LLC | OFFICE CLS B+ | $73,717,500 + $60,985,700 |
| 15 | 273 Summer St | 0602703000 | Two 81 Summer St LLC | OFFICE CLS B+ | $54,894,800 |
| 16 | 343 Congress St | 0602694000 | MEPT Seaport 343 Congress LLC | OFFICE CLS B+ | $48,003,300 |
| 17 | 44 Farnsworth St | 0602662015 | T-C Fort Point Creative | OFFICE CLS B+ | $42,526,800 |
| 18 | 33-41 Farnsworth St | 0602660010 | CRE-MLL Farnsworth Property Owner LLC | OFFICE CLS B+ | $35,506,900 |
| 19 | 374 Congress St | 0602646010 | T-C Fort Point Creative | OFFICE CLS B+ | $33,885,200 |
| 20 | Congress St (no street number recorded) | 0602643075 | Seaport L Title Holder | OFFICE CLS B+ | $30,693,800 |
| 21 | 321-325 Summer St | 0602764000 | Three 21 Summer St LLC | OFFICE CLS B+ | $30,167,100 |
| 22 | 305 Congress St | 0602691000 | Congress Ventures LLC Mass LLC | OFFICE CLS A- | $29,065,000 |
| 23 | 313 Congress St | 0602692000 | MEPT Fort Point Creative LLC | OFFICE CLS B+ | $27,963,200 |
| 24 | 337-347 Summer St | 0602765030 | ASB Summer Street Venture LLC | OFFICE CLS B+ | $27,447,660 |
| 25 | 268-272 Summer St | 0602700000 | 256 Holdings LLC | OFFICE 3-9 STORY | $26,199,900 |

**Excluded from pool (not a Step 3 finding, dropped as out-of-scope):**
**10 Melcher St** — PID `0602702000`, owner 263 Summer Street Development LLC, FY25 FeatureServer said `LU='C'` (office), but Source #2's live API (`landUseCode='E'`, Exempt Ownership; direct API fetch, 2026-09-12) is authoritative per user instruction. Dropped from the pool entirely.

---

## Step 2 — Negative Check (Already Listed?)

**Method:** Source #8 (LoopNet) / Source #9 (Crexi) direct fetch, web-search fallback per Rule 9.
**Aggregate result:** All 25 candidates — **no active listing found.**

**Special handling — completed historical sales treated as "No active listing" (not an open flag), per interpretive rule:**
- **1 Marina Park Dr** (PID 0602671035) — sale closed: Oxford Properties completed acquisition from Clarion Partners, **$435M, August 2026** (deed recorded ~Aug 18, 2026; press releases Aug 19-25, 2026 confirm completion). User-supplied correction, 2026-09-12.
- Three additional candidates in this same category (referred to earlier in-session as "#1, #11, #15, #16") were also treated as completed historical sales, not active listings — **their specific identities were not preserved through context compaction** (see Known Gaps above). Re-identify if this distinction becomes load-bearing for a report.

No candidate was discarded at Step 2 — all 25 survived to Step 3.

---

## Step 3 — First-Pass Tax-Status Screen (Source #2)

**Method:** Source #2 direct API fetch (Firebase callable function `fetchPropertyDetailsByParcelId`, `us-central1-assessing-properties-prod.cloudfunctions.net`), confirmed working avenue, 2026-09-12.

**Finding on `fine38d` field:** Source-embedded label (from `properties.boston.gov` JS bundle): `title:"38D Fine"`, `description:"This is a fine imposed under Massachusetts General Law Chapter 59, Section 38D for failure to file required property tax documents."` — a compliance-triggered penalty, not a categorical/flat fee. Kept as an irregular flag (not downgraded).

**5 irregular candidates (fine38d fee present, all $250):**

| Building | PID(s) | Owner | fine38d |
|---|---|---|---|
| 101 Seaport Blvd | 0602643022 | 101 Seaport Blvd LLC | $250 |
| 1 Boston Wharf Rd | 0602643070 | Seaport L-5 Title Holder LLC | $250 |
| 12-56/19-39 Thompson Pl | 0602654010, 0602652010 | Fort Point Channel Investors LLC | $250 each |
| Congress St (no street number, PID 0602643075) | 0602643075 | Seaport L Title Holder | $250 |
| 313 Congress St | 0602692000 | MEPT Fort Point Creative LLC | $250 |

**20 discarded** — routine tax profile, no irregularity (uniform 1% CPA surcharge across all candidates is routine, not discriminating; neither Source #2 nor #3 exposes a true delinquency/payment-status field — a confirmed limitation, not fabricated).

**10 Melcher St** — excluded from the pool entirely (see Step 1 section above), not counted as either irregular or discarded.

---

## Step 4 — Ownership and Lien Check (IN PROGRESS)

Applies to the 5 Step-3-irregular buildings only.

**Source #5 (UCC Search) — COMPLETE, all clean:**

| Building | Debtor searched | Result | Avenue |
|---|---|---|---|
| 101 Seaport Blvd | 101 Seaport Blvd LLC | None found | Manually retrieved by user, pasted 2026-09-12 |
| 1 Boston Wharf Rd | Seaport L-5 Title Holder LLC | None found | Manually retrieved by user, pasted 2026-09-12 |
| 12-56/19-39 Thompson Pl | Fort Point Channel Investors LLC | None found | Manually retrieved by user, pasted 2026-09-12 |
| Congress St (PID 0602643075) | Seaport L Title Holder | None found | Manually retrieved by user, pasted 2026-09-12 |
| 313 Congress St | MEPT Fort Point Creative LLC | None found | Manually retrieved by user, pasted 2026-09-12 |

Active-filings search only (matches Signal 3's "active UCC-1" requirement) — Signal 3 not satisfied for any of the 5.

**Source #1 (Massachusetts Land Records) — IN PROGRESS.** Automated avenues exhausted this session (Incapsula/Cloudflare bot-detection gates on both `masslandrecords.com` and its successor `massrods.com/suffolk`, confirmed via curl + WebFetch, 2026-09-12). Manual fallback: Suffolk Registry of Deeds "20/20 Perfect Vision" web interface, Name Search, results pasted by user. **Indexing quirk discovered:** entity names beginning with a leading numeral are re-indexed with the numeral moved to the end (e.g. "101 Seaport Blvd LLC" → indexed as "Seaport Blvd LLC 101"). Always verify via a broader Property Search cross-reference if a Name Search returns 0 hits for a numeral-leading entity name.

User confirmed 2026-09-12 that all Name Search results pasted are the complete result sets (no further pages) for all 5 candidates. Four key documents were pulled as PDFs by the user (via the Registry's "View Img," saved locally under `acsResources/`) and reviewed to satisfy the "lender/guarantor/affiliated entity" requirement.

**1) 101 Seaport Blvd LLC — COMPLETE.** Clean, entity-scoped Name Search ("Seaport Blvd LLC 101"), 7 instruments, all 2016–2017, nothing since:

| Date | Book/Page | Type | Role |
|---|---|---|---|
| 4/12/2016 | 55965/53 | UNIT DEED | GT (Grantee) |
| 4/12/2016 | 55965/58 | AFFIDAVIT | GR |
| 4/14/2016 | 55976/323 | ASSIGNMENT | GT |
| 5/3/2016 | 56069/323 | APPOINTMENT | GR |
| 2/3/2017 | 57524/106 | AMENDMENT | GR |
| 8/29/2017 | 58444/71 | LIEN | GR |
| 9/19/2017 | 58546/52 | RELEASE | GR |

Lien released ~3 weeks after filing. No activity since 9/19/2017. No mortgage instrument in this entity's record.

**Document reviewed — ASSIGNMENT, Bk 55976/Pg 323 (4/14/2016):** "Assignment and Assumption of Declarant's Rights" — SCD L1 Seaport Square LLC ("Assignor") assigns all rights/obligations as Declarant under the 101 Seaport Boulevard Condominium Master Deed (11/4/2015, Bk 55280/Pg 1) to 101 Seaport Blvd LLC ("Assignee"), which had acquired the Commercial/Garage Unit via Unit Deed of even date. Not a financing document — no lender named. **Assignee signed by: Union Investment Real Estate GmbH** (German limited liability company), "acting in its own name and for the account of the open ended real estate fund UniImmo: Europa, its sole member," by Dr. Reinhard Kutscher and Dr. Frank Billand, managing directors. **Affiliated entity for Step 5 SPV check: Union Investment Real Estate GmbH / fund UniImmo: Europa** — the ultimate member/sponsor behind 101 Seaport Blvd LLC.

**2) Seaport L-5 Title Holder LLC (1 Boston Wharf Rd) — COMPLETE (user confirmed no further pages).** Notable instruments:

| Date | Book/Page | Type |
|---|---|---|
| 12/10/2019 | 62207/222 | MORTGAGE |
| 9/17/2021 | 66306/125 | MORTGAGE |
| 9/17/2021 | 66306/156 | FINANCING STATEMENT |
| 3/18/2026 | 72531/270 | CONTINUATION OF FINANCING STATEMENT |
| 8/13/2026 | 73123/17 | ASSIGNMENT |
| 8/27/2026 | 73179/331 | RELEASE |
| 8/27/2026 | 73179/334 | RELEASE/TERM FINANCING STATEMENT (UCC3 Amendment) |

No LIEN-type entry. Plus routine deed/easement/certificate/subordination/order/vote activity 2018–2026 (full list in session transcript, not reproduced here).

**Document reviewed — UCC FINANCING STATEMENT AMENDMENT, Bk 73179/Pg 334 (recorded 8/27/2026, Doc #55607, fixture filing):** Terminates the financing statement originally filed at Bk 66306/Pg 156 (9/17/2021). **Secured Party authorizing termination: Wells Fargo Bank, National Association, as Administrative Agent.** Debtor: Seaport L-5 Title Holder LLC. Collateral: fixture filing on Consolidated Parcel L5 (1-27 Boston Wharf Rd, City of Boston Tax ID 06-2643-070). **Lender for Step 5: Wells Fargo Bank, N.A. (as Administrative Agent — indicates a syndicated facility), financing statement filed 9/17/2021, terminated 8/27/2026.** The same-date RELEASE (73179/331) was not opened but, given the matching date/book and adjacent page, is very likely the corresponding mortgage discharge — flagged as a reasonable inference, not independently confirmed.

**3) Fort Point Channel Investors LLC (12-56/19-39 Thompson Pl) — COMPLETE (user confirmed no further pages).** Major finding — most extensive record of the 5 candidates:
- **~20 LIEN filings**, 12/20/2018–3/5/2026: 60555/281, 63405/348, 63406/1, 69514/242, 69615/286, 71842/275, 71842/279, 71859/272, 71906/95, 71941/87, 71941/91, 71962/225, 71962/228, 71989/53, 72011/323, 72038/1, 72062/26, 72062/29, 72083/110, 72138/265, 72152/258, 72487/307.
- **6 COMPLAINTS**: 69669/161 (11/28/2023), 69757/107 (12/26/2023), 72288/343 (1/5/2026), 72314/234 (1/13/2026), 72399/40 (2/9/2026), 72528/120 (3/17/2026).
- **13 RELEASES**: 60637/260 (1/14/2019), 61075/341 (5/7/2019), 63521/243 (8/7/2020), 69950/142 (3/7/2024), then a cluster of 9 between 6/8/2026–7/7/2026: 72860/179, 72861/188, 72862/296, 72866/198, 72894/166, 72912/315, 72919/224, 72919/308, 72942/234, 72976/188.

Fort Point Channel Investors LLC recorded in GR role on nearly every LIEN/COMPLAINT/RELEASE row.

**Document reviewed — COMPLAINT, Bk 72487/Pg 307 (recorded 3/5/2026; underlying Superior Court filing dated 2/20/2026, C.A. No. 26-0522, Suffolk Superior Court), one representative document of ~26 in this pattern — not all reviewed:** "Mechanic's Lien Complaint Under M.G.L. c. 254." **Plaintiff:** Boston Builders, Inc. (subcontractor, Rockland MA). **Defendants:** Englewood Construction, Inc. (general contractor, Illinois corp.); Lineage Hospitality LLC a/k/a Sally's Apizza (tenant, Delaware LLC); **Fort Point Channel Investors LLC** (landlord/fee owner, Delaware LLC, registered agent CT Corporation System, 155 Federal St Suite 700, Boston MA 02110). Facts stated: subcontract dated 4/30/2025 (Boston Builders/Englewood) for finish carpentry, metal studs, drywall at 12-56 Thomson Place (Sally's Apizza space); subcontract price $428,431; completed/billed total $293,662.15; amount paid to date $0.00; balance due $293,662.15. Notice of Contract recorded 9/10/2025 (Bk 71859/Pg 272). Statement of Amount Due recorded 11/26/2025 (Bk 72152/Pg 258). Complaint seeks joint-and-several judgment against all three defendants for $293,662.15 + interest + costs, plus lien enforcement/sale of the property interest. **This confirms the LIEN-type filings on this candidate are M.G.L. c.254 mechanic's liens tied to tenant-fit-out subcontractor disputes**, with Fort Point Channel Investors LLC named as fee-owner/landlord defendant. Given the volume (~26 lien/complaint/release documents spanning 2018–2026), this single document is representative, not exhaustive — full resolution status of each individual lien was not pursued as disproportionate to Step 4's scope.

**4) Seaport L Title Holder (PID 0602643075, Congress St) — COMPLETE.** Only one MORTGAGE (67575/255, 5/2/2022) and one RELEASE (71052/272, 2/3/2025). No LIEN-type entries beyond routine municipal lien certificates (tax-status certificates, not creditor liens). Consistent with Source #5 "none found."

**Document reviewed — MORTGAGE, Bk 67575/Pg 255 (recorded 5/2/2022, $10 consideration + Mortgage Covenants, up to $25,047,593):** **Grantor: Seaport L Title Holder LLC** (c/o WS Development, 33 Boylston Street, Suite 3000, Chestnut Hill, MA 02467). **Grantee/Mortgagee: Seaport D Office Owner LLC** (same c/o WS Development address). Property: East Service Road & Autumn Lane, Parcels L3 and L6 (per Exhibit A, "Redivision Plan of Land, Seaport Block L," prepared for Seaport L-5 Title Holder LLC). Signed by Richard A. Marks, VP & Secretary, as authorized representative of and on behalf of each Member of Seaport L Title Holder LLC.

**LABEL — RELATED-PARTY / INTERCOMPANY FINANCING, NOT THIRD-PARTY INSTITUTIONAL DEBT:** Grantor (Seaport L Title Holder LLC) and Grantee/Mortgagee (Seaport D Office Owner LLC) share the identical mailing address, both c/o WS Development, 33 Boylston Street, Suite 3000, Chestnut Hill, MA 02467, per the recorded instrument. This is the basis for the flag — no independent corporate-affiliation source was checked. If this mortgage factors into any downstream report (Step 5 or the Section 6 report), it must be labeled as apparent related-party/intercompany financing between affiliated WS Development entities, not as third-party institutional debt. Relevant affiliated entity for Step 5: **Seaport D Office Owner LLC (WS Development affiliate)**.

**5) MEPT Fort Point Creative LLC (313 Congress St) — COMPLETE (user confirmed no further pages; ~10 rows total).** No LIEN, MORTGAGE, or FINANCING STATEMENT found. Only DEEDs (1/14/2015), NOTICEs (8/19/2015, 1/5/2016), a municipal lien certificate + certificate + deed + agreement (3/27/2019), and an easement (6/10/2022). No lender/affiliated-entity document pulled — none of the instrument types warranted it.

---

## Step 4/6 — Fort Point Channel Investors LLC legal-distress signal — RESOLVED (Source #6, manual, checked 2026-09-12)

**Suffolk Superior Court, C.A. No. 2684CV00522** (Boston Builders Inc. v. Englewood Construction Inc., Lineage Hospitality LLC a/k/a Sally's Apizza, Fort Point Channel Investors LLC). Docket shows: **Notice of Voluntary Dismissal With Prejudice filed 6/10/2026. Disposition: Voluntary Dismissal, 6/10/2026.** User noted the docket's summary "Case Status: Open" field appears stale relative to the dismissal entry; the dismissal is treated as authoritative per the user's direct read of the docket.

**Signal 4 (legal distress) for Fort Point Channel Investors LLC: existed, now resolved.** Case was active from filing (2/20/2026) through dismissal (6/10/2026) — four months before this run (2026-09-12). Does **not** count toward the Section 4 two-signal minimum as an active signal. This resolution is consistent with, not contradicted by, the 9-release cluster already found at the Registry (72860/179 through 72976/188, 6/8/2026–7/7/2026) — same underlying dispute cluster clearing out at the registry and the courts within days of each other.

---

## Step 5 — Legal and Institutional Check (COMPLETE)

**Source #7 (SEC EDGAR Full-Text Search, `efts.sec.gov` API avenue — confirmed working, 2026-09-12).** Tested record-owner names and Step-4 lender/guarantor/affiliate names for all 5 candidates:

| Entity tested | Query | Total hits | Result |
|---|---|---|---|
| 101 Seaport Blvd LLC | "101 Seaport Blvd LLC" | 1 | **Match: CIK 0001694963**, Form D filing 1/18/2017, Delaware entity, business address Hamburg, Germany |
| Union Investment Real Estate (affiliate, from Step 4) | "Union Investment Real Estate" | 50 | **Match** — top hits include UIR 10th Street LLC (CIK 0001694961, adjacent CIK to 101 Seaport Blvd LLC) and 101 Seaport Blvd LLC (CIK 0001694963) again, plus unrelated third parties (CBRE, TIAA, Jones Lang LaSalle Income Property Trust, etc. — not further pursued as out of scope for this candidate) |
| Fort Point Channel Investors LLC | "Fort Point Channel Investors LLC" and "Fort Point Channel Investors" (broader) | 0 (both) | None found |
| Seaport L-5 Title Holder LLC | "Seaport L-5 Title Holder" | 0 | None found |
| Wells Fargo Bank, N.A. (lender, from Step 4) + Seaport L-5 | "Wells Fargo Bank, National Association" AND "Seaport" | 2,505 | Hits exist but are not narrowed to this specific property — Wells Fargo N.A. appears as trustee/servicer across thousands of unrelated commercial-mortgage-trust filings, and "Seaport" is a common place name; reviewing all 2,505 is disproportionate to Step 5's scope. **Not treated as a confirmed institutional-ownership match** — inconclusive, not pursued further |
| Seaport L Title Holder | "Seaport L Title Holder" | 0 | None found |
| Seaport D Office Owner LLC (affiliate, from Step 4) | "Seaport D Office Owner" | 0 | None found |
| MEPT Fort Point Creative LLC | "MEPT Fort Point" | 0 | None found |

**Disposition per SOP ("if neither shows an identifiable public-company connection, skip and note 'not institutionally owned — skipped'"):**
- **101 Seaport Blvd LLC — foreign-institutional ownership confirmed as a fact** (Union Investment Real Estate GmbH / UniImmo: Europa, corroborated by both the Step 4 registry document and the Source #7 EDGAR match). **Correction, applied at Step 6:** the EDGAR match is a **Form D** (exempt-offering notice), not an 8-K/10-K/10-Q. Section 4's Signal 5 ("Institutional distress") requires specifically "Filed 8-K/10-K/10-Q language naming the property, its owning entity, or a lender/guarantor entity" — a Form D does not meet that definition. Institutional ownership is a documented fact for this entity; it does **not**, by itself, satisfy Signal 5.
- Seaport L-5 Title Holder LLC — not institutionally owned; skipped (Wells Fargo hit inconclusive, not a property-specific match).
- Fort Point Channel Investors LLC — not institutionally owned — skipped.
- Seaport L Title Holder — not institutionally owned — skipped.
- MEPT Fort Point Creative LLC — not institutionally owned — skipped.

**Source #6 (MassCourts, manual avenue, checked 2026-09-12) — all 5 candidates complete.** User checked both Suffolk Superior Court Civil and Eastern Housing Court (the correct Boston division) for all 5 entities:

| Entity | Suffolk Superior Court Civil | Eastern Housing Court | Result |
|---|---|---|---|
| 101 Seaport Blvd LLC | none found | none found | None found |
| Seaport L-5 Title Holder LLC | none found | none found | None found |
| Seaport L Title Holder | none found | none found | None found |
| MEPT Fort Point Creative LLC | none found | none found | None found |
| Fort Point Channel Investors LLC | C.A. No. 2684CV00522 — resolved (voluntary dismissal w/ prejudice, 6/10/2026) | — | Existed, now resolved (logged above under Step 4/6) |

**Search-mechanics correction (Rule 8, worth carrying forward):** an earlier manual pass mistakenly queried Metro South Housing Court, which covers Norfolk County — not the correct division for Boston/Suffolk properties. The correct housing-court division for this SOP's scope is **Eastern Housing Court**. Re-run with the corrected division confirmed "none found" for the 4 candidates. Worth flagging as a possible SOP v11 addition to the Source #6 search-mechanics note, pending explicit approval to edit the SOP.

**Step 5 disposition, all candidates:**
- 101 Seaport Blvd LLC — institutional connection confirmed (Source #7); no legal case found (Source #6).
- Seaport L-5 Title Holder LLC — not institutionally owned, skipped (Source #7); no legal case found (Source #6).
- Fort Point Channel Investors LLC — not institutionally owned, skipped (Source #7); one legal case found, resolved 6/10/2026 (Source #6).
- Seaport L Title Holder — not institutionally owned, skipped (Source #7); no legal case found (Source #6).
- MEPT Fort Point Creative LLC — not institutionally owned, skipped (Source #7); no legal case found (Source #6).

---

## Step 6 — Signal Scoring (COMPLETE)

Applying Section 4's 5 signal definitions literally, to documented findings from Steps 3–5 only:

| Signal | Minimum evidence required | 101 Seaport Blvd LLC | Seaport L-5 Title Holder LLC | Fort Point Channel Investors LLC | Seaport L Title Holder | MEPT Fort Point Creative LLC |
|---|---|---|---|---|---|---|
| 1. Tax delinquency (#2/#3) | Delinquent status shown directly on parcel record | Not satisfied | Not satisfied | Not satisfied | Not satisfied | Not satisfied |
| 2. Ownership/lien change (#1) | Recorded instrument with doc number and date | **Satisfied** (7 instruments, incl. lien 58444/71) | **Satisfied** (2 mortgages, financing statement, assignment, releases) | **Satisfied** (~20 liens, 6 complaints, 13 releases) | **Satisfied** (mortgage 67575/255, release 71052/272) | **Satisfied** (deeds, notices, easement) |
| 3. Secured debt filing (#5) | Active UCC-1 naming the owner/entity | Not satisfied (none found) | Not satisfied (none found) | Not satisfied (none found) | Not satisfied (none found) | Not satisfied (none found) |
| 4. Legal distress (#6) | **Open** civil case involving the owner entity | Not satisfied (none found) | Not satisfied (none found) | Not satisfied — case existed (C.A. No. 2684CV00522) but is resolved (dismissed w/ prejudice 6/10/2026), not open as of 2026-09-12 | Not satisfied (none found) | Not satisfied (none found) |
| 5. Institutional distress (#7) | Filed 8-K/10-K/10-Q language naming the property, owning entity, or a Step-4 lender/guarantor | Not satisfied — EDGAR match is a **Form D**, not 8-K/10-K/10-Q; does not meet the definition | Not satisfied (Wells Fargo hit inconclusive/not property-specific) | Not satisfied (0 hits) | Not satisfied (0 hits) | Not satisfied (0 hits) |
| **Signal count** | — | **1** | **1** | **1** | **1** | **1** |
| **Outcome (Rule 1.6)** | — | **DO NOT ADVANCE** | **DO NOT ADVANCE** | **DO NOT ADVANCE** | **DO NOT ADVANCE** | **DO NOT ADVANCE** |

**Reason, uniform across all 5:** each candidate clears only Signal 2 (a recorded Source #1 instrument exists). No candidate reaches the 2-signal minimum — Signal 1 is unavailable this session (no true delinquency field exposed by Source #2/#3, a confirmed platform limitation, not a per-candidate finding), Signal 3 is clean across the board (Source #5 UCC search: none found), Signal 4 requires an *open* case and the only case found (Fort Point Channel Investors LLC) is resolved, and Signal 5 requires 8-K/10-K/10-Q language specifically, which no candidate produced (101 Seaport Blvd LLC's EDGAR hit is a Form D, a different form type). Per Rule 1.6, one signal alone = DO NOT ADVANCE. This is the SOP's own stated expectation for a Signal-5-limited run ("expect most candidates to clear the minimum via Signals 1–4, not Signal 5... A DO NOT ADVANCE outcome from Signal 5 being unavailable is expected, not a process failure") — but here none of Signals 1, 3, or 4 clear either, so no candidate reaches 2 signals by any combination.

---

## Step 7 — Evidence Log Compilation (COMPLETE)

**Evidence log: empty.** Section 5 Step 7 scope is "every property that passed Step 6" — Step 6 produced 0 Advance / Advance-with-caveat outcomes across all 5 candidates (all DO NOT ADVANCE). No evidence log entries to compile this run.

---

## Step 8 — Report Drafting (COMPLETE — null result)

**No report drafted.** Step 8's instruction is explicit: "Using only the evidence log from Step 7, draft the 5-part report (Section 6). If Step 7's log is empty, there is nothing to draft — say so and stop." Step 7's evidence log has zero entries (see above), so there is no property to draft a Section 6 report for. This is a complete, valid Step 8 outcome, not an incomplete run — consistent with Rule 13 (a full-pool `DO NOT ADVANCE` is a legitimate, reportable result).

---

## Step 9 — Final QA Pass (COMPLETE — null result)

**Nothing to QA.** Step 9's instruction: "Check the drafted report against Section 1 rules 4-6 and 9. If no report was drafted (empty result), there is nothing to QA — say so and stop." Step 8 produced no report, so there is no client-facing output to check against Rules 4 (sourcing), 5 (no financial/legal modeling), 6 (confidence outcomes), or 9 (Retrieval Protocol logging). Stated plainly and stopped, per the SOP.

**Run disposition:** All 9 steps of Section 5 are now complete for this run. Final result: **full-pool `DO NOT ADVANCE`** — 0 of the original 25 Seaport/South Boston Waterfront office candidates advanced past Step 6 (5 reached Step 6 via Step 3's irregularity filter; each cleared only 1 of the 2 required signals). No report was produced. Per Rule 13, this is a valid, complete, and permanently-logged outcome, not a failed or incomplete run — it does not itself justify loosening any Section 4 signal definition. Per Section 8, a second submarket with zero survivors would be the trigger to flag signal-definition review; this is the first submarket run, so no further definitional changes are indicated by this result alone.

---

## Source/avenue notes for this session (Rule 8)

- Source #2: confirmed working direct API avenue (Firebase callable functions), 2026-09-12.
- Source #3: confirmed working (used in Step 1, prior session segment).
- Source #5: confirmed working only via manual browser (automated fetch blocked by Incapsula), 2026-09-12. **Coverage gap discovered:** Source #5 (Secretary of the Commonwealth UCC search) does not index UCC fixture filings recorded at the Registry of Deeds (Source #1) — e.g. Seaport L-5 Title Holder LLC's FINANCING STATEMENT/CONTINUATION entries. A "none found" at Source #5 does not rule out recorded UCC activity; Source #1 is a necessary cross-check for real-estate-collateral UCC filings.
- Source #1: **no working automated avenue found this session** — manual-only, via Name Search on the Suffolk Registry's "20/20 Perfect Vision" web interface. Worth flagging to the user as a possible SOP v11 update (documented avenue no longer works; leading-numeral indexing quirk) once this run concludes, pending explicit approval to edit the SOP.
- Source #6 (MassCourts, masscourts.org): automated avenue confirmed blocked this session, 2026-09-12 (WebFetch returns a JS/meta-refresh stub, no usable form — consistent with the SOP's documented "I'm not a robot" gate). Per Rule 9, fell back to manual avenue: **user checked masscourts.org directly for C.A. No. 2684CV00522, 2026-09-12** — successful, returned full docket disposition (voluntary dismissal, 6/10/2026). Logged in the Fort Point Channel Investors LLC finding above.
