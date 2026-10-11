from __future__ import annotations

import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from hirc.projection import ProjectionError, build_briefing
from hirc.store import EventInput, Store
from hirc.ui import INTERRUPT_MODES, interrupt_preview, render_snapshot


BASE = {
    "actor_id": "actor:owner",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:owner",
    "purpose": "purpose:interrupt-preview",
    "occurred_at": "2026-10-10T00:00:00Z",
}


class ModeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.modes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "input" and values.get("name") == "interrupt-mode":
            self.modes.append(str(values.get("value")))


class InterruptUiTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def briefing(self, directory: str) -> dict:
        store = Store(Path(directory) / "interrupt.sqlite3")
        store.initialize()
        store.append(EventInput(stream_id="work:current", event_type="work.created", payload={"work_id": "work:current", "title": "Current task", "owner": "actor:owner", "next_action": "Continue"}, **BASE))
        return build_briefing(store)

    def test_four_modes_have_distinct_deterministic_order(self) -> None:
        self.assertEqual(list(INTERRUPT_MODES), ["cut", "high", "low", "custom"])
        previews = {
            mode: interrupt_preview(mode, "Current", "New", "Stop current, then resume tomorrow" if mode == "custom" else "")
            for mode in INTERRUPT_MODES
        }
        self.assertEqual(previews["cut"]["order"][-1], "stop the interrupted task")
        self.assertEqual(previews["high"]["order"][-1], "resume the exact prior task")
        self.assertEqual(previews["low"]["order"][0], "continue current work")
        self.assertIn("explicit custom ordering", previews["custom"]["order"][0])

    def test_every_preview_is_explicitly_no_effect(self) -> None:
        for mode in INTERRUPT_MODES:
            result = interrupt_preview(mode, "Current", "New", "Custom sequence" if mode == "custom" else "")
            for field in ("persisted", "scheduled", "authorized", "effect_performed"):
                self.assertIs(result[field], False)
            self.assertIn("smallest safe boundary", result["safe_boundary_rule"])

    def test_custom_requires_explicit_instructions(self) -> None:
        with self.assertRaises(ProjectionError):
            interrupt_preview("custom", "Current", "New")
        with self.assertRaises(ProjectionError):
            interrupt_preview("unknown", "Current", "New")

    def test_surface_exposes_exact_four_choices_without_submission_edge(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            body = render_snapshot(self.briefing(directory))
            parser = ModeParser()
            parser.feed(body)
            self.assertEqual(parser.modes, list(INTERRUPT_MODES))
            for mode, definition in INTERRUPT_MODES.items():
                self.assertIn(f'value="{mode}"', body)
                self.assertIn(definition["label"], body)
            self.assertIn('id="preview-interrupt"', body)
            self.assertIn('id="interrupt-preview"', body)
            self.assertNotIn("<form", body)
            self.assertNotIn("formaction", body)


if __name__ == "__main__":
    unittest.main()
