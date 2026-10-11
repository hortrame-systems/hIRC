"""Canonical encoding helpers used by the local integrity boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_MAX_JSON_BYTES = 1_048_576
DEFAULT_MAX_JSON_DEPTH = 64


def canonical_json(value: Any) -> str:
    """Return stable UTF-8 JSON text for values accepted by the event schema."""

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def strict_json_loads(value: str) -> Any:
    """Decode JSON while rejecting duplicate object keys at every depth."""
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, child in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key: {key}")
            result[key] = child
        return result

    return json.loads(value, object_pairs_hook=unique_object)


def bounded_canonical_json(
    value: Any,
    *,
    max_bytes: int = DEFAULT_MAX_JSON_BYTES,
    max_depth: int = DEFAULT_MAX_JSON_DEPTH,
) -> str:
    """Validate finite JSON shape/depth/UTF-8 size and return canonical text."""

    def walk(item: Any, depth: int) -> None:
        if depth > max_depth:
            raise ValueError("JSON nesting depth exceeds the local limit")
        if isinstance(item, dict):
            for key, child in item.items():
                if not isinstance(key, str):
                    raise TypeError("JSON object keys must be text")
                key.encode("utf-8")
                walk(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                walk(child, depth + 1)
        elif item is None or isinstance(item, (str, int, float, bool)):
            if isinstance(item, str):
                item.encode("utf-8")
        else:
            raise TypeError("value is not JSON data")

    try:
        walk(value, 0)
        rendered = canonical_json(value)
        encoded = rendered.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ValueError("JSON text is not valid UTF-8") from error
    if len(encoded) > max_bytes:
        raise ValueError("canonical JSON exceeds the local byte limit")
    return rendered


def load_bounded_json_file(
    path: str | Path,
    *,
    max_bytes: int = DEFAULT_MAX_JSON_BYTES,
    max_depth: int = DEFAULT_MAX_JSON_DEPTH,
) -> Any:
    """Read, decode and structurally bound one UTF-8 JSON file before use."""
    source = Path(path)
    with source.open("rb") as stream:
        raw = stream.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise ValueError("JSON file exceeds the local byte limit")
    try:
        text = raw.decode("utf-8", errors="strict")
        value = strict_json_loads(text)
        bounded_canonical_json(value, max_bytes=max_bytes, max_depth=max_depth)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, TypeError, ValueError) as error:
        raise ValueError("JSON file is not valid bounded UTF-8 JSON") from error
    return value
