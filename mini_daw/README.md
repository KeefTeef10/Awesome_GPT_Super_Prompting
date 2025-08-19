# Mini DAW

This directory contains a tiny Digital Audio Workstation implemented in
pure Python.  It supports loading WAV files, placing them on tracks and
mixing them down into a single output file.  Playback is available when
the optional `sounddevice` package is installed.

## Usage

```
python -m mini_daw.main <audio_folder> output.wav
```

The script searches the given folder for audio files and mixes the first
two clips it finds.  A file system helper is provided in
[`file_system.py`](file_system.py) for locating audio clips on disk.

This code is intentionally minimal and is designed for educational
purposes rather than production use.
