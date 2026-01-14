import os
import argparse
import yt_dlp

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

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(destination, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
    }

    print("\nDownloading...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    print("Download complete.")

if __name__ == "__main__":
    main()
