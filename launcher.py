import os

PRIMARY_DIRECTORY_FILE = "primary_directory.txt"

def set_primary_directory():
    print("Set the primary directory where files will be placed:")
    primary_directory = input(">> ")
    
    with open(PRIMARY_DIRECTORY_FILE, 'w') as file:
        file.write(primary_directory)

def get_primary_directory():
    if os.path.exists(PRIMARY_DIRECTORY_FILE):
        with open(PRIMARY_DIRECTORY_FILE, 'r') as file:
            return file.read().strip()
    else:
        return "."

def launch_mp3_downloader():
    os.system(f"python mp3_downloader.py --primary_directory {get_primary_directory()}")

def launch_mp4_downloader():
    os.system(f"python mp4_downloader.py --primary_directory {get_primary_directory()}")

def main():
    print("Welcome to the Downloader Launcher!")
    
    if not os.path.exists(PRIMARY_DIRECTORY_FILE):
        set_primary_directory()
    
    while True:
        print("\nChoose an option:")
        print("1: Launch MP3 Downloader")
        print("2: Launch MP4 Downloader")
        print("3: Set Primary Directory")
        print("0: Exit")

        choice = input(">> ")

        if choice == '1':
            launch_mp3_downloader()
        elif choice == '2':
            launch_mp4_downloader()
        elif choice == '3':
            set_primary_directory()
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 0.")

if __name__ == "__main__":
    main()
