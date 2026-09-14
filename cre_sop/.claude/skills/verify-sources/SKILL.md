---
name: verify-sources
description: Click-tests every approved data source URL in the SOP and reports live/blocked/changed status. User-invoked at the start of a session, per the SOP's rule that sources must be re-verified fresh every session, not assumed permanent.
disable-model-invocation: true
---

# Source Verification

`sop.md`'s Section 2 (Approved Free Data Sources) is the live list of
sources - do not hardcode the source list in this skill file. The list can
grow, shrink, or have its known-avenue notes updated across SOP versions
(Sources #1/#5's manual-only status, for example, is explicitly documented as
provisional and due for re-check, not permanent). Read Section 2 fresh each
time this skill runs.

## What to do

1. Read `sop.md`'s Section 2 in full to get the current source list, each
   source's URL(s), and its currently-known avenue(s).
2. For each source, per the SOP's own retrieval protocol (Section 1's
   avenue-exhaustive rule): try the currently-documented primary avenue
   first (direct API/fetch where one is documented), and only fall through
   to a secondary avenue if the primary fails. Do not attempt to bypass a
   bot-detection/CAPTCHA gate - one confirmed hit of that gate is sufficient
   to record the source as blocked/manual-only for this session.
3. For each source, record:
   - Still reachable via its documented avenue - unchanged
   - Reachable, but via a different avenue than documented - flag as a
     Section 2 update candidate
   - Blocked (bot gate, redirect loop, 404, structural change) - manual-only
     for this session
   - Structure appears to have changed (different fields, different API
     shape) even if reachable - flag for review, don't assume old field
     names/paths still work
4. Report a simple table: Source # | reachable? | avenue used | notes.
5. Do not edit `sop.md` itself with these results - that file only changes
   through the project's explicit, user-confirmed version-upgrade process.
   Instead, report findings in chat and let the user decide whether they
   warrant a Section 2 update in the next SOP revision.

This directly implements Section 1's requirement that sources are verified
fresh every session, with no dated "verified as of" claims treated as
still valid from a prior session.
