import youtube_dl
import sys

folder = f"~/Music/{sys.argv[1]}/"
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': folder+'%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    filenames = sys.argv[2:]
    ydl.download(filenames)