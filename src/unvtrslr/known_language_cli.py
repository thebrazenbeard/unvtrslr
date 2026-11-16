"""Operator CLI for installed, offline, known-language Argos text translation."""
from __future__ import annotations

import argparse
import json
import sys

from .known_language_runtime import (
    KnownLanguageError,
    MAX_SOURCE_CHARS,
    direct_routes,
    translate_known_text,
)


def main(argv: list[str] | None = None, *, provider=None) -> int:
    parser = argparse.ArgumentParser(
        description="Translate known-language text using installed EXTERNAL Argos models. "
        "Not UNVTRSLR native translation or a certified semantic result."
    )
    parser.add_argument("--from-lang", help="Explicit source language code (e.g. en)")
    parser.add_argument("--to-lang", help="Explicit target language code (e.g. fr)")
    parser.add_argument("--text", help="Source text; otherwise read stdin (preferred)")
    parser.add_argument("--allow-pivot", action="store_true", help="Opt into lossy multi-hop translation")
    parser.add_argument("--list-routes", action="store_true", help="List directly installed routes")
    parser.add_argument("--json", action="store_true", help="Structured output with provenance and route")
    args = parser.parse_args(argv)
    try:
        if args.list_routes:
            if args.from_lang or args.to_lang or args.text is not None or args.allow_pivot:
                parser.error("--list-routes cannot be combined with translation arguments")
            routes = direct_routes(provider=provider)
            if args.json:
                print(json.dumps({"provenance": "ARGOS_EXTERNAL_NOT_UNVTRSLR_NATIVE",
                                  "direct_routes": [{"source": a, "target": b} for a,b in routes]}))
            else:
                for frm, to in routes:
                    print(f"{frm}->{to}")
            return 0

        if not args.from_lang or not args.to_lang:
            parser.error("--from-lang and --to-lang are required for translation")
        if args.text is None:
            source_text = sys.stdin.read(MAX_SOURCE_CHARS + 1)
        else:
            source_text = args.text
        result = translate_known_text(
            args.from_lang, args.to_lang, source_text,
            allow_pivot=args.allow_pivot, provider=provider,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=True, allow_nan=False))
        else:
            print(result.translated_text)
            print(
                f"[{result.provenance}; route={'->'.join(result.route)}; "
                "meaning preservation not independently verified]",
                file=sys.stderr,
            )
        return 0
    except KnownLanguageError as exc:
        print(f"UNVTRSLR known-language translation unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
