import os
import yt_dlp

def list_formats(url):
    """
    Fetch and display available formats for the given YouTube video.
    :param url: YouTube video URL
    :return: A dictionary of formats with their IDs
    """
    try:
        print("\nFetching available formats...\n")
        options = {
            'listformats': True,  # List available formats without downloading
            'quiet': True,  # Suppress unnecessary output
        }

        formats = {}

        # Use yt-dlp to extract formats
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            for fmt in info['formats']:
                if fmt.get("ext") and fmt.get("format_note"):
                    formats[fmt["format_id"]] = f"{fmt['format_note']} ({fmt['ext']})"

        # Display formats
        print("Available formats:")
        for fmt_id, description in formats.items():
            print(f"{fmt_id}: {description}")

        return formats
    except Exception as e:
        print(f"An error occurred while fetching formats: {e}")
        return None

def download_video(url, format_id):
    """
    Downloads a YouTube video in the user-selected format.
    :param url: YouTube video URL
    :param format_id: Format ID for the desired resolution/format
    """
    try:
        # Specify download options
        options = {
            'format': format_id,  # User-selected format
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to 'downloads' folder
        }

        # Ensure the 'downloads' directory exists
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        print("\nDownloading...")
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        print("Download complete! Check the 'downloads' folder.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Welcome to the YouTube Video Downloader with Resolution Selection!")
    while True:
        print("\nOptions:")
        print("1. Download a video/audio")
        print("2. Exit")

        choice = input("\nEnter your choice: ").strip()
        if choice == "1":
            url = input("\nEnter the YouTube video URL: ").strip()
            if not url:
                print("Error: URL cannot be empty.")
            else:
                # Step 1: List available formats
                formats = list_formats(url)
                if formats:
                    # Step 2: Ask user to select a format
                    format_id = input("\nEnter the format ID you want to download: ").strip()
                    if format_id not in formats:
                        print("Invalid format ID. Please try again.")
                    else:
                        # Step 3: Download video in selected format
                        download_video(url, format_id)
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
