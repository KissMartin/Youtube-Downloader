import os
import subprocess

PRIMARY_DIRECTORY_FILE = "primary_directory.txt"

def set_primary_directory():
    path = input("Set primary directory:\n>> ")
    with open(PRIMARY_DIRECTORY_FILE, "w") as f:
        f.write(path)

def get_primary_directory():
    if os.path.exists(PRIMARY_DIRECTORY_FILE):
        with open(PRIMARY_DIRECTORY_FILE) as f:
            return f.read().strip()
    return "."

def launch(script):
    subprocess.run([
        "python",
        script,
        "--primary_directory",
        get_primary_directory()
    ])

def main():
    if not os.path.exists(PRIMARY_DIRECTORY_FILE):
        set_primary_directory()

    while True:
        print("\n1: MP3\n2: MP4\n3: Set Directory\n0: Exit")
        choice = input(">> ")

        if choice == "1":
            launch("mp3_downloader.py")
        elif choice == "2":
            launch("mp4_downloader.py")
        elif choice == "3":
            set_primary_directory()
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
