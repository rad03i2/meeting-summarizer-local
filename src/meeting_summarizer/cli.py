from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .core import Summary, summarize_file

VERSION = "1.0.0"
AUTHOR = "Radwan Abdulhadi Ahmed / رضوان عبدالهادي أحمد / @rad03i2"


def markdown(summary: Summary, title: str = "Meeting Summary") -> str:
    lines = [f"# {title}", "", "## Overview"]
    lines += [f"- {x}" for x in summary.overview] or ["- No summary points found."]
    lines += ["", "## Action items"] + ([f"- {x}" for x in summary.action_items] or ["- None detected."])
    lines += ["", "## Decisions"] + ([f"- {x}" for x in summary.decisions] or ["- None detected."])
    lines += ["", "## Speakers"] + [f"- {name}: {count} utterance(s)" for name, count in summary.speakers.items()]
    lines += ["", "## Keywords", ", ".join(summary.keywords) or "None", ""]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="meeting-summary", description="Summarize UTF-8 meeting transcripts locally.")
    p.add_argument("transcript", nargs="?", help="Path to a UTF-8 .txt/.md transcript")
    p.add_argument("--format", choices=("markdown", "json"), default="markdown")
    p.add_argument("--output", "-o", help="Write report to this path")
    p.add_argument("--max-points", type=int, default=5)
    p.add_argument("--keywords", type=int, default=8)
    p.add_argument("--title", default="Meeting Summary")
    p.add_argument("--version", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.version:
        print(f"meeting-summarizer-local {VERSION} — {AUTHOR}")
        return 0
    if not args.transcript:
        print("error: transcript path is required", file=sys.stderr)
        return 2
    try:
        summary = summarize_file(args.transcript, max_points=args.max_points, keyword_count=args.keywords)
        output = json.dumps(summary.to_dict(), ensure_ascii=False, indent=2) + "\n" if args.format == "json" else markdown(summary, args.title)
        if args.output:
            target = Path(args.output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(output, encoding="utf-8")
        else:
            print(output, end="" if output.endswith("\n") else "\n")
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
