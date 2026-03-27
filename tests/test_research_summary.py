import json
import subprocess
import sys
import unittest
from pathlib import Path

from research_summary import extract_keywords, summarize_notes


ROOT = Path(__file__).resolve().parents[1]


class ResearchSummaryTests(unittest.TestCase):
    def test_extract_keywords_orders_by_frequency_then_name(self) -> None:
        notes = [
            "Agents help research teams move faster.",
            "Research teams use agents for synthesis.",
            "Automation helps teams review research findings.",
        ]

        self.assertEqual(
            extract_keywords(notes, limit=4),
            ["research", "teams", "agents", "automation"],
        )

    def test_summarize_notes_requires_non_empty_input(self) -> None:
        with self.assertRaises(ValueError):
            summarize_notes([])

        with self.assertRaises(ValueError):
            summarize_notes(["   ", "\n"])

    def test_cli_returns_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "research_summary.py"),
                "--limit",
                "2",
                "Codex can automate code review.",
                "GitHub comments can start cloud tasks.",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(payload["note_count"], 2)
        self.assertEqual(len(payload["keywords"]), 2)
        self.assertIn("summary", payload)
        self.assertTrue(payload["summary"].startswith("2 notes analyzed."))

    def test_cli_rejects_invalid_limit(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "research_summary.py"),
                "--limit",
                "0",
                "Codex can automate code review.",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("--limit must be greater than 0", result.stderr)


if __name__ == "__main__":
    unittest.main()
