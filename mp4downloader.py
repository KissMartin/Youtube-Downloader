from pytube import YouTube


def main() -> None:
    link = input("Link: ")
    yt = YouTube(link)

    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    destination = str(input(">> ")) or '.'

    out_file = video.download(output_path=destination)

    print(yt.title + " has been successfully downloaded.")


if __name__ == "__main__":
    main()
