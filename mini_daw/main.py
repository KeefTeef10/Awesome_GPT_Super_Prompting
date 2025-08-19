"""Command line interface for the mini DAW.

This script demonstrates basic usage of the :mod:`mini_daw` package. It
scans a directory for audio files and mixes the first two files it finds
onto separate tracks before exporting the result.
"""

from __future__ import annotations

import argparse
from .audio_clip import AudioClip
from .daw import DAW
from .file_system import list_audio_files


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mini DAW example")
    parser.add_argument("root", help="Directory containing audio clips")
    parser.add_argument("output", help="Output WAV file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    files = list_audio_files(args.root)
    if not files:
        parser.error("no audio files found in given directory")

    daw = DAW()
    track1 = daw.new_track()
    clip1 = AudioClip.from_wav(files[0])
    track1.add_clip(clip1)

    if len(files) > 1:
        track2 = daw.new_track()
        clip2 = AudioClip.from_wav(files[1])
        # start second clip halfway through first clip
        track2.add_clip(clip2, start_sample=len(clip1.samples) // 2)

    daw.export(args.output)
    print(f"Exported mix to {args.output}")
    return 0


if __name__ == "__main__":  # pragma: no cover - manual execution
    raise SystemExit(main())
