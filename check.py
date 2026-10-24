#!/usr/bin/env python3
"""Check deals.json: valid JSON, every field present, unique ids, no expired deals."""
import datetime
import json
import re
import sys

FIELDS = {"id", "store", "domain", "deal", "how", "url", "expires", "updated"}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def main() -> int:
    try:
        with open("deals.json", encoding="utf-8") as f:
            feed = json.load(f)
    except (OSError, ValueError) as e:
        print(f"deals.json: {e}")
        return 1
    errors = []
    deals = feed.get("deals")
    if not isinstance(deals, list):
        errors.append("`deals` must be a list")
        deals = []
    if not DATE.match(str(feed.get("updated", ""))):
        errors.append("`updated` must be YYYY-MM-DD")
    today = datetime.date.today().isoformat()
    seen = set()
    for i, d in enumerate(deals):
        where = f"deal {i} ({d.get('id', '?')})" if isinstance(d, dict) else f"deal {i}"
        if not isinstance(d, dict):
            errors.append(f"{where}: must be an object")
            continue
        missing = FIELDS - d.keys()
        extra = d.keys() - FIELDS
        if missing:
            errors.append(f"{where}: missing {sorted(missing)}")
        if extra:
            errors.append(f"{where}: unknown {sorted(extra)}")
        if d.get("id") in seen:
            errors.append(f"{where}: id used twice")
        seen.add(d.get("id"))
        for k in ("id", "store", "domain", "deal", "how", "url"):
            if not isinstance(d.get(k), str) or not d.get(k).strip():
                errors.append(f"{where}: `{k}` must be non-empty text")
        if not str(d.get("url", "")).startswith("https://"):
            errors.append(f"{where}: `url` must start with https://")
        if d.get("domain", "").startswith("www.") or "/" in str(d.get("domain", "")):
            errors.append(f"{where}: `domain` is a bare host, no www. or path")
        if not DATE.match(str(d.get("updated", ""))):
            errors.append(f"{where}: `updated` must be YYYY-MM-DD")
        exp = d.get("expires")
        if exp is not None:
            if not DATE.match(str(exp)):
                errors.append(f"{where}: `expires` must be YYYY-MM-DD or null")
            elif exp < today:
                errors.append(f"{where}: expired on {exp}; remove it or extend it")
    for e in errors:
        print(e)
    print(f"{len(deals)} deals, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
