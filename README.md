# Codex GitHub Demo

This is a tiny, dependency-free demo that shows how to use Codex with a GitHub repository.

## Files

- `research_summary.py`: a simple CLI that turns research notes into a JSON summary.
- `tests/test_research_summary.py`: unit tests that Codex can run after making changes.
- `AGENTS.md`: project rules and review guidance that Codex will follow.

## Run locally

```bash
python research_summary.py --limit 3 "Codex can edit code." "GitHub comments can trigger review."
python -m unittest discover -s tests -p "test_*.py"
```

## Example Codex prompts

Use prompts like these after your GitHub repository is connected to Codex:

```text
Read AGENTS.md, run the tests, and improve the keyword extraction so generic words are filtered more aggressively.
```

```text
Review the pull request and focus on keyword ranking and CLI error handling.
```

```text
Refactor research_summary.py to make the summary sentence easier to extend, but keep all tests passing.
```
