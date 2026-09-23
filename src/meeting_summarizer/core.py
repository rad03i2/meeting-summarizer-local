from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

WORD_RE = re.compile(r"[\w\u0600-\u06ff]+", re.UNICODE)
SPEAKER_RE = re.compile(r"^\s*([^:\n]{1,60}):\s*(.+)$")
TIMESTAMP_RE = re.compile(r"^\s*(?:\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*)")
STOP = {"the","a","an","and","or","to","of","in","on","for","is","are","was","were","we","i","you","it","this","that","with","be","as","at","من","في","على","إلى","الى","و","أو","او","هو","هي","هذا","هذه","أن","ان","تم","مع"}
ACTION_MARKERS = ("will ", "need to", "needs to", "action:", "todo", "follow up", "سوف", "سنقوم", "يجب", "مطلوب", "متابعة")
DECISION_MARKERS = ("decided", "agreed", "decision:", "approved", "we'll use", "قرر", "اتفق", "اعتمد", "تمت الموافقة")

@dataclass(frozen=True)
class Utterance:
    speaker: str
    text: str

@dataclass(frozen=True)
class Summary:
    overview: list[str]
    action_items: list[str]
    decisions: list[str]
    speakers: dict[str, int]
    keywords: list[str]
    utterance_count: int

    def to_dict(self) -> dict:
        return asdict(self)


def parse_transcript(text: str) -> list[Utterance]:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Transcript is empty")
    result: list[Utterance] = []
    current = "Unknown"
    for raw in text.splitlines():
        line = TIMESTAMP_RE.sub("", raw).strip()
        if not line:
            continue
        match = SPEAKER_RE.match(line)
        if match:
            current, body = match.group(1).strip(), match.group(2).strip()
            result.append(Utterance(current, body))
        elif result:
            previous = result[-1]
            result[-1] = Utterance(previous.speaker, previous.text + " " + line)
        else:
            result.append(Utterance(current, line))
    if not result:
        raise ValueError("Transcript contains no usable text")
    return result


def _tokens(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text) if len(w) > 2 and w.lower() not in STOP and not w.isdigit()]


def _sentences(items: Iterable[Utterance]) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for item in items:
        parts = re.split(r"(?<=[.!?؟])\s+", item.text)
        out.extend((item.speaker, p.strip()) for p in parts if p.strip())
    return out


def summarize(text: str, max_points: int = 5, keyword_count: int = 8) -> Summary:
    if max_points < 1 or keyword_count < 1:
        raise ValueError("max_points and keyword_count must be positive")
    utterances = parse_transcript(text)
    sentences = _sentences(utterances)
    freq = Counter(token for u in utterances for token in _tokens(u.text))
    scored = []
    for index, (speaker, sentence) in enumerate(sentences):
        tokens = _tokens(sentence)
        score = sum(freq[t] for t in set(tokens)) / max(len(tokens), 1)
        scored.append((score, index, f"{speaker}: {sentence}"))
    chosen = sorted(sorted(scored, reverse=True)[:max_points], key=lambda x: x[1])
    actions, decisions = [], []
    for speaker, sentence in sentences:
        lower = sentence.lower()
        rendered = f"{speaker}: {sentence}"
        if any(marker in lower for marker in ACTION_MARKERS):
            actions.append(rendered)
        if any(marker in lower for marker in DECISION_MARKERS):
            decisions.append(rendered)
    speakers = Counter(u.speaker for u in utterances)
    return Summary(
        overview=[x[2] for x in chosen],
        action_items=list(dict.fromkeys(actions)),
        decisions=list(dict.fromkeys(decisions)),
        speakers=dict(sorted(speakers.items())),
        keywords=[word for word, _ in freq.most_common(keyword_count)],
        utterance_count=len(utterances),
    )


def summarize_file(path: str | Path, **kwargs) -> Summary:
    source = Path(path)
    if not source.is_file():
        raise ValueError(f"Transcript not found: {source}")
    try:
        text = source.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Transcript must be UTF-8 text") from exc
    return summarize(text, **kwargs)
