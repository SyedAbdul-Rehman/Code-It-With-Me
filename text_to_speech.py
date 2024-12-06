import pyttsx3

def list_voices(engine):
    try:
        voices = engine.getProperty('voices')
        for index, voice in enumerate(voices):
            print(f"Voice ID: {index}")
            print(f" - Name: {voice.name}")
            print()
    except Exception as e:
        print(f"Error listing voices: {e}")

def text_to_speech(text, rate=150, volume=1.0, voice_id=0, save_as_file=False, filename="output.wav"):
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Set properties
        engine.setProperty('rate', rate)  # Speed of speech
        engine.setProperty('volume', volume)  # Volume level (0.0 to 1.0)

        # Set voice
        voices = engine.getProperty('voices')
        if voice_id < len(voices):
            engine.setProperty('voice', voices[voice_id].id)
        else:
            print("Invalid voice ID, using default voice.")
            engine.setProperty('voice', voices[0].id)  # Default voice

        # Convert text to speech
        engine.say(text)

        # Save to file if required
        if save_as_file:
            engine.save_to_file(text, filename)

        # Play the speech
        engine.runAndWait()
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")

def main():
    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # List available voices
        print("Available voices:")
        list_voices(engine)

        # Accept text input from the user
        text = input("Enter the text you want to convert to speech: ")

        # Check if the text is empty
        if not text.strip():
            print("Error: No text provided.")
            return

        # Customize voice settings
        rate = int(input("Enter speech rate (default 150): ") or 150)
        volume = float(input("Enter volume level (0.0 to 1.0, default 1.0): ") or 1.0)
        voice_id = int(input("Enter voice ID (default 0): ") or 0)

        # Option to save the audio
        save_as_file = input("If you want to save the audio type \"yes\" (default no): ").strip().lower() == 'yes'
        filename = "output.wav"
        if save_as_file:
            filename = input("Enter the filename (with extension .wav or .mp3): ")

        # Convert text to speech
        text_to_speech(text, rate, volume, voice_id, save_as_file, filename)
    except ValueError as ve:
        print(f"Input error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
