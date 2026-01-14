import os
import argparse
import yt_dlp
from tqdm import tqdm

class YTDLLogger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(f"[ERROR] {msg}")

def tqdm_hook(d):
    if d['status'] == 'downloading':
        pbar.total = d.get('total_bytes') or d.get('total_bytes_estimate')
        pbar.update(d['downloaded_bytes'] - pbar.n)
    elif d['status'] == 'finished':
        pbar.close()

def get_valid_link() -> str:
    while True:
        link = input("\nVideo Link: ")
        if link.lower() == "exit":
            return link
        if link.startswith("http"):
            return link
        print("Invalid link.")

def get_valid_directory(primary_directory) -> str:
    print(f"\nDestination directory: {primary_directory}")
    print("Press Enter to confirm or type a new path.")
    while True:
        destination = input(">> ") or primary_directory
        if destination.lower() == "exit":
            return destination
        if os.path.isdir(destination):
            return destination
        print("Invalid directory.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary_directory", default=".")
    args = parser.parse_args()

    print("\nType 'exit' to exit.")
    link = get_valid_link()
    if link.lower() == "exit":
        return

    destination = get_valid_directory(args.primary_directory)
    if destination.lower() == "exit":
        return

    global pbar
    pbar = tqdm(unit='B', unit_scale=True, desc="Downloading", ncols=80)

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(destination, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": False,
        "logger": YTDLLogger(),  # hide warnings
        "progress_hooks": [tqdm_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    print("Download complete.")

if __name__ == "__main__":
    main()
