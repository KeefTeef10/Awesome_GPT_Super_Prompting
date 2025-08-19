"""File system utilities for accessing audio clips.

This module provides a simple wrapper around the local file system to
search for audio files. It intentionally avoids external dependencies so
that it can run in minimal environments.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List


AUDIO_EXTENSIONS: List[str] = [".wav", ".mp3", ".flac", ".ogg"]


def list_audio_files(root: str | Path, extensions: Iterable[str] | None = None) -> List[Path]:
    """Return a list of audio files under *root*.

    Parameters
    ----------
    root:
        Directory to search in.
    extensions:
        Optional iterable of file extensions to filter on.  If omitted,
        :data:`AUDIO_EXTENSIONS` is used.
    """

    root_path = Path(root)
    if extensions is None:
        extensions = AUDIO_EXTENSIONS

    result: List[Path] = []
    for ext in extensions:
        result.extend(root_path.rglob(f"*{ext}"))
    return sorted(result)


__all__ = ["list_audio_files", "AUDIO_EXTENSIONS"]
