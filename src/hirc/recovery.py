"""Verified atomic SQLite backup and restore for the local hIRC store."""

from __future__ import annotations

import hashlib
import os
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path
from typing import Any

from .atomic import AtomicPublishError, publish_new
from .store import IntegrityError, Store


class RecoveryError(IntegrityError):
    """A backup or restore could not preserve the verified local store."""


def _copy_verified(source: str | Path, destination: str | Path, operation: str) -> dict[str, Any]:
    source_path = Path(source)
    target = Path(destination)
    if not source_path.is_file():
        raise RecoveryError(f"{operation} source is missing")
    if target.exists():
        raise RecoveryError(f"{operation} target already exists")
    source_store = Store(source_path)
    try:
        source_state = source_store.verify(read_only=True)
    except sqlite3.Error as error:
        raise RecoveryError(f"{operation} source is unreadable") from error
    if not source_state["valid"]:
        raise RecoveryError(f"{operation} source is invalid: " + "; ".join(source_state["errors"]))
    target.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    try:
        with closing(sqlite3.connect(source_path)) as source_connection, closing(
            sqlite3.connect(temporary)
        ) as target_connection:
            source_connection.backup(target_connection)
            target_connection.commit()
        with temporary.open("r+b") as stream:
            stream.flush()
            os.fsync(stream.fileno())
        copied_state = Store(temporary).verify(read_only=True)
        if not copied_state["valid"]:
            raise RecoveryError(f"{operation} copy is invalid: " + "; ".join(copied_state["errors"]))
        if (
            copied_state["head_hash"] != source_state["head_hash"]
            or copied_state["event_count"] != source_state["event_count"]
            or copied_state["disabled_capabilities"] != source_state["disabled_capabilities"]
        ):
            raise RecoveryError(f"{operation} copy does not match the source state")
        body = temporary.read_bytes()
        try:
            publish_new(temporary, target)
        except AtomicPublishError as error:
            raise RecoveryError(f"{operation} target appeared during publication") from error
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise
    return {
        "schema": "hirc.recovery-copy/1",
        "operation": operation,
        "source": str(source_path.resolve()),
        "destination": str(target.resolve()),
        "sha256": hashlib.sha256(body).hexdigest(),
        "bytes": len(body),
        "event_count": source_state["event_count"],
        "head_hash": source_state["head_hash"],
        "encrypted": False,
        "sensitive_data_release_allowed": False,
    }


def backup_store(source: str | Path, destination: str | Path) -> dict[str, Any]:
    return _copy_verified(source, destination, "backup")


def restore_store(backup: str | Path, destination: str | Path) -> dict[str, Any]:
    return _copy_verified(backup, destination, "restore")
