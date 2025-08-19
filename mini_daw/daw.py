"""A very small Digital Audio Workstation in pure Python."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

import numpy as np

from .audio_clip import AudioClip
from .track import Track

try:  # Optional playback support
    import sounddevice as sd
except Exception:  # pragma: no cover - sounddevice is optional
    sd = None


@dataclass
class DAW:
    tracks: List[Track] = field(default_factory=list)

    def new_track(self) -> Track:
        track = Track()
        self.tracks.append(track)
        return track

    def render(self) -> AudioClip:
        if not self.tracks:
            return AudioClip(np.zeros(0, dtype=np.int16), 44100, 2, 1)
        rendered = [track.mixdown() for track in self.tracks]
        frame_rate = rendered[0].frame_rate
        sample_width = rendered[0].sample_width
        channels = rendered[0].channels
        end_sample = max(len(r.samples) for r in rendered)
        mix = np.zeros((end_sample, channels), dtype=np.int32)
        for clip in rendered:
            data = clip.samples
            if clip.channels == 1 and channels == 2:
                data = np.tile(data[:, None], (1, 2))
            mix[:len(data)] += data
        max_val = 2 ** (8 * sample_width - 1) - 1
        mix = np.clip(mix, -max_val, max_val).astype({1: np.int8, 2: np.int16, 4: np.int32}[sample_width])
        return AudioClip(mix, frame_rate, sample_width, channels)

    def play(self) -> None:
        """Play the current mix using :mod:`sounddevice` if available."""
        if sd is None:
            raise RuntimeError("sounddevice library not available")
        clip = self.render()
        sd.play(clip.samples, clip.frame_rate)
        sd.wait()

    def export(self, filename: str) -> None:
        self.render().to_wav(filename)


__all__ = ["DAW"]
