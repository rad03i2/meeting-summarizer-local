import json
from pathlib import Path
from meeting_summarizer.core import parse_transcript, summarize, summarize_file
from meeting_summarizer.cli import main, markdown

SAMPLE = """[09:00] Alice: We agreed to ship the report Friday.
09:01 Bob: I will update the dashboard tomorrow.
Alice: The dashboard needs the new air quality metrics.
رضوان: يجب مراجعة النتائج قبل النشر.
رضوان: اتفق الفريق على اعتماد النسخة الجديدة.
"""

def test_parse_speakers_and_timestamps():
    rows = parse_transcript(SAMPLE)
    assert rows[0].speaker == "Alice"
    assert rows[1].speaker == "Bob"
    assert rows[-1].speaker == "رضوان"

def test_summary_extracts_actions_decisions_and_arabic():
    result = summarize(SAMPLE, max_points=3, keyword_count=5)
    assert len(result.overview) == 3
    assert any("Bob" in x for x in result.action_items)
    assert any("رضوان" in x for x in result.action_items)
    assert any("agreed" in x for x in result.decisions)
    assert any("اتفق" in x for x in result.decisions)
    assert result.speakers["رضوان"] == 2

def test_continuation_line_is_joined():
    rows = parse_transcript("Sam: First line\ncontinues here")
    assert rows[0].text == "First line continues here"

def test_invalid_inputs():
    for value in ("", "   \n"):
        try: summarize(value)
        except ValueError: pass
        else: raise AssertionError("expected ValueError")
    try: summarize("A: hi", max_points=0)
    except ValueError: pass
    else: raise AssertionError("expected ValueError")

def test_file_and_markdown(tmp_path: Path):
    p = tmp_path / "meeting.txt"
    p.write_text(SAMPLE, encoding="utf-8")
    result = summarize_file(p)
    report = markdown(result, "Sprint")
    assert "# Sprint" in report and "## Action items" in report

def test_cli_json_output(tmp_path: Path):
    src = tmp_path / "in.txt"; out = tmp_path / "out.json"
    src.write_text(SAMPLE, encoding="utf-8")
    assert main([str(src), "--format", "json", "-o", str(out)]) == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["utterance_count"] == 5

def test_cli_missing_file():
    assert main(["definitely-missing.txt"]) == 2
