import os
from pytube import YouTube
import argparse

def get_valid_link() -> str:
    while True:
        try:
            link = input("\nMusic Link: ")
            if link.lower() == 'exit':
                return link
            yt = YouTube(link)
            return link
        except Exception as e:
            print("Invalid link. Please provide a valid YouTube link.")

def get_valid_directory(title, primary_directory) -> str:
    print(f"\nDownloading:\n'{title}' | to the primary directory: {primary_directory}")
    print("Press Enter to confirm or type a new path to change the destination.")
    while True:
        try:
            destination = str(input(">> ") or primary_directory)

            if destination.lower() == 'exit':
                return destination

            if not os.path.exists(destination) or not os.path.isdir(destination):
                raise ValueError("Invalid destination directory. Please provide a valid path.")
            
            return destination
        except ValueError as ve:
            print(ve)

def main():
    parser = argparse.ArgumentParser(description="MP3 Downloader")
    parser.add_argument("--primary_directory", default='.', help="Primary directory for downloading files.")
    args = parser.parse_args()

    print("\nType 'exit' to exit the program.")
    link = get_valid_link()

    if link.lower() == 'exit':
        print("Exiting MP3 Downloader.")
        return

    yt = YouTube(link)

    destination = get_valid_directory(yt.title, args.primary_directory)

    print("\nDownloading...")

    out_file = yt.streams.filter(only_audio=True).first().download(output_path=destination)

    base, ext = os.path.splitext(out_file)
    new_file = os.path.join(destination, f"{yt.title}.mp3")
    os.rename(out_file, new_file)

    print(f"{yt.title}\nHas been successfully downloaded to {destination}\n")

if __name__ == "__main__":
    main()
