"""Track management for the mini DAW."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np

from .audio_clip import AudioClip


@dataclass
class Track:
    clips: List[Tuple[AudioClip, int]] = field(default_factory=list)

    def add_clip(self, clip: AudioClip, start_sample: int = 0) -> None:
        self.clips.append((clip, start_sample))

    def mixdown(self) -> AudioClip:
        """Render the track to a single :class:`AudioClip`."""
        if not self.clips:
            return AudioClip(np.zeros(0, dtype=np.int16), 44100, 2, 1)

        frame_rate = self.clips[0][0].frame_rate
        sample_width = self.clips[0][0].sample_width
        channels = self.clips[0][0].channels

        end_sample = max(start + len(clip.samples) for clip, start in self.clips)
        mix = np.zeros((end_sample, channels), dtype=np.int32)

        for clip, start in self.clips:
            data = clip.samples
            if data.ndim == 1:
                data = data[:, None]
            if clip.channels == 1 and channels == 2:
                data = np.tile(data, (1, 2))
            mix[start:start + len(data)] += data

        # Clip to valid range
        max_val = 2 ** (8 * sample_width - 1) - 1
        mix = np.clip(mix, -max_val, max_val).astype({1: np.int8, 2: np.int16, 4: np.int32}[sample_width])
        return AudioClip(mix, frame_rate, sample_width, channels)


__all__ = ["Track"]
