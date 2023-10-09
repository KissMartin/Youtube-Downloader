import os
from pytube import YouTube


def main() -> None:
    link = input("Link: ")
    yt = YouTube(link)

    video = yt.streams.filter(only_audio=True).first()

    destination = str(input(">> ")) or '.'

    out_file = video.download(output_path=destination)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print(yt.title + " has been successfully downloaded.")


if __name__ == "__main__":
    main()
