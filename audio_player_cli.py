import time  # Import time for sleep functionality
import yt_dlp  # Import yt_dlp for downloading YouTube audio
import vlc  # Import VLC for media playback
import os  # Import os for clearing the console

# Function to fetch the audio URL of a YouTube video
def get_audio_url(youtube_url):
    try:
        print("\nFetching Song...")
        print("\nWait a second...\n")
        # Options for yt_dlp to extract audio URL
        ydl_opts = {
            'format': 'bestaudio/best',  # Fetch the best quality audio
            'quiet': True,  # Suppress verbose output
            'extract_flat': True,  # Extract metadata without downloading
        }
        # Extract audio stream URL
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info['url']
    except yt_dlp.DownloadError as e:
        # Specific error for yt-dlp download issues
        print(f"Download error: {e}")
        print("Check if the URL is valid and accessible.")
    except KeyError as e:
        # Handle case when the 'url' key is not found in the info dictionary
        print(f"KeyError: Missing expected data in the response. {e}")
        print("Could not extract the audio URL. Please try again later.")
    except Exception as e:
        # Catch any other errors
        print(f"Failed to fetch audio URL. Error: {e}")
        print("Wait for 2 seconds and try again...")
    time.sleep(2)
    return None

# Function to play a song
# Function to play a song with volume control
def play_song(song):
    try:
        print("\nStarting the song...")
        url = get_audio_url(song)  # Fetch the audio URL
        if not url:
            print("Could not fetch the audio URL. Aborting...")
            time.sleep(2)
            return
        player = vlc.MediaPlayer(url)  # Create a VLC media player instance
        player.play()  # Start playback

        # Set an initial volume level
        volume = 50
        player.audio_set_volume(volume)
        print(f"Volume set to {volume}%.")

        # Infinite loop to handle user controls
        while True:
            print("\nControls: [P] Pause/Resume | [R] Restart | [Q] Quit | [+] Increase Volume | [-] Decrease Volume")
            command = input("Enter command: ").strip().lower()

            if command == "p":  # Pause or resume the music
                if player.is_playing():
                    player.pause()
                    print("Music paused.")
                else:
                    player.play()
                    print("Music resumed.")
            elif command == "r":  # Restart the song
                player.stop()
                player.play()
                print("Music restarted.")
            elif command == "+":  # Increase volume
                volume = min(100, volume + 10)  # Max volume is 100%
                player.audio_set_volume(volume)
                print(f"Volume increased to {volume}%.")
            elif command == "-":  # Decrease volume
                volume = max(0, volume - 10)  # Min volume is 0%
                player.audio_set_volume(volume)
                print(f"Volume decreased to {volume}%.")
            elif command == "q":  # Quit the player and return to the main menu
                player.stop()
                print("Exiting player.")
                break
            else:
                # Handle invalid commands
                print("Invalid command. Try again.")
    except vlc.MediaPlayerError as e:
        # Handle VLC player-specific errors
        print(f"VLC MediaPlayer error: {e}")
        print("Could not initialize the media player. Please check the installation and dependencies.")
    except Exception as e:
        # General error handling
        print(f"Some error occurred while playing the song. Error: {e}")
        print("Wait for 2 seconds and try again...")
        time.sleep(2)

# Function to display a list of pre-defined songs and allow selection
def list_of_songs():
    songs = [
        "https://youtu.be/kyjg5kX4pT0?si=QKSHUocD6HVORbBW",
        "https://youtu.be/XO8wew38VM8?si=9qG5id8bC5f-Mxaq",
        "https://youtu.be/VCNLZflKQ7o?si=mCTy9U26-TU0X3lA"
    ]
    while True:
        try:
            os.system("cls")  # Clear the screen
            print("\n" + "_"*30)
            print("\nList of songs:")
            print("\n1. Dil Tu Jaan Tu by Gurnazar Ft. Kritika Yadav")
            print("2. Millionaire by YoYo Honey Singh")
            print("3. Tere Hawaale by Arijit Singh")
            print("4. Exit")
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                play_song(songs[0])  # Play the first song
            elif choice == 2:
                play_song(songs[1])  # Play the second song
            elif choice == 3:
                play_song(songs[2])  # Play the third song
            elif choice == 4:
                # Exit the list and return to the main menu
                print("\nThanks for using my music player!")
                break
            else:
                # Handle invalid menu choices
                print("\nInvalid choice... Please choose from the list.")
                print("Wait for 2 seconds and try again...")
                time.sleep(2)
        except ValueError:
            # Handle invalid input when the user enters something that's not a number
            print("Invalid input. Please enter a number.")
            time.sleep(2)
        except Exception as e:
            # Catch any unexpected errors
            print(f"Unexpected error: {e}")
            time.sleep(2)

# Main function to display the main menu and handle user choices
def main():
    while True:
        try:
            os.system("cls")  # Clear the screen
            print("\n                Welcome to my music player")
            print("\n" + "_"*30)
            print("\n1. Wanna play my list of songs?")
            print("2. Wanna play your own song?")
            print("3. Exit")
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                list_of_songs()  # Show the list of pre-defined songs
            elif choice == 2:
                os.system("cls")  # Clear the screen
                song_url = input("\nEnter the song URL: ").strip()
                play_song(song_url)  # Play the user's custom song
            elif choice == 3:
                # Exit the program
                print(f"\nThanks for using my music player! Have a nice day! {chr(0x1F642)}")
                break
            else:
                # Handle invalid menu choices
                print("\nInvalid choice... Please choose from the options.")
                print("Wait for 2 seconds and try again...")
                time.sleep(2)
        except ValueError:
            # Handle invalid input when the user enters something that's not a number
            print("Invalid input. Please enter a valid number.")
            print("Wait for 2 seconds and try again...")    
            time.sleep(2)
        except Exception as e:
            # Catch any unexpected errors
            print(f"Unexpected error: {e}")
            time.sleep(2)

# Entry point of the program
if __name__ == "__main__":
    main()
