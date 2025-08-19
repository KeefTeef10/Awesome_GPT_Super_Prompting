"""Simple Tkinter user interface for the mini DAW.

This module exposes a minimal graphical front end that allows users to
load multiple WAV files, play the resulting mix (when the optional
``sounddevice`` package is installed) and export the mix to a new WAV
file.  The UI is intentionally basic and is meant for demonstration
purposes only.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Iterable

from .audio_clip import AudioClip
from .daw import DAW


class MiniDAWUI(tk.Tk):
    """Small graphical front end for :mod:`mini_daw`."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Mini DAW")
        self.geometry("400x300")

        self.daw = DAW()

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        controls = tk.Frame(self)
        controls.pack(fill=tk.X)

        tk.Button(controls, text="Load Clips", command=self.load_clips).pack(
            side=tk.LEFT
        )
        tk.Button(controls, text="Play Mix", command=self.play_mix).pack(
            side=tk.LEFT
        )
        tk.Button(controls, text="Export Mix", command=self.export_mix).pack(
            side=tk.LEFT
        )

    def load_clips(self) -> None:
        """Ask the user for WAV files and add them to the project."""
        filenames: Iterable[str] = filedialog.askopenfilenames(
            title="Select WAV files", filetypes=[("WAV", "*.wav")]
        )
        for filename in filenames:
            clip = AudioClip.from_wav(filename)
            track = self.daw.new_track()
            track.add_clip(clip)
            self.listbox.insert(tk.END, filename)

    def play_mix(self) -> None:
        """Render and play the current mix."""
        try:
            self.daw.play()
        except Exception as exc:  # pragma: no cover - GUI feedback only
            messagebox.showerror("Playback error", str(exc))

    def export_mix(self) -> None:
        """Render and export the current mix to a WAV file."""
        filename = filedialog.asksaveasfilename(
            title="Export Mix",
            defaultextension=".wav",
            filetypes=[("WAV", "*.wav")],
        )
        if filename:
            self.daw.export(filename)
            messagebox.showinfo("Export complete", f"Mix exported to {filename}")


def main() -> None:  # pragma: no cover - manual execution
    app = MiniDAWUI()
    app.mainloop()


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
