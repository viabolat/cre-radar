---
name: sop-step
description: Runs the next step of the CRE-SOP with correct one-step, persist-then-confirm gating. Use when the user says "proceed to Step N", "confirmed", "revise", or otherwise asks to continue the SOP workflow.
---

# SOP Step Runner

This skill does not contain its own copy of the SOP's rules. `sop.md` is a
versioned document (currently v12, but it will keep changing) and is the
project's sole source of truth. A paraphrased snapshot baked into this file
would silently drift out of date the next time `sop.md` is revised - exactly
the kind of staleness the project has already had to correct once (the
Metro South -> Eastern Housing Court fix, and the whole v10->v12 signal
rewrite). So:

**Before doing anything else, read `sop.md` in full** (it is short enough to
read whole - do not rely on memory or an earlier read from this conversation
if there is any chance the file has changed since). Pay specific attention to:

- **Section 1 (Operating Rules)** - especially the one-step-at-a-time rule,
  the exact `AWAITING CONFIRMATION` line format, the no-fabrication sourcing
  requirement, and the persist-to-file requirement.
- **Section 5 (Step-by-Step Workflow)** - the numbered step definitions
  themselves.
- Whatever the current **CHANGELOG** section says was most recently added or
  tightened - a rule that changed recently is the one most likely to differ
  from what you remember.

Then read `checkpoint.md` (or whatever the project's current checkpoint file
is named) to find the last completed step and confirmed status line.

## What to do

1. Determine the next incomplete step from Section 5, based on the
   checkpoint's status line - not from anything stated earlier in this
   conversation, since the checkpoint file is the durable record.
2. Execute exactly that one step, applying Section 1's rules as written in
   the live file - not as summarized here or anywhere else.
3. Persist the step's full output to the checkpoint file before responding,
   per the SOP's persistence rule.
4. End the response with the SOP's exact required confirmation line (read it
   from Section 1 - do not retype it from memory in case the exact wording
   has changed).
5. Do not advance past the one step, and do not treat silence or an
   ambiguous reply as confirmation - both per the live rules in Section 1.

If the SOP's filename, section numbers, or rule numbers have changed since
this skill was written, follow the live document's actual structure, not the
section names used above - they are locators for *this* session's file, not
a guaranteed permanent structure.
