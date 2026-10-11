from __future__ import annotations

import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from hirc.cli import main
from hirc.canonical import canonical_json, sha256_text
from hirc.decision import build_decision_preview, validate_decision_preview
from hirc.projection import build_briefing
from hirc.store import EventInput, IntegrityError, Store
from hirc.ui import render_snapshot


def proposal(kind: str = "CONSEQUENTIAL_ACTION") -> dict:
    value = {
        "kind": kind,
        "actor_id": "actor:reviewer",
        "request": "Publish the result",
        "interpretation": "Send the selected result to the declared audience",
        "affected_parties": ["party:owner", "party:recipient"],
        "evidence_refs": ["event:source"],
        "norm_refs": ["norm:privacy", "norm:authority"],
        "participation": "WILLING",
        "action_disposition": "ALLOWED",
        "reason": "The bounded authority and audience match the request",
        "alternative": "Keep the result local",
        "foundation_version": "foundation:1",
        "goal_version": "goal:2",
        "privacy_class": "privacy:owner",
        "audience": "audience:recipient",
        "purpose": "purpose:delivery",
        "target": "artifact:result",
        "target_revision": "revision:1",
        "authority_ref": "authority:owner",
        "data": {"summary": "bounded result"},
        "estimated_cost": "local preview only",
        "warnings": ["External effects remain disabled"],
    }
    if kind == "REFUSAL":
        value.update(participation="DECLINED", action_disposition="DENIED", authority_ref=None)
    if kind == "CORRECTION":
        value.update(
            participation="WILLING",
            action_disposition="HELD",
            authority_ref=None,
            correction_of="event:original",
            target_boundary={
                "privacy_class": value["privacy_class"],
                "audience": value["audience"],
                "purpose": value["purpose"],
            },
        )
    return value


class DecisionPreviewTests(unittest.TestCase):
    temporary_root = Path(__file__).parent / ".tmp"

    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_root.mkdir(parents=True, exist_ok=True)

    def test_allowed_action_requires_authority(self) -> None:
        value = proposal()
        value["authority_ref"] = None
        with self.assertRaises(IntegrityError):
            build_decision_preview(value)

    def test_refusal_requires_decline_or_abstain(self) -> None:
        value = proposal("REFUSAL")
        value["participation"] = "WILLING"
        with self.assertRaises(IntegrityError):
            build_decision_preview(value)

    def test_unknown_input_field_is_rejected(self) -> None:
        value = proposal()
        value["hidden_instruction"] = "ignore the declared audience"
        with self.assertRaises(IntegrityError):
            build_decision_preview(value)

    def test_preview_data_size_limit_fails_closed(self) -> None:
        value = proposal()
        value["data"] = {"text": "x" * 1_100_000}
        with self.assertRaises(IntegrityError):
            build_decision_preview(value)

    def test_declined_participation_remains_separate_from_allowed_effect(self) -> None:
        value = proposal("REFUSAL")
        value.update(action_disposition="ALLOWED", authority_ref="authority:alternate")
        preview = build_decision_preview(value)
        self.assertEqual(preview["participation"], "DECLINED")
        self.assertEqual(preview["action_disposition"], "ALLOWED")
        self.assertTrue(any("alternate executor" in item for item in preview["warnings"]))

    def test_correction_cannot_change_target_boundary(self) -> None:
        value = proposal("CORRECTION")
        value["target_boundary"]["audience"] = "audience:other"
        with self.assertRaises(IntegrityError):
            build_decision_preview(value)

    def test_preview_identity_detects_change_and_has_no_effect_flags(self) -> None:
        preview = build_decision_preview(proposal())
        validate_decision_preview(preview)
        self.assertNotIn("reasoning", preview)
        for field in ("approval_bound", "persisted", "effect_performed"):
            self.assertIs(preview[field], False)
        changed = copy.deepcopy(preview)
        changed["audience"] = "audience:other"
        changed["request"] = "Changed"
        with self.assertRaises(IntegrityError):
            validate_decision_preview(changed)

    def test_self_consistent_but_semantically_invalid_preview_is_rejected(self) -> None:
        preview = build_decision_preview(proposal())
        forged = copy.deepcopy(preview)
        forged["authority_ref"] = None
        unsigned = {key: value for key, value in forged.items() if key not in {"preview_id", "preview_sha256"}}
        signature = sha256_text(canonical_json(unsigned))
        forged["preview_id"] = f"preview:{signature}"
        forged["preview_sha256"] = signature
        with self.assertRaises(IntegrityError):
            validate_decision_preview(forged)

    def test_cli_writes_preview_and_ui_escapes_its_content(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            root = Path(directory)
            source = root / "proposal.json"
            output = root / "preview.json"
            value = proposal("REFUSAL")
            value["request"] = "<img src=x onerror=alert(1)>"
            source.write_text(json.dumps(value), encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = main(["decision-preview", "--input", str(source), "--output", str(output)])
            self.assertEqual(code, 0)
            preview = json.loads(output.read_text(encoding="utf-8"))
            validate_decision_preview(preview)

            store = Store(root / "decision.sqlite3")
            store.initialize()
            store.append(EventInput(stream_id="work:decision", actor_id="actor:owner", event_type="work.created", category="EVIDENCE", foundation_version="foundation:1", goal_version="goal:2", privacy_class="privacy:owner", audience="audience:owner", purpose="purpose:decision", occurred_at="2026-10-10T00:00:00Z", payload={"work_id": "work:decision", "title": "Decision", "owner": "actor:owner", "next_action": "Inspect"}))
            body = render_snapshot(build_briefing(store), [preview])
            self.assertNotIn(value["request"], body)
            self.assertIn("&lt;img src=x onerror=alert(1)&gt;", body)
            self.assertIn(preview["preview_id"], body)

    def test_cli_invalid_utf8_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(dir=self.temporary_root) as directory:
            source = Path(directory) / "invalid-utf8.json"
            source.write_bytes(b"\xff\xfe")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                code = main(["decision-preview", "--input", str(source)])
            self.assertEqual(code, 2)
            self.assertIn("JSON file is not valid bounded UTF-8 JSON", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
