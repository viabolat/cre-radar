# Source registry

One section per external source touched by any pipeline stage. Checked
before attempting a new source (to avoid repeating a failed approach) and
updated every time a source is touched. Template:

### <Source name> — <town/district, if source is scoped that narrowly>

- **URL:**
- **Access category:** hard-blocked | login-gated | public-but-js-rendered | static-parseable | open-api
- **Stage(s) that use this source:**
- **What was tried:** (one bullet per distinct attempt)
- **What worked / what didn't:**
- **Current recommended approach:**
- **Open questions:**
- **Date last verified:** YYYY-MM-DD

---

### masslandrecords.com — Suffolk / Middlesex South / Worcester / Dukes

- **URL:** masslandrecords.com (per-district paths); successor/mirror
  massrods.com found on some districts
- **Access category:** hard-blocked (for any automated/headless retrieval)
- **Stage(s) that use this source:** Stage 4
- **What was tried:** direct HTTP fetch; WebFetch; standalone Playwright
  automation
- **What worked / what didn't:** all three blocked by Incapsula, which
  specifically targets automation-launched browsers (CDP flags,
  `navigator.webdriver`) with a hard "incident ID" refusal, not a CAPTCHA —
  confirmed a structural block, not a fixable fetch bug
- **Current recommended approach:** session-assisted capture only — browse
  and search as a human in real Chrome; `massrecords-api`'s Tampermonkey
  userscripts (`capture.user.js`, `capture-image.user.js`) read the
  already-rendered page and forward it to the local FastAPI service. This
  is a permanent, by-design handoff, not a gap to close later.
- **Open questions:** which of the "Unconfirmed" districts (Middlesex
  North, Norfolk, Plymouth, Nantucket) are actually on this domain vs. the
  separate one used by Barnstable/Berkshire/Bristol/Essex/Franklin/
  Hampden/Hampshire/Worcester North — untested.
- **Date last verified:** 2026-09-14 (per massrecords-api/README.md)

### MA Secretary of the Commonwealth — CorpSearch

- **URL:** https://corp.sec.state.ma.us/corpweb/CorpSearch/CorpSearch.aspx
- **Access category:** login-gated-equivalent — not a login wall, but an
  IP-based access restriction (same category of block as
  masslandrecords.com, different trigger)
- **Stage(s) that use this source:** Stage 3
- **What was tried:** direct search from the working session's IP
- **What worked / what didn't:** succeeds when the session's IP isn't
  subject to MA gov's access restriction; blocked when it is, requiring a
  Boston-exit VPN — conditional, not structural (see
  `03-owner-entity-resolution.md`'s distinction from Stage 4's permanent
  block)
- **Current recommended approach:** attempt directly first; if blocked,
  complete via Boston-exit VPN / browser session
- **Open questions:** none currently — behavior is understood, just
  session-dependent
- **Date last verified:** 2026-09-15

### Citizenserve — Revere / Brockton / Medway

- **URL:** (per-town Citizenserve portal URL — not yet recorded)
- **Access category:** login-gated
- **Stage(s) that use this source:** Stage 2
- **What was tried:** nothing yet — identified as the permit vendor for
  these three towns, not yet attempted
- **What worked / what didn't:** n/a
- **Current recommended approach:** unresolved — requires registering an
  account per town/vendor as a one-time manual setup step; whether
  subsequent searches can then be automated with stored credentials has
  not been tried
- **Open questions:** (1) can credentials be stored and reused safely — no
  secrets-storage mechanism decided yet (see plan Section 4, ambiguity 4);
  (2) is account creation itself automatable or does it require a human
  (email verification, etc.)
- **Date last verified:** not yet checked

### PermitEyes — Falmouth / Chelmsford / Mashpee / North Reading / Berkshire County

- **URL:** (per-town PermitEyes portal URL — not yet recorded)
- **Access category:** public-but-js-rendered
- **Stage(s) that use this source:** Stage 2
- **What was tried:** plain HTTP fetch
- **What worked / what didn't:** plain fetch returns an empty table — the
  page ships a static shell and loads Owner/Applicant/Parcel No./Street/
  Description/Permit Number/Issue Date via JavaScript after render, so a
  non-browser fetch never sees the data
- **Current recommended approach:** untested but two candidates worth
  trying before treating this as a handoff: (1) Claude-in-Chrome drives
  the search form and the page's own "Export to Excel" button, then reads
  the exported file; (2) reverse-engineer the underlying AJAX/XHR call the
  rendered page makes and hit that directly
- **Open questions:** which of the two candidate approaches actually
  works, if either — neither has been tried yet
- **Date last verified:** not yet checked
