"""Utility to generate simple sine wave tones for testing."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np

from .audio_clip import AudioClip


def generate_tone(filename: str, frequency: float, duration: float, frame_rate: int = 44100) -> None:
    t = np.linspace(0, duration, int(frame_rate * duration), False)
    tone = 0.5 * np.sin(2 * math.pi * frequency * t)
    samples = (tone * (2 ** 15 - 1)).astype(np.int16)
    clip = AudioClip(samples, frame_rate, 2, 1)
    clip.to_wav(filename)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a sine wave tone")
    parser.add_argument("filename")
    parser.add_argument("frequency", type=float)
    parser.add_argument("duration", type=float)
    args = parser.parse_args(argv)
    generate_tone(args.filename, args.frequency, args.duration)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
