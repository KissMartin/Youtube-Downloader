import os
from pytube import YouTube

def get_valid_link() -> str:
    while True:
        try:
            link = input("Video Link: ")
            if link.lower() == 'exit':
                return link
            yt = YouTube(link)
            return link
        except Exception as e:
            print("Invalid link. Please provide a valid YouTube link.")

def get_valid_directory(title) -> str:
    while True:
        try:
            print(f"Downloading:\n'{title}' | to the current directory.")
            print("Press Enter to confirm or type a new path to change the destination.")
            print("Example: C:\\Users\\Videos")

            destination = str(input(">> ") or '.')

            if destination.lower() == 'exit':
                return destination

            if not os.path.exists(destination) or not os.path.isdir(destination):
                raise ValueError("Invalid destination directory. Please provide a valid path.")
            
            return destination
        except ValueError as ve:
            print(ve)

def download_video(link: str, destination: str) -> None:
    yt = YouTube(link)

    print("Downloading...")

    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    out_file = video.download(output_path=destination)

    print(yt.title + "\nHas been successfully downloaded to " + destination)

def main() -> None:
    print("Type 'exit' to exit the program.")
    link = get_valid_link()

    if link.lower() == 'exit':
        print("Exiting MP4 Downloader.")
        return

    yt = YouTube(link)

    destination = get_valid_directory(yt.title)

    if destination.lower() == 'exit':
        print("Exiting MP4 Downloader.")
        return

    download_video(link, destination)

if __name__ == "__main__":
    main()
