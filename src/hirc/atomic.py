"""Small fail-closed filesystem publication primitives."""

from __future__ import annotations

import os
from pathlib import Path


class AtomicPublishError(OSError):
    """A create-if-absent publication could not be completed safely."""


def _publish_new_name(source: Path, destination: Path) -> None:
    if os.name == "nt":
        # Windows rename is atomic and refuses an existing destination.
        os.rename(source, destination)
        return
    # A same-filesystem hard link provides create-if-absent publication on POSIX.
    os.link(source, destination, follow_symlinks=False)
    source.unlink()


def publish_new(source: str | Path, destination: str | Path) -> None:
    """Publish one fsynced same-directory file without replacing any target."""
    temporary = Path(source)
    target = Path(destination)
    if temporary.parent.resolve() != target.parent.resolve():
        raise AtomicPublishError("atomic publication requires one directory")
    try:
        _publish_new_name(temporary, target)
    except FileExistsError as error:
        raise AtomicPublishError("publication target already exists") from error
    except OSError as error:
        raise AtomicPublishError("atomic create-if-absent publication failed") from error
