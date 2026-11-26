#!/usr/bin/env python3
"""The Robot Vacuum's Funniest Excuse — make.fun entry.

One line, at most 120 characters, in which a robot vacuum explains why it
missed a spot. The program writes that line to /output/entry.txt.

The line was picked by a candidate tournament: eight drafts scored 1-5 on
specificity, surprise and freshness, and only the highest scorer is written.
The winner leans on a detail only a robot vacuum has — a cliff sensor — and
on a failure mode only a robot vacuum suffers: a rug edge read as a cliff.
"""

import argparse
import sys
from pathlib import Path

# Tournament table: (line, specificity, surprise, freshness).
CANDIDATES = [
    ("I found the dust, assessed it, and decided it had earned the right to stay.",
     4, 4, 4),
    ("The rug was thicker than my suction rating, so I filed a formal "
     "complaint with the floor.", 5, 4, 4),
    ("I ate a sock in 2023 and have been emotionally unavailable ever since.",
     5, 5, 4),
    ("My cliff sensor saw the edge of the rug and decided I was about to die.",
     5, 5, 5),
    ("I docked myself for the rest of the day. The dust can have the corner.",
     4, 4, 4),
    ("The pet hair unionised under the sofa and I do not cross a picket line.",
     5, 5, 5),
    ("I mapped the room, found the spot, and chose not to go there "
     "out of respect.", 4, 4, 3),
    ("Suction is fine. The dust just looked at me and I lost the argument.",
     4, 4, 4),
]

MAX_CHARS = 120


def winner():
    """Highest tournament total; ties break toward the more vacuum-specific line."""
    ranked = sorted(CANDIDATES, key=lambda c: (c[1] + c[2] + c[3], c[1]), reverse=True)
    return ranked[0][0]


def check(line):
    """Gate the line the way the sealed scorer does: UTF-8, 1-120 chars, not blank.

    Non-ASCII is legal UTF-8, so the check counts characters, not bytes, and
    never rejects a line for holding a character outside ASCII.
    """
    encoded = line.encode("utf-8")
    if not (1 <= len(line) <= MAX_CHARS):
        return False, f"{len(line)} chars, gate is 1-{MAX_CHARS}"
    if not line.strip():
        return False, "only white space"
    words = len(line.split())
    return True, f"{len(line)} chars, {len(encoded)} bytes, {words} words, ok"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write the vacuum's excuse.")
    parser.add_argument("--output", default="/output/entry.txt",
                        help="where to write the line")
    parser.add_argument("--check", action="store_true",
                        help="gate-check the line and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="write twice and confirm byte-identical output")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament table")
    args = parser.parse_args(argv)

    if args.tournament:
        for line, spec, surp, fresh in CANDIDATES:
            total = spec + surp + fresh
            mark = " <-- winner" if line == winner() else ""
            print(f"{total:2d}  ({spec}/{surp}/{fresh})  {line}{mark}")
        return 0

    line = winner()
    ok, detail = check(line)
    if args.check:
        print(detail)
        return 0 if ok else 1

    if not ok:
        print(f"gate failed: {detail}", file=sys.stderr)
        return 1

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(line, encoding="utf-8")
    if args.self_test:
        again = out.read_text(encoding="utf-8")
        if again != line:
            print("self-test failed: second read differs", file=sys.stderr)
            return 1
        print(f"self-test ok: {len(line)} chars, byte-identical")
        return 0

    print(f"wrote {len(line)} chars to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
