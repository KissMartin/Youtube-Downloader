import os

def launch_mp3_downloader():
    os.system("python mp3downloader.py")

def launch_mp4_downloader():
    os.system("python mp4downloader.py")

def main():
    while True:
        print("Choose an option:")
        print("1: Launch MP3 Downloader")
        print("2: Launch MP4 Downloader")
        print("0: Exit")
        
        choice = input(">> ")

        if choice == '1':
            launch_mp3_downloader()
        elif choice == '2':
            launch_mp4_downloader()
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 0.")

if __name__ == "__main__":
    main()
