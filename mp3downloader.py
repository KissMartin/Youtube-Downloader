import os
from pytube import YouTube

def get_valid_link() -> str:
    while True:
        try:
            link = input("Music Link: ")
            if link.lower() == 'exit':
                return link
            yt = YouTube(link)
            return link
        except Exception as e:
            print("Invalid link. Please provide a valid YouTube link.")

def get_valid_directory(title) -> str:
    print(f"Downloading:\n'{title}' | to the current directory.")
    print("Press Enter to confirm or type a new path to change the destination.")
    print("Example: C:\\Users\\Music")
    while True:
        try:

            destination = str(input(">> ") or '.')

            if not os.path.exists(destination) or not os.path.isdir(destination):
                raise ValueError("Invalid destination directory. Please provide a valid path.")
            
            return destination
        except ValueError as ve:
            print(ve)

def main() -> None:
    print("Type 'exit' to exit the program.")
    link = get_valid_link()

    if link.lower() == 'exit':
        print("Exiting MP3 Downloader.")
        return

    yt = YouTube(link)

    video = yt.streams.filter(only_audio=True).first()

    destination = get_valid_directory(yt.title)

    print("Downloading...")

    out_file = video.download(output_path=destination)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print(yt.title + "\nHas been successfully downloaded to " + destination)

if __name__ == "__main__":
    main()
