#!/usr/bin/env python3
"""
YouTube Downloader with Graphical User Interface (version 2).

Requirements:
  pip install yt-dlp imageio-ffmpeg
  (tkinter comes with Python by default)

Usage:
  python youtube_downloader_gui.py
"""

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import yt_dlp
import imageio_ffmpeg

COLOR_BACKGROUND = "#1e1e2e"
COLOR_PANEL = "#282838"
COLOR_TEXT = "#e0e0e0"
COLOR_SUBTEXT = "#9a9ab0"
COLOR_ACCENT = "#e63950"
COLOR_ACCENT_HOVER = "#ff4d63"
COLOR_SUCCESS = "#3ddc84"
COLOR_INPUT = "#32324a"


class App:
    def __init__(self, root):
        self.root = root
        root.title("YouTube Downloader")
        root.geometry("540x560")
        root.minsize(520, 540)
        root.resizable(True, True)
        root.configure(bg=COLOR_BACKGROUND)

        self._configure_styles()

        # Header
        header = tk.Frame(root, bg=COLOR_BACKGROUND)
        header.pack(fill="x", padx=24, pady=(22, 10))
        tk.Label(
            header, text="▶ YouTube Downloader",
            bg=COLOR_BACKGROUND, fg=COLOR_TEXT, font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")
        tk.Label(
            header, text="Paste the link, choose the format and download.",
            bg=COLOR_BACKGROUND, fg=COLOR_SUBTEXT, font=("Segoe UI", 9)
        ).pack(anchor="w")

        # Main panel
        panel = tk.Frame(root, bg=COLOR_PANEL)
        panel.pack(fill="both", expand=True, padx=24, pady=10)

        # Link
        tk.Label(
            panel, text="Video link", bg=COLOR_PANEL, fg=COLOR_SUBTEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(18, 4))
        self.entry_link = tk.Entry(
            panel, font=("Segoe UI", 10), bg=COLOR_INPUT, fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT, relief="flat"
        )
        self.entry_link.pack(fill="x", padx=18, ipady=7)

        # Format
        tk.Label(
            panel, text="Format", bg=COLOR_PANEL, fg=COLOR_SUBTEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(16, 4))
        frame_type = tk.Frame(panel, bg=COLOR_PANEL)
        frame_type.pack(anchor="w", padx=14)
        self.type = tk.StringVar(value="video")
        self._create_radio(frame_type, "Video (mp4)", "video")
        self._create_radio(frame_type, "Audio (mp3)", "audio")

        # Destination folder
        tk.Label(
            panel, text="Destination folder", bg=COLOR_PANEL, fg=COLOR_SUBTEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(16, 4))
        frame_folder = tk.Frame(panel, bg=COLOR_PANEL)
        frame_folder.pack(fill="x", padx=18)
        self.folder = tk.StringVar(value="downloads")
        entry_folder = tk.Entry(
            frame_folder, textvariable=self.folder, font=("Segoe UI", 10),
            bg=COLOR_INPUT, fg=COLOR_TEXT, insertbackground=COLOR_TEXT, relief="flat"
        )
        entry_folder.pack(side="left", fill="x", expand=True, ipady=7)
        tk.Button(
            frame_folder, text="Browse", command=self.choose_folder,
            bg=COLOR_INPUT, fg=COLOR_TEXT, relief="flat", font=("Segoe UI", 9),
            activebackground=COLOR_ACCENT, cursor="hand2", padx=10
        ).pack(side="left", padx=(8, 0))

        # Download button
        self.btn_download = tk.Button(
            panel, text="DOWNLOAD", command=self.start_download,
            bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 11, "bold"),
            relief="flat", cursor="hand2", activebackground=COLOR_ACCENT_HOVER
        )
        self.btn_download.pack(fill="x", padx=18, pady=(20, 6), ipady=8)

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.bar = ttk.Progressbar(
            panel, orient="horizontal", mode="determinate",
            variable=self.progress_var, maximum=100, style="Custom.Horizontal.TProgressbar"
        )
        self.bar.pack(fill="x", padx=18, pady=(6, 4))

        self.status = tk.Label(
            panel, text="Ready.", bg=COLOR_PANEL, fg=COLOR_SUBTEXT, font=("Segoe UI", 9)
        )
        self.status.pack(anchor="w", padx=18, pady=(0, 14))

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=COLOR_INPUT, background=COLOR_ACCENT,
            bordercolor=COLOR_PANEL, lightcolor=COLOR_ACCENT, darkcolor=COLOR_ACCENT,
            thickness=14,
        )

    def _create_radio(self, parent, text, value):
        rb = tk.Radiobutton(
            parent, text=text, variable=self.type, value=value,
            bg=COLOR_PANEL, fg=COLOR_TEXT, selectcolor=COLOR_INPUT,
            activebackground=COLOR_PANEL, font=("Segoe UI", 10),
            indicatoron=True, padx=10, pady=4
        )
        rb.pack(side="left", padx=6)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder.set(folder)

    def start_download(self):
        url = self.entry_link.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please paste a valid link.")
            return

        self.btn_download.config(state="disabled", text="DOWNLOADING...")
        self.bar.config(mode="indeterminate")
        self.bar.start(12)
        self.status.config(text="Preparing...", fg=COLOR_SUBTEXT)

        thread = threading.Thread(target=self.download, args=(url,), daemon=True)
        thread.start()

    def download(self, url):
        audio_only = self.type.get() == "audio"
        destination_folder = self.folder.get() or "downloads"

        if audio_only:
            # Conversion to mp3 using ffmpeg included in the imageio-ffmpeg 
            # package (installed via pip, no manual download needed).
            options = {
                "format": "bestaudio/best",
                "outtmpl": f"{destination_folder}/%(title)s.%(ext)s",
                "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "progress_hooks": [self.progress],
                "noprogress": True,
                "quiet": True,
            }
        else:
            # Chooses a single file that already has video+audio merged
            # ("progressive" format), so it doesn't need ffmpeg to merge anything.
            options = {
                "format": "best[ext=mp4]/best",
                "outtmpl": f"{destination_folder}/%(title)s.%(ext)s",
                "progress_hooks": [self.progress],
                "noprogress": True,
                "quiet": True,
            }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
            self.root.after(0, self.completed, True, "")
        except Exception as e:
            self.root.after(0, self.completed, False, str(e))

    def progress(self, d):
        # Calculates the percentage manually from bytes
        # (avoids using strings from yt-dlp which contain ANSI color codes).
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                pct = (downloaded / total) * 100
                self.root.after(0, self._update_progress, pct, f"Downloading... {pct:.0f}%")
            else:
                # Unknown total size: keeps animation running
                # and shows how many MB have been downloaded so far.
                mb = downloaded / (1024 * 1024)
                self.root.after(0, self._update_status, f"Downloading... {mb:.1f} MB")
        elif d.get("status") == "finished":
            self.root.after(0, self._update_status, "Finalizing...")

    def _update_status(self, text):
        self.status.config(text=text, fg=COLOR_ACCENT)

    def _update_progress(self, pct, text):
        if str(self.bar["mode"]) == "indeterminate":
            self.bar.stop()
            self.bar.config(mode="determinate")
        self.progress_var.set(pct)
        self.status.config(text=text, fg=COLOR_ACCENT)

    def completed(self, success, error):
        self.btn_download.config(state="normal", text="DOWNLOAD")
        if str(self.bar["mode"]) == "indeterminate":
            self.bar.stop()
            self.bar.config(mode="determinate")
        if success:
            self.progress_var.set(100)
            self.status.config(text="Completed!", fg=COLOR_SUCCESS)
            messagebox.showinfo("Success", "Download finished successfully!")
        else:
            self.status.config(text="Error.", fg=COLOR_ACCENT)
            messagebox.showerror("Error", f"Failed:\n{error}")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()