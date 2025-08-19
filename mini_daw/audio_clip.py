"""Representation of a single audio clip.

The :class:`AudioClip` class wraps basic loading and manipulation of WAV
files using the built-in :mod:`wave` module and :mod:`numpy` for math.
"""

from __future__ import annotations

import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

import numpy as np


@dataclass
class AudioClip:
    """A short piece of audio loaded into memory."""

    samples: np.ndarray
    frame_rate: int
    sample_width: int
    channels: int

    @classmethod
    def from_wav(cls, filename: str | Path) -> "AudioClip":
        """Load a clip from a WAV file."""
        path = Path(filename)
        with wave.open(str(path), "rb") as wf:
            frame_rate = wf.getframerate()
            sample_width = wf.getsampwidth()
            channels = wf.getnchannels()
            frames = wf.readframes(wf.getnframes())
        dtype = {1: np.int8, 2: np.int16, 4: np.int32}[sample_width]
        samples = np.frombuffer(frames, dtype=dtype)
        if channels > 1:
            samples = samples.reshape(-1, channels)
        return cls(samples, frame_rate, sample_width, channels)

    @property
    def duration_seconds(self) -> float:
        return len(self.samples) / self.frame_rate

    def to_wav(self, filename: str | Path) -> None:
        """Write the clip to a WAV file."""
        path = Path(filename)
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.sample_width)
            wf.setframerate(self.frame_rate)
            wf.writeframes(self.samples.tobytes())


__all__ = ["AudioClip"]
