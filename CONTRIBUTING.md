# Contributing

Thanks for improving Meeting Summarizer Local.

1. Fork the repository and create a focused branch.
2. Use Python 3.10+ and install with `python -m pip install -e . pytest`.
3. Keep the core privacy-first and dependency-light; do not add network calls or telemetry without a clearly optional design and documentation.
4. Add or update tests for behavior changes, including Arabic/Unicode cases when relevant.
5. Run `python -m compileall -q src tests` and `pytest -q`.
6. Update both English and Arabic README sections when user-facing behavior changes.

Please keep pull requests small, explain the motivation, and never commit real confidential meeting transcripts, credentials, generated environments, or build artifacts.
