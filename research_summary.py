"""Small demo utility for summarizing short research notes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "could",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "will",
    "with",
}


def extract_keywords(notes: list[str], limit: int = 5) -> list[str]:
    """Return the most frequent non-trivial keywords across the notes."""
    tokens = []
    for note in notes:
        words = re.findall(r"[a-zA-Z]{3,}", note.lower())
        tokens.extend(word for word in words if word not in STOPWORDS)

    counts = Counter(tokens)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _count in ranked[:limit]]


def summarize_notes(notes: list[str], keyword_limit: int = 5) -> dict[str, object]:
    """Build a small structured summary for a collection of notes."""
    if not notes:
        raise ValueError("at least one research note is required")

    cleaned_notes = [note.strip() for note in notes if note.strip()]
    if not cleaned_notes:
        raise ValueError("at least one non-empty research note is required")

    keywords = extract_keywords(cleaned_notes, limit=keyword_limit)
    lead_sentence = cleaned_notes[0].rstrip(".")
    summary = (
        f"{len(cleaned_notes)} notes analyzed. "
        f"Lead note: {lead_sentence}. "
        f"Top keywords: {', '.join(keywords)}."
    )

    return {
        "note_count": len(cleaned_notes),
        "keywords": keywords,
        "summary": summary,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize short research notes into a JSON payload."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="maximum number of keywords to return",
    )
    parser.add_argument("notes", nargs="*", help="research notes to summarize")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not args.notes:
        print("at least one research note is required", file=sys.stderr)
        return 1

    if args.limit < 1:
        print("--limit must be greater than 0", file=sys.stderr)
        return 1

    try:
        payload = summarize_notes(args.notes, keyword_limit=args.limit)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
