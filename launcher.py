import os
import re
import subprocess
import requests
from tqdm import tqdm

APP_DATA_DIR = os.path.join(
    os.getenv("APPDATA") or os.path.expanduser("~"),
    "YoutubeDownloader"
)

os.makedirs(APP_DATA_DIR, exist_ok=True)

PRIMARY_DIRECTORY_FILE = os.path.join(
    APP_DATA_DIR, "primary_directory.txt"
)

YTDLP_EXE_PATH = os.path.join(APP_DATA_DIR, "yt-dlp.exe")

YTDLP_URL = (
    "https://github.com/yt-dlp/yt-dlp/releases/latest/"
    "download/yt-dlp.exe"
)


def ensure_ytdlp_exists():
    """Download yt-dlp if missing and update it."""
    if not os.path.exists(YTDLP_EXE_PATH):
        print("Initial setup: Downloading yt-dlp...")

        try:
            response = requests.get(YTDLP_URL, timeout=60)
            response.raise_for_status()

            with open(YTDLP_EXE_PATH, "wb") as file:
                file.write(response.content)

        except requests.RequestException as error:
            print(f"Could not download yt-dlp: {error}")
            return False

    # Update yt-dlp when possible.
    try:
        subprocess.run(
            [YTDLP_EXE_PATH, "-U"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=120
        )
    except (OSError, subprocess.TimeoutExpired):
        print("Warning: Could not update yt-dlp.")

    return True


def set_primary_directory():
    path = input(
        "Set primary directory (where downloads go):\n>> "
    ).strip().strip('"')

    if not os.path.isdir(path):
        print("Invalid directory.")
        return

    with open(PRIMARY_DIRECTORY_FILE, "w", encoding="utf-8") as file:
        file.write(path)


def get_primary_directory():
    if os.path.exists(PRIMARY_DIRECTORY_FILE):
        with open(PRIMARY_DIRECTORY_FILE, encoding="utf-8") as file:
            path = file.read().strip()

        if os.path.isdir(path):
            return path

    return os.path.join(os.path.expanduser("~"), "Downloads")


def is_twitter_url(url):
    """Recognize common Twitter/X post URLs."""
    return bool(
        re.match(
            r"^https?://(?:www\.|mobile\.)?"
            r"(?:x\.com|twitter\.com)/",
            url.strip(),
            re.IGNORECASE
        )
    )


def download_logic(mode, primary_dir):
    print("\nType 'exit' to cancel.")

    link = input(f"{mode} link: ").strip()

    if link.lower() == "exit":
        return

    if not link:
        print("No URL provided.")
        return

    # The Twitter option should only accept Twitter/X URLs.
    if mode == "TWITTER" and not is_twitter_url(link):
        print("Please enter a valid Twitter/X post URL.")
        return

    print(
        f"\nDestination: {primary_dir}"
        "\nPress Enter to confirm or type another directory."
    )

    destination = input(">> ").strip().strip('"') or primary_dir

    if not os.path.isdir(destination):
        print("Invalid directory.")
        return

    if not ensure_ytdlp_exists():
        return

    # Build the yt-dlp command.
    command = [YTDLP_EXE_PATH]

    if mode == "MP3":
        command += [
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "192K"
        ]

    elif mode == "MP4":
        command += [
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4"
        ]

    elif mode == "TWITTER":
        # Download the best available video and audio.
        command += [
            "-f", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4"
        ]

    # Make yt-dlp print progress updates on separate lines.
    command += [
        "--newline",
        "-o", os.path.join(destination, "%(title)s.%(ext)s"),
        link
    ]

    print(f"\nDownloading {mode}...")

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1
        )

        with tqdm(
            total=100,
            desc=f"Downloading {mode}",
            unit="%",
            ncols=80
        ) as pbar:

            for line in process.stdout:
                # yt-dlp progress example:
                # [download]  42.5% of ...
                match = re.search(r"\[download\]\s+(\d+(?:\.\d+)?)%", line)

                if match:
                    percentage = float(match.group(1))
                    pbar.n = min(percentage, 100)
                    pbar.refresh()
                elif line.strip():
                    print(line.rstrip())

        return_code = process.wait()

        if return_code == 0:
            print("\nDownload complete!")
        else:
            print(
                f"\nDownload failed (exit code {return_code})."
                "\nCheck the error above and try again."
            )

    except OSError as error:
        print(f"Could not start yt-dlp: {error}")

    except KeyboardInterrupt:
        print("\nCancelling download...")
        if process.poll() is None:
            process.terminate()
            process.wait()


def main():
    if not os.path.exists(PRIMARY_DIRECTORY_FILE):
        set_primary_directory()

    while True:
        primary_dir = get_primary_directory()

        print("\n=== Video Downloader ===")
        print("1: MP3")
        print("2: MP4")
        print("3: Twitter/X Video")
        print("4: Set Directory")
        print("0: Exit")

        choice = input(">> ").strip()

        if choice == "1":
            download_logic("MP3", primary_dir)

        elif choice == "2":
            download_logic("MP4", primary_dir)

        elif choice == "3":
            download_logic("TWITTER", primary_dir)

        elif choice == "4":
            set_primary_directory()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()