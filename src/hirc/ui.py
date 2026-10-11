"""Self-contained, read-only local HTML snapshot for verified hIRC briefings."""

from __future__ import annotations

import base64
import hashlib
import html
import os
import tempfile
from pathlib import Path
from typing import Any

from .canonical import canonical_json
from .decision import validate_decision_preview
from .projection import ProjectionError


INTERRUPT_MODES = {
    "cut": {
        "label": "Interrupt and cut",
        "order": ("checkpoint current work", "run the new task", "stop the interrupted task"),
        "return_behavior": "Do not return automatically; leave the interrupted task visible with its remaining state.",
    },
    "high": {
        "label": "Interrupt with high priority",
        "order": ("checkpoint current work", "suspend current work", "run the new task", "resume the exact prior task"),
        "return_behavior": "Return automatically after the new task reaches its declared completion boundary.",
    },
    "low": {
        "label": "Interrupt with low priority",
        "order": ("continue current work", "queue the new task", "run it at the current task's declared completion boundary"),
        "return_behavior": "Do not interrupt the current task.",
    },
    "custom": {
        "label": "Custom",
        "order": ("apply the explicit custom ordering at the smallest safe boundary",),
        "return_behavior": "Use only the stated pause, cancellation and resumption behavior; do not infer missing effects.",
    },
}


def interrupt_preview(mode: str, current_work: str, new_task: str, custom: str = "") -> dict[str, Any]:
    if mode not in INTERRUPT_MODES:
        raise ProjectionError("unknown interruption mode")
    if not isinstance(current_work, str) or not current_work.strip():
        raise ProjectionError("interruption preview requires current work")
    if not isinstance(new_task, str) or not new_task.strip():
        raise ProjectionError("interruption preview requires a new task")
    if mode == "custom" and (not isinstance(custom, str) or not custom.strip()):
        raise ProjectionError("custom interruption preview requires explicit instructions")
    selected = INTERRUPT_MODES[mode]
    return {
        "schema": "hirc.interruption-preview/1",
        "mode": mode,
        "label": selected["label"],
        "current_work": current_work,
        "new_task": new_task,
        "order": list(selected["order"]),
        "return_behavior": selected["return_behavior"],
        "custom": custom.strip() if mode == "custom" else None,
        "safe_boundary_rule": "If an immediate cut would interrupt an unsafe in-flight effect, wait for the smallest safe boundary and explain the delay.",
        "persisted": False,
        "scheduled": False,
        "authorized": False,
        "effect_performed": False,
    }


STYLE = """
:root{color-scheme:dark;--bg:#101418;--panel:#182028;--ink:#f4f7f9;--muted:#a9b7c3;--line:#31404c;--accent:#7dd3fc;--held:#fbbf24;--blocked:#fb7185;--ok:#86efac;font:16px/1.45 system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink)}button,input,textarea{font:inherit}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:var(--ink);color:var(--bg);padding:.6rem;z-index:5}header{position:sticky;top:0;background:#101418f2;border-bottom:1px solid var(--line);padding:.8rem 1rem;z-index:3}.toolbar{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}.toolbar button,.toolbar input,.interrupt button,.interrupt input,.interrupt textarea{border:1px solid var(--line);border-radius:.45rem;background:var(--panel);color:var(--ink);padding:.55rem .7rem}.toolbar button:focus-visible,.toolbar input:focus-visible,.interrupt button:focus-visible,.interrupt input:focus-visible,.interrupt textarea:focus-visible,a:focus-visible{outline:3px solid var(--accent);outline-offset:2px}.toolbar label{color:var(--muted)}.layout{display:grid;grid-template-columns:minmax(12rem,18rem) minmax(0,1fr);gap:1rem;max-width:90rem;margin:auto;padding:1rem}.panel,.work-card,.interrupt{background:var(--panel);border:1px solid var(--line);border-radius:.65rem;padding:1rem}.panel{align-self:start}.work-list{display:grid;gap:.8rem}.work-card[hidden]{display:none}.work-card:target,.work-card[data-selected=true]{border-color:var(--accent);box-shadow:0 0 0 2px #7dd3fc44}.status{font-weight:700}.status-HELD{color:var(--held)}.status-BLOCKED{color:var(--blocked)}.status-OPEN,.status-ACTIVE{color:var(--ok)}.meta{display:grid;grid-template-columns:max-content 1fr;gap:.25rem .7rem}.meta dt{color:var(--muted)}.meta dd{margin:0;overflow-wrap:anywhere}.sources{font-family:ui-monospace,monospace;font-size:.85rem;overflow-wrap:anywhere}.empty{color:var(--muted)}.interrupt{max-width:90rem;margin:0 auto 1rem}.interrupt fieldset{border:1px solid var(--line);border-radius:.45rem;display:grid;gap:.45rem;margin:.7rem 0;padding:.7rem}.interrupt .field{display:grid;gap:.25rem;margin:.6rem 0}.interrupt input[type=text],.interrupt textarea{width:100%}.interrupt-preview{border-left:4px solid var(--accent);margin-top:.8rem;padding:.7rem;min-height:3rem}.no-effect{color:var(--muted)}footer{max-width:90rem;margin:auto;padding:0 1rem 1.5rem;color:var(--muted)}@media(max-width:44rem){.layout{grid-template-columns:1fr}header{position:static}}@media(prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
""".strip()

SCRIPT = """
(()=>{"use strict";const cards=[...document.querySelectorAll(".work-card")],search=document.getElementById("search"),announcer=document.getElementById("announcer"),custom=document.getElementById("custom-order"),preview=document.getElementById("interrupt-preview");function selectedCard(){return cards.find(card=>card.dataset.selected==="true")||cards.find(card=>card.dataset.runnable==="true"&&!card.hidden)||cards[0]||null}function selectRoute(){const route=decodeURIComponent(location.hash.slice(1));let selected=null;for(const card of cards){const active=route&&card.dataset.route===route;card.dataset.selected=active?"true":"false";if(active)selected=card}if(selected){selected.scrollIntoView({block:"start"});selected.focus({preventScroll:true})}}function filter(){const query=search.value.trim().toLocaleLowerCase();let visible=0;for(const card of cards){const match=!query||card.textContent.toLocaleLowerCase().includes(query);card.hidden=!match;if(match)visible++}announcer.textContent=visible+" work item"+(visible===1?"":"s")+" shown"}function mode(){return document.querySelector('input[name="interrupt-mode"]:checked')}function syncCustom(){custom.disabled=!mode()||mode().value!=="custom"}function line(label,value){const p=document.createElement("p"),strong=document.createElement("strong");strong.textContent=label+": ";p.append(strong,document.createTextNode(value));return p}function previewInterrupt(){const selected=mode(),task=document.getElementById("new-task").value.trim(),current=selectedCard();preview.replaceChildren();if(!selected||!task||!current){preview.append(line("Held","Select current work, enter the new task and choose one mode."));return}if(selected.value==="custom"&&!custom.value.trim()){preview.append(line("Held","Custom requires explicit ordering, pause, cancellation and resumption instructions."));return}preview.append(line("Choice",selected.dataset.label),line("Current work",current.dataset.title),line("New task",task),line("Order",selected.dataset.order),line("Return",selected.dataset.return));if(selected.value==="custom")preview.append(line("Custom",custom.value.trim()));preview.append(line("Safe boundary","An unsafe in-flight effect waits for the smallest safe boundary and explains the delay."),line("No effect","Preview only: nothing is saved, scheduled, sent, authorized or executed."))}document.getElementById("back").addEventListener("click",()=>history.back());document.getElementById("forward").addEventListener("click",()=>history.forward());document.getElementById("resume").addEventListener("click",()=>{const card=cards.find(item=>item.dataset.runnable==="true"&&!item.hidden);if(card){history.pushState(null,"","#"+encodeURIComponent(card.dataset.route));selectRoute();announcer.textContent="Resumed "+card.dataset.title}else{announcer.textContent="No runnable work item"}});for(const link of document.querySelectorAll("[data-work-link]")){link.addEventListener("click",event=>{event.preventDefault();history.pushState(null,"",link.getAttribute("href"));selectRoute()})}for(const choice of document.querySelectorAll('input[name="interrupt-mode"]'))choice.addEventListener("change",syncCustom);document.getElementById("preview-interrupt").addEventListener("click",previewInterrupt);search.addEventListener("input",filter);addEventListener("popstate",selectRoute);addEventListener("hashchange",selectRoute);syncCustom();filter();selectRoute()})();
""".strip()


def _digest_token(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _csp_hash(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")


def _text(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _list_text(values: list[str]) -> str:
    return ", ".join(values) if values else "none"


def render_snapshot(briefing: dict[str, Any], decision_previews: list[dict[str, Any]] | None = None) -> str:
    if briefing.get("schema") != "hirc.return-briefing/1":
        raise ProjectionError("UI snapshot requires a hirc.return-briefing/1 input")
    work = briefing.get("work")
    commitments = briefing.get("commitments")
    if not isinstance(work, list) or not isinstance(commitments, list):
        raise ProjectionError("UI snapshot requires work and commitment lists")

    owners = sorted(
        {
            str(item.get("owner"))
            for item in [*work, *commitments]
            if isinstance(item, dict) and isinstance(item.get("owner"), str)
        }
    )
    roster = "".join(f"<li>{_text(owner)}</li>" for owner in owners) or '<li class="empty">No explicit owners</li>'
    navigation: list[str] = []
    cards: list[str] = []
    for item in sorted(work, key=lambda row: str(row.get("work_id", ""))):
        if not isinstance(item, dict):
            raise ProjectionError("work rows must be objects")
        required = ("work_id", "title", "owner", "status", "next_action", "information_boundary", "source_events")
        if any(key not in item for key in required):
            raise ProjectionError("work row is incomplete for UI rendering")
        route = str(item["work_id"])
        token = _digest_token(route)
        title = str(item["title"])
        status = str(item["status"])
        runnable = status in {"OPEN", "ACTIVE"} and not item.get("active_holds") and not item.get("blocked_by")
        navigation.append(
            f'<li><a data-work-link href="#{_text(route)}">{_text(title)}</a> <span class="status status-{_text(status)}">{_text(status)}</span></li>'
        )
        boundary = item["information_boundary"]
        sources = item["source_events"]
        if not isinstance(boundary, dict) or not isinstance(sources, dict):
            raise ProjectionError("work boundary and source events must be objects")
        cards.append(
            "".join(
                [
                    f'<article class="work-card" id="work-{token}" tabindex="-1" data-route="{_text(route)}" data-title="{_text(title)}" data-runnable="{str(runnable).lower()}">',
                    f'<h2>{_text(title)}</h2><p class="status status-{_text(status)}">{_text(status)}</p>',
                    '<dl class="meta">',
                    f'<dt>Work ID</dt><dd>{_text(route)}</dd>',
                    f'<dt>Owner</dt><dd>{_text(item["owner"])}</dd>',
                    f'<dt>Next action</dt><dd>{_text(item["next_action"])}</dd>',
                    f'<dt>Dependencies</dt><dd>{_text(_list_text(list(item.get("dependencies", []))))}</dd>',
                    f'<dt>Active holds</dt><dd>{_text(_list_text(list(item.get("active_holds", []))))}</dd>',
                    f'<dt>Blocked by</dt><dd>{_text(_list_text(list(item.get("blocked_by", []))))}</dd>',
                    f'<dt>Privacy</dt><dd>{_text(boundary.get("privacy_class", "unknown"))}</dd>',
                    f'<dt>Audience</dt><dd>{_text(boundary.get("audience", "unknown"))}</dd>',
                    f'<dt>Purpose</dt><dd>{_text(boundary.get("purpose", "unknown"))}</dd>',
                    '</dl><h3>Source events</h3>',
                    '<ul class="sources">'
                    + "".join(f'<li>{_text(key)}: {_text(value)}</li>' for key, value in sorted(sources.items()))
                    + "</ul></article>",
                ]
            )
        )
    card_body = "".join(cards) or '<p class="empty">No work items</p>'
    mode_controls = []
    for index, (mode, definition) in enumerate(INTERRUPT_MODES.items()):
        order = " → ".join(definition["order"])
        mode_controls.append(
            f'<label><input type="radio" name="interrupt-mode" value="{_text(mode)}" data-label="{_text(definition["label"])}" data-order="{_text(order)}" data-return="{_text(definition["return_behavior"])}"{" checked" if index == 0 else ""}> {_text(definition["label"])}</label>'
        )
    decision_cards: list[str] = []
    for preview in decision_previews or []:
        validate_decision_preview(preview)
        boundary = preview["information_boundary"]
        decision_cards.append(
            "".join(
                [
                    '<article class="decision-card">',
                    f'<h3>{_text(preview["kind"])}</h3>',
                    f'<p class="sources">{_text(preview["preview_id"])}</p>',
                    '<dl class="meta">',
                    f'<dt>Request</dt><dd>{_text(preview["request"])}</dd>',
                    f'<dt>Interpretation</dt><dd>{_text(preview["interpretation"])}</dd>',
                    f'<dt>Participation</dt><dd>{_text(preview["participation"])}</dd>',
                    f'<dt>Action</dt><dd>{_text(preview["action_disposition"])}</dd>',
                    f'<dt>Reason</dt><dd>{_text(preview["reason"])}</dd>',
                    f'<dt>Alternative</dt><dd>{_text(preview["alternative"] or "none")}</dd>',
                    f'<dt>Target</dt><dd>{_text(preview["target"])} @ {_text(preview["target_revision"])}</dd>',
                    f'<dt>Authority</dt><dd>{_text(preview["authority_ref"] or "none")}</dd>',
                    f'<dt>Privacy</dt><dd>{_text(boundary["privacy_class"])}</dd>',
                    f'<dt>Audience</dt><dd>{_text(boundary["audience"])}</dd>',
                    f'<dt>Purpose</dt><dd>{_text(boundary["purpose"])}</dd>',
                    f'<dt>Cost</dt><dd>{_text(preview["estimated_cost"])}</dd>',
                    '</dl>',
                    '<p class="no-effect">Preview only: no participation consent, bound approval, persistence or effect.</p>',
                    '<h4>Warnings</h4><ul>'
                    + ("".join(f'<li>{_text(item)}</li>' for item in preview["warnings"]) or '<li class="empty">none</li>')
                    + '</ul><h4>Evidence</h4><ul class="sources">'
                    + "".join(f'<li>{_text(item)}</li>' for item in preview["evidence_refs"])
                    + '</ul></article>',
                ]
            )
        )
    decision_body = "".join(decision_cards) or '<p class="empty">No bound decision preview supplied.</p>'
    csp = (
        "default-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'; "
        f"style-src 'sha256-{_csp_hash(STYLE)}'; script-src 'sha256-{_csp_hash(SCRIPT)}'"
    )
    head = _text(str(briefing.get("store_head", "unknown")))
    count = _text(str(briefing.get("event_count", "unknown")))
    return "".join(
        [
            "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">",
            '<meta name="viewport" content="width=device-width,initial-scale=1">',
            f'<meta http-equiv="Content-Security-Policy" content="{_text(csp)}">',
            "<title>hIRC local return briefing</title>",
            f"<style>{STYLE}</style></head><body>",
            '<a class="skip" href="#main">Skip to work</a><header><div class="toolbar" role="navigation" aria-label="Briefing navigation">',
            '<button id="back" type="button">Back</button><button id="forward" type="button">Forward</button><button id="resume" type="button">Resume</button>',
            '<label for="search">Search work</label><input id="search" type="search" autocomplete="off">',
            '<span id="announcer" role="status" aria-live="polite"></span></div></header>',
            '<div class="layout"><aside class="panel" aria-label="Roster and work index">',
            f"<h1>hIRC</h1><p>Local read-only return briefing</p><p>{count} verified source events</p>",
            f'<p class="sources">Store head: {head}</p><h2>Roster</h2><ul>{roster}</ul><h2>Work</h2><ul>{"".join(navigation)}</ul>',
            f'</aside><main id="main" class="work-list">{card_body}</main></div>',
            '<section class="interrupt" aria-labelledby="interrupt-heading"><h2 id="interrupt-heading">Interrupt busy work</h2>',
            '<p>Choose a local preview. The current selection is used as the interrupted task.</p>',
            '<div class="field"><label for="new-task">New task</label><input id="new-task" type="text" autocomplete="off"></div>',
            f'<fieldset><legend>Priority and return behavior</legend>{"".join(mode_controls)}</fieldset>',
            '<div class="field"><label for="custom-order">Custom ordering, pause, cancellation and resumption</label><textarea id="custom-order" rows="3" disabled></textarea></div>',
            '<button id="preview-interrupt" type="button">Preview interruption</button>',
            '<p class="no-effect">Preview only. Nothing is saved, scheduled, sent, authorized or executed.</p>',
            '<div id="interrupt-preview" class="interrupt-preview" role="status" aria-live="polite" aria-atomic="true"></div></section>',
            f'<section class="interrupt" aria-labelledby="decision-heading"><h2 id="decision-heading">Inspect refusal, correction and action previews</h2>{decision_body}</section>',
            '<footer>No action, message, network request or external effect can be produced from this snapshot.</footer>',
            f"<script>{SCRIPT}</script></body></html>\n",
        ]
    )


def write_snapshot(
    briefing: dict[str, Any], output: str | Path, decision_previews: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    body = render_snapshot(briefing, decision_previews).encode("utf-8")
    handle, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    return {
        "schema": "hirc.ui-snapshot-result/1",
        "path": str(destination.resolve()),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "source_head": briefing.get("store_head"),
        "read_only": True,
    }


def snapshot_manifest(briefing: dict[str, Any]) -> str:
    """Canonical supporting identity for callers that need a deterministic pin."""
    body = render_snapshot(briefing).encode("utf-8")
    return canonical_json({"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)})
