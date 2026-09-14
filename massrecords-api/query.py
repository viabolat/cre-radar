#!/usr/bin/env python3
"""Quick CLI over the local capture API's /records endpoint.

Usage:
  ./query.py "SEAPORT"                  # name search
  ./query.py --book 12345 --page 67
  ./query.py --id 42                    # single record + parties
"""
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request

BASE = "http://localhost:8787"


def fetch(path: str) -> dict | list:
    with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as resp:
        return json.load(resp)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?", help="name substring to search")
    ap.add_argument("--book")
    ap.add_argument("--page")
    ap.add_argument("--type", dest="type_")
    ap.add_argument("--date-from")
    ap.add_argument("--date-to")
    ap.add_argument("--id", type=int, help="fetch one record by id, with parties")
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    try:
        if args.id is not None:
            data = fetch(f"/records/{args.id}")
        else:
            params = {
                "name": args.name,
                "book": args.book,
                "page": args.page,
                "type": args.type_,
                "date_from": args.date_from,
                "date_to": args.date_to,
                "limit": args.limit,
            }
            qs = urllib.parse.urlencode({k: v for k, v in params.items() if v})
            data = fetch(f"/records?{qs}")
    except urllib.error.URLError:
        print("Can't reach the local API on :8787 — run ./serve.sh first.")
        raise SystemExit(1)

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
