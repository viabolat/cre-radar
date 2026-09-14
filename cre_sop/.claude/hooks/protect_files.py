#!/usr/bin/env python3
"""
PreToolUse guard for cre_sop.

Protects two classes of file from accidental mutation by the agent:
  1. sop.md - the versioned source of truth. Should only ever change via an
     explicit, user-confirmed SOP version upgrade (archive the old version first).
  2. acsResources/*.pdf - retrieved evidence documents. Never edited/overwritten
     once saved.

Exists because a prior session had a real incident: an out-of-band `mv` silently
overwrote an archived SOP version (macOS `mv` overwrites same-named destination
files with no prompt). This hook can't stop actions taken outside Claude Code,
but it stops this agent from repeating that mistake via Edit/Write/Bash.

Blocking is intentionally conservative (biased toward false positives over a
missed overwrite) since these files are touched rarely and the cost of an
extra confirmation step is low.
"""
import json
import shlex
import sys

MUTATING_VERBS = {"mv", "cp", "rm", "truncate", "shred", "unlink", "tee"}


def is_protected_path(path: str) -> bool:
    if not path:
        return False
    norm = path.replace("\\", "/").lower()
    base = norm.rsplit("/", 1)[-1]
    if base == "sop.md":
        return True
    if "acsresources/" in norm and norm.endswith(".pdf"):
        return True
    return False


def normalize_token(tok: str):
    stripped = tok.lstrip(">")
    was_glued_redirect = stripped != tok
    return stripped.strip("'\""), was_glued_redirect


def bash_touches_protected(command: str) -> bool:
    if not command:
        return False
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        tokens = command.split()

    verb_present = any(t in MUTATING_VERBS for t in tokens)

    for i, raw_tok in enumerate(tokens):
        norm_tok, was_glued_redirect = normalize_token(raw_tok)
        if not is_protected_path(norm_tok):
            continue
        if verb_present:
            return True
        if was_glued_redirect:
            return True
        if i > 0 and tokens[i - 1] in (">", ">>"):
            return True
    return False


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}
    blocked_reason = None

    if tool_name in ("Edit", "Write", "NotebookEdit"):
        file_path = tool_input.get("file_path", "") or tool_input.get("notebook_path", "")
        if is_protected_path(file_path):
            blocked_reason = (
                f"Blocked: '{file_path}' is a protected file.\n"
                "sop.md is the versioned source of truth - it must only change via an "
                "explicit, user-confirmed SOP version upgrade (archive the current version "
                "first, same as the v10->v12 process). acsResources/*.pdf files are retrieved "
                "evidence documents and must never be edited or overwritten.\n"
                "If the user has explicitly confirmed this exact change, ask them to run it "
                "themselves outside this session, or to temporarily remove the matching entry "
                "from .claude/settings.json."
            )
    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        if bash_touches_protected(command):
            blocked_reason = (
                f"Blocked: this command appears to overwrite, move, or delete a protected file "
                f"(sop.md or an acsResources/*.pdf evidence document):\n  {command}\n"
                "This guard exists because a prior session had a silent mv-based overwrite that "
                "destroyed an archived SOP version. If this is a genuine, user-confirmed SOP "
                "version upgrade or archival move, ask the user to confirm explicitly, then either "
                "have them run it directly outside this session, or temporarily remove the "
                "matching entry from .claude/settings.json."
            )

    if blocked_reason:
        print(blocked_reason, file=sys.stderr)
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
