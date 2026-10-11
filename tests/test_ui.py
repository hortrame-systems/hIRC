from __future__ import annotations

import io
import base64
import hashlib
import tempfile
import unittest
from contextlib import redirect_stdout
from html.parser import HTMLParser
from pathlib import Path

from hirc.cli import main
from hirc.projection import ProjectionError, build_briefing
from hirc.store import EventInput, Store
from hirc.ui import SCRIPT, STYLE, render_snapshot, write_snapshot


BASE = {
    "actor_id": "actor:owner",
    "category": "EVIDENCE",
    "foundation_version": "foundation:1",
    "goal_version": "goal:2",
    "privacy_class": "privacy:owner",
    "audience": "audience:owner",
    "purpose": "purpose:ui",
    "occurred_at": "2026-10-10T00:00:00Z",
}


class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.inline_handlers: list[tuple[str, str]] = []
        self.remote_attributes: list[tuple[str, str, str]] = []
        self.csp: str | None = None
        self.active: str | None = None
        self.script = ""
        self.style = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        for key, value in attrs:
            if key.lower().startswith("on"):
                self.inline_handlers.append((tag, key))
            if key in {"src", "action", "formaction"} and value:
                self.remote_attributes.append((tag, key, value))
            if key == "href" and value and not value.startswith("#"):
                self.remote_attributes.append((tag, key, value))
        if tag == "meta" and values.get("http-equiv") == "Content-Security-Policy":
            self.csp = values.get("content")
        if tag in {"script", "style"}:
            self.active = tag

    def handle_endtag(self, tag: str) -> None:
        if tag == self.active:
            self.active = None

    def handle_data(self, data: str) -> None:
        if self.active == "script":
            self.script += data
        elif self.active == "style":
            self.style += data


class UiSnapshotTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def fixture(self, directory: str, title: str = "Local work") -> tuple[Store, dict]:
        store = Store(Path(directory) / "ui.sqlite3")
        store.initialize()
        store.append(
            EventInput(
                stream_id="work:ui",
                event_type="work.created",
                payload={"work_id": "work:ui", "title": title, "owner": "actor:owner", "next_action": "Inspect"},
                **BASE,
            )
        )
        return store, build_briefing(store)

    def test_snapshot_is_deterministic_and_hostile_markup_stays_inert(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            _, briefing = self.fixture(directory, '<script>alert("x")</script>')
            first = render_snapshot(briefing)
            second = render_snapshot(briefing)
            self.assertEqual(first, second)
            self.assertNotIn('<script>alert("x")</script>', first)
            self.assertIn("&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;", first)
            self.assertNotIn("innerHTML", first)
            self.assertNotIn("eval(", first)
            self.assertIn("Content-Security-Policy", first)
            self.assertNotIn("http://", first)
            self.assertNotIn("https://", first)

    def test_snapshot_has_accessible_controls_and_information_boundary(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            _, briefing = self.fixture(directory)
            body = render_snapshot(briefing)
            for text in (
                'lang="en"',
                'href="#main"',
                'aria-label="Briefing navigation"',
                'id="back"',
                'id="forward"',
                'id="resume"',
                'label for="search"',
                'role="status"',
                "privacy:owner",
                "audience:owner",
                "purpose:ui",
                "Local read-only return briefing",
            ):
                self.assertIn(text, body)

    def test_cli_writes_the_same_atomic_snapshot(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            store, briefing = self.fixture(directory)
            direct = Path(directory) / "direct.html"
            cli = Path(directory) / "cli.html"
            direct_result = write_snapshot(briefing, direct)
            output = io.StringIO()
            with redirect_stdout(output):
                code = main(["--db", str(store.path), "ui-snapshot", "--output", str(cli)])
            self.assertEqual(code, 0)
            self.assertEqual(direct.read_bytes(), cli.read_bytes())
            self.assertEqual(direct_result["sha256"], __import__("json").loads(output.getvalue())["sha256"])

    def test_snapshot_rejects_wrong_schema(self) -> None:
        with self.assertRaises(ProjectionError):
            render_snapshot({"schema": "wrong", "work": [], "commitments": []})

    def test_parsed_surface_has_unique_ids_exact_hashes_and_no_active_external_edge(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            _, briefing = self.fixture(directory)
            parser = SurfaceParser()
            parser.feed(render_snapshot(briefing))
            script_hash = base64.b64encode(hashlib.sha256(SCRIPT.encode()).digest()).decode()
            style_hash = base64.b64encode(hashlib.sha256(STYLE.encode()).digest()).decode()
            self.assertEqual(parser.script, SCRIPT)
            self.assertEqual(parser.style, STYLE)
            self.assertEqual(len(parser.ids), len(set(parser.ids)))
            self.assertEqual(parser.inline_handlers, [])
            self.assertEqual(parser.remote_attributes, [])
            self.assertIn(f"script-src 'sha256-{script_hash}'", parser.csp or "")
            self.assertIn(f"style-src 'sha256-{style_hash}'", parser.csp or "")


if __name__ == "__main__":
    unittest.main()
