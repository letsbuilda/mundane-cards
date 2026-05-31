#!/usr/bin/env python3
"""Fail if any card id collides once composed as ``set_id:id`` across every file in ``sets/``.

JSON Schema validates each file on its own; it cannot see across files. This is the cross-set
collision guard, enforced in CI so a duplicate id never reaches the backend. Standard library only,
so it runs on any Python 3 without installing anything.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SETS_DIR = Path(__file__).resolve().parent.parent / "sets"


def main() -> int:
    """Return 0 when all composed ids are unique, 1 (with a report) otherwise."""
    seen: dict[str, str] = {}
    dupes: list[str] = []

    for path in sorted(SETS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        set_id = data["set_id"]
        for card in data["cards"]:
            composed = f"{set_id}:{card['id']}"
            if composed in seen:
                dupes.append(f"{composed!r} in {path.name} (already defined in {seen[composed]})")
            else:
                seen[composed] = path.name

    if dupes:
        print("Duplicate composed card ids found:", file=sys.stderr)
        for line in dupes:
            print(f"  - {line}", file=sys.stderr)
        return 1

    print(f"OK: {len(seen)} unique composed card id(s) across {SETS_DIR.name}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
