# YouTube Downloader

A small desktop app for downloading YouTube videos as **mp4** or **mp3**. Built with Python, kept as lightweight as possible.

## What it does

Paste a link, pick video or audio, hit download. That's pretty much it. There's a progress bar so you know it's actually doing something, and you get to choose where the file lands on your computer.

## Before you start

You'll need Python 3.8 or newer. If you don't have it, grab it from [python.org](https://www.python.org/downloads/).

## Setting it up

Clone the repo (or just download the files) and install the two dependencies:

```bash
git clone https://github.com/HeavyFromTF2/Youtube_Downloader_MP4-MP3.git
cd Youtube_Downloader_MP4-MP3
pip install yt-dlp imageio-ffmpeg
```

That's it, only two packages. `tkinter`, which handles the actual window and buttons, ships with Python already — you shouldn't need to install anything for it. The one exception is some Linux distros, which split it out separately:

```bash
sudo apt install python3-tk
```

## Running it

```bash
python youtube_downloader_gui.py
```

A window pops up. Paste your link, choose mp4 or mp3, pick a folder (it defaults to a `downloads` folder next to the script), and click **DOWNLOAD**. Wait for the bar to fill up, and you're done.

## Why these two libraries

**yt-dlp** does the heavy lifting — figuring out the actual video/audio streams and pulling them down. There's no realistic way to do this without it (or something equivalent); YouTube changes how it serves content often enough that rolling your own solution would break constantly.

**imageio-ffmpeg** is only needed for the mp3 option. Audio coming straight from YouTube isn't in mp3 format, so it needs converting — and that conversion needs ffmpeg. Instead of asking you to install ffmpeg separately (which on Windows especially is a bit of a hassle), this package just bundles a copy of it that gets installed automatically with pip.

## A couple of things worth knowing

- Video downloads stick to formats that already bundle video and audio into one file. This keeps things simple (no merging step, no extra tools), but it does mean you won't always get the absolute highest resolution YouTube offers — usually it tops out somewhere around 720p, depending on what's available for that particular video.
- The first mp3 conversion might feel a touch slower than later ones, since the bundled ffmpeg has to spin up.

## One more thing

Only use this on videos you actually have the right to download — your own content, anything under a permissive license, or public domain material. Downloading copyrighted videos without permission goes against YouTube's terms of service, so use your judgment.

## License

Do whatever you want with this. Use it, change it, break it, fix it.
