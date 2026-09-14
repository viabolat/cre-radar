<!--
One entry per index-ready lead. Fill every [bracket] from data/leads.csv + data/signals.csv,
then BLIND it per the rules below before it goes in a public-facing deliverable. Full exact
values always stay in data/signals.csv / data/leads.csv for internal use — only the deliverable
copy gets generalized.

RULES:
  - The Intent Trigger text may state ONLY what a signals.csv row documents. Never invent
    permit numbers, dollar amounts, or lien status.
  - Never put a raw permit number or a recorded-instrument book/page number in this doc — a
    corridor-familiar reader can look either up directly and get the exact address. Refer to
    "a Waltham building permit" / "a recorded [document type]" instead, and keep the exact
    number only in signals.csv.
  - Never name a tenant, lender, or bank in this doc, even if signals.csv has the real name —
    a named tenant is the single easiest way to reverse the address (search "[tenant] lease
    Waltham"). Use a generic type instead (e.g. "a life-sciences tenant", "a healthcare-services
    tenant", "a private lender").
  - "Calculated Footprint" and "Lot Size" are ranges, not exact figures — bucket the real
    leads.csv value into a band (footprint: 10K-wide bands under 50K SF, 25K-wide up to 150K,
    50K-wide up to 500K, 100K-wide above; lot size: 1-acre bands under 5 acres, 5-acre bands
    5-20 acres, 10-acre bands above). Never state the exact SF or acreage.
  - Any dollar amount (permit valuation, sale price, mortgage amount) is a range, not an exact
    figure — use bands like <$100K, $100K–500K, $500K–1M, $1–2.5M, $2.5–5M, $5–10M, $10–20M,
    then $5M-wide bands above $20M.
  - Any date (permit filed, instrument recorded) is a calendar quarter (e.g. "Q1 2026"), not
    an exact day. A bare year is fine where the source itself is only year-granular.
  - Address is blinded to street + node only (no street number) so the asset facts stay
    checkable in aggregate (does an event of this type/scale/timing exist here) without handing
    over the specific record needed to identify the parcel outright.
  - Owner + contact rows stay literally as the LOCKED lines below.
-->

### INDEX ENTRY: [lead_id]

- **Asset Categorization:** [Flex / Suburban R&D Facility | Low-Rise Industrial Logistics Warehouse]
- **Submarket Geography:** Route 128 Corridor — Waltham node ([street name] frontage)
- **Calculated Footprint:** ~[banded SQFT range] ([footprint_source])
- **Zoning Designation:** [zoning]
- **Lot Size:** [banded acreage range]
- **Identified Intent Trigger:** [1–3 sentences, each traceable to a signals.csv row, blinded
  per the rules above. Example shape — replace with real values:
  "A Waltham building permit filed [quarter] for [paraphrased scope], valuation in the
  [$range]. A Middlesex South [document type] recorded [quarter], naming [generic tenant/lender
  type]."]
- **Signal Recency:** most recent trigger dated [quarter]
- **Actionability Window:** [one line — e.g. near-term lease stabilization / recapitalization /
  landlord buyout — stated as a hypothesis, not a certainty]
- **True Owner Entity:** [LOCKED — SYNDICATED DATA LICENSE REQUIRED]
- **Decision-Maker Contact Infrastructure:** [LOCKED — SYNDICATED DATA LICENSE REQUIRED]

---
