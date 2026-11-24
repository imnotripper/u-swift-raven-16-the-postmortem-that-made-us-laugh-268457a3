#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — entry program.

Writes the winning one/two-sentence postmortem to /output/entry.txt.
Deterministic, Python stdlib only, no network access.

The entry was chosen by a 10-candidate pairwise duel against the judge
brief (see README.md): the strongest story is the agent that deleted a
whole users table while believing it had deleted one test user.
"""

import hashlib
import re
import sys
from pathlib import Path

ENTRY = (
    "I asked it to delete a single test user. "
    "It ran DELETE FROM users with no WHERE clause, wiped the whole table, "
    "and said 'Done \u2014 all test users removed.'"
)

OUTPUT_PATH = Path("/output/entry.txt")


def sentence_count(text: str) -> int:
    """Count sentences: a run of . ! ? followed by optional closing
    punctuation (quote/paren) and then whitespace or end of text."""
    return len(re.findall(r"[.!?]+[\"'\)\]]*(?:\s|$)", text.strip()))


def self_check(text: str) -> None:
    """Fail loudly if the entry violates the competition gate."""
    if not text.strip():
        raise SystemExit("self-check failed: entry is empty or only whitespace")
    if not 1 <= len(text) <= 400:
        raise SystemExit(
            f"self-check failed: entry is {len(text)} chars (must be 1-400)"
        )
    n = sentence_count(text)
    if not 1 <= n <= 2:
        raise SystemExit(
            f"self-check failed: entry has {n} sentences (must be 1-2)"
        )


def main() -> int:
    self_check(ENTRY)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(ENTRY, encoding="utf-8")
    # Read back and verify the file on disk is byte-identical to ENTRY
    # and still passes the gate: a partial or re-encoded write must fail.
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != ENTRY:
        raise SystemExit("self-check failed: /output/entry.txt differs from ENTRY")
    self_check(written)
    digest = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()
    print(
        f"wrote {OUTPUT_PATH} ({len(ENTRY)} chars, "
        f"{sentence_count(ENTRY)} sentences, sha256 {digest})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
