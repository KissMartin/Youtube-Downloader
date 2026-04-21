import os
import subprocess
import re
import requests
import sys
from tqdm import tqdm

APP_DATA_DIR = os.path.join(os.getenv('APPDATA'), 'YoutubeDownloader')

if not os.path.exists(APP_DATA_DIR):
    os.makedirs(APP_DATA_DIR)

PRIMARY_DIRECTORY_FILE = os.path.join(APP_DATA_DIR, "primary_directory.txt")
YTDLP_EXE_PATH = os.path.join(APP_DATA_DIR, "yt-dlp.exe")

def ensure_ytdlp_exists():
    if not os.path.exists(YTDLP_EXE_PATH):
        print("Initial setup: Downloading YouTube engine to system data...")
        url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        r = requests.get(url)
        with open(YTDLP_EXE_PATH, "wb") as f:
            f.write(r.content)
    
    subprocess.run([YTDLP_EXE_PATH, "-U"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def set_primary_directory():
    path = input("Set primary directory (where you want your music/videos to go):\n>> ")
    with open(PRIMARY_DIRECTORY_FILE, "w") as f:
        f.write(path)

def get_primary_directory():
    if os.path.exists(PRIMARY_DIRECTORY_FILE):
        with open(PRIMARY_DIRECTORY_FILE) as f:
            return f.read().strip()
    return os.path.join(os.path.expanduser("~"), "Downloads")

def download_logic(mode, primary_dir):
    print(f"\nType 'exit' to cancel.")
    link = input(f"{mode} Link: ")
    if link.lower() == "exit": return

    print(f"\nDestination: {primary_dir} (Press Enter to confirm or type new path)")
    destination = input(">> ") or primary_dir
    if not os.path.isdir(destination):
        print("Invalid directory.")
        return

    ensure_ytdlp_exists()

    if mode == "MP3":
        command = [YTDLP_EXE_PATH, "-x", "--audio-format", "mp3", "--audio-quality", "192K"]
    else:
        command = [YTDLP_EXE_PATH, "-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4"]

    command += ["--newline", "-o", os.path.join(destination, "%(title)s.%(ext)s"), link]

    pbar = tqdm(total=100, unit='%', desc=f"Downloading {mode}", ncols=80)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in process.stdout:
        match = re.search(r"(\d+\.\d+)%", line)
        if match:
            pbar.n = float(match.group(1))
            pbar.refresh()

    process.wait()
    pbar.n = 100
    pbar.close()
    print("Download complete.")

def main():
    if not os.path.exists(PRIMARY_DIRECTORY_FILE):
        set_primary_directory()

    while True:
        primary_dir = get_primary_directory()
        print(f"\n1: MP3\n2: MP4\n3: Set Directory\n0: Exit")
        choice = input(">> ")

        if choice == "1":
            download_logic("MP3", primary_dir)
        elif choice == "2":
            download_logic("MP4", primary_dir)
        elif choice == "3":
            set_primary_directory()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()