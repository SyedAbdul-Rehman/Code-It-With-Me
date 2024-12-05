import time
import qrcode  # Import the qrcode library for generating QR codes
import os  # Import os for file and directory operations
import requests  # Import requests for making HTTP requests

def terminal_color(color, is_background=False):
    # Map color names to ANSI escape codes for terminal output
    color_map = {
        "black": 40 if is_background else 30,
        "red": 41 if is_background else 31,
        "green": 42 if is_background else 32,
        "yellow": 43 if is_background else 33,
        "blue": 44 if is_background else 34,
        "magenta": 45 if is_background else 35,
        "cyan": 46 if is_background else 36,
        "white": 47 if is_background else 37,
        "reset": 0
    }
    # Return the ANSI escape code for the specified color
    return f"\033[{color_map.get(color.lower(), 0)}m"

def fetch_random_joke():
    try:
        # Set headers to accept JSON response
        headers = {'Accept': 'application/json'}
        # Make a GET request to fetch a random joke
        response = requests.get("https://icanhazdadjoke.com/", headers=headers)
        # Raise an error if the response status is not OK
        response.raise_for_status()
        # Parse the JSON response
        data = response.json()
        # Return the joke from the response data
        return data.get('joke', 'No joke found.')
    except requests.RequestException as e:
        # Print an error message if the request fails
        print(f"An error occurred while fetching the joke: {e}")
        # Return a default joke in case of an error
        return "Why don't scientists trust atoms? Because they make up everything!"

def generate_qr_terminal(data, box_size=1, border=2, fill_color="black", back_color="white"):
    try:
        # Create a QRCode object with specified settings
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        # Add data to the QR code
        qr.add_data(data)
        # Optimize the QR code size
        qr.make(fit=True)

        # Get terminal color codes for fill and background
        fill_color_code = terminal_color(fill_color)
        back_color_code = terminal_color(back_color, is_background=True)

        # Iterate over the QR code matrix to print it in the terminal
        for row in qr.get_matrix():
            for col in row:
                if col:
                    # Print filled cells with the specified fill color
                    print(f"{fill_color_code}██{terminal_color('reset')}", end="")
                else:
                    # Print empty cells with the specified background color
                    print(f"{back_color_code}  {terminal_color('reset')}", end="")
            print()  # New line after each row

        # Indicate successful QR code generation
        print("\nQR Code successfully displayed in the terminal.")
        return qr  # Return the QRCode object
    except Exception as e:
        # Print an error message if QR code generation fails
        print(f"An error occurred while generating the QR code: {e}")
        return None

def save_qr_code(qr, data, fill_color="black", back_color="white"):
    try:
        # Define the folder name for saving QR codes
        folder_name = "qr_codes"
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Create a valid filename by replacing spaces and slashes
        filename = f"{folder_name}/{data.replace(' ', '_').replace('/', '_')[:50]}.png"
        # Generate an image from the QRCode object
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        # Save the image to the specified filename
        img.save(filename)

        # Indicate successful saving of the QR code
        print(f"QR Code saved as {filename}")
    except Exception as e:
        # Print an error message if saving fails
        print(f"An error occurred while saving the QR code: {e}")

def main():
    # Welcome message for the user
    print("Welcome to the Terminal QR Code Generator! (Suggestion: Open terminal in full screen)")
    print("\n" + "_"*30)
    
    while True:
        # Display the menu options
        print("\nMenu:")
        print("1. Generate QR Code with Default Settings")
        print("2. Generate QR Code with Custom Settings")
        print("3. Surprise Me...")
        print("4. Exit")
        
        # Prompt the user to select an option
        choice = input("Please select an option (1, 2, 3, or 4): ").strip()
        
        if choice == "1":
            try:
                # Prompt the user for data to encode in the QR code
                data = input("Enter the data (text, URL, etc.) for the QR code: ").strip()
                if not data:
                    raise ValueError("Input cannot be empty.")
                
                # Generate the QR code with default settings
                print("\nGenerating QR code with default settings...")
                qr = generate_qr_terminal(data)
                
                if qr:
                    # Ask the user if they want to save the QR code
                    save_option = input("If you want to save this QR code typr \"yes\": ").strip().lower()
                    if save_option == "yes":
                        save_qr_code(qr, data)
                    else:
                        print("QR code not saved.")
            except Exception as e:
                # Print an error message if an exception occurs
                print(f"An error occurred: {e}")
        
        elif choice == "2":
            try:
                # Prompt the user for data to encode in the QR code
                data = input("Enter the data (text, URL, etc.) for the QR code: ").strip()
                if not data:
                    raise ValueError("Input cannot be empty.")
                
                # Prompt the user for custom QR code settings
                box_size = int(input("Enter box size (default is 10): ").strip() or 10)
                border = int(input("Enter border size (default is 4): ").strip() or 4)
                fill_color = input("Enter fill color (default is black): ").strip() or "black"
                back_color = input("Enter background color (default is white): ").strip() or "white"
                
                # Generate the QR code with custom settings
                print("\nGenerating QR code with custom settings...")
                qr = generate_qr_terminal(data, box_size, border, fill_color, back_color)
                
                if qr:
                    # Ask the user if they want to save the QR code
                    save_option = input("Do you want to save this QR code as an image file? (yes/no): ").strip().lower()
                    if save_option == "yes":
                        save_qr_code(qr, data, fill_color, back_color)
                    else:
                        print("QR code not saved.")
            except ValueError as ve:
                # Print an error message for value errors
                print(f"Error: {ve}")
            except Exception as e:
                # Print an error message for unexpected exceptions
                print(f"An unexpected error occurred: {e}")
        
        elif choice == "3":
            try:
                # Fetch a random joke and generate a QR code for it
                random_joke = fetch_random_joke()
                qr = generate_qr_terminal(random_joke)
                
                if qr:
                    # Ask the user if they want to save the QR code
                    save_option = input("Do you want to save this QR code as an image file? (yes/no): ").strip().lower()
                    if save_option == "yes":
                        save_qr_code(qr, random_joke)
                    else:
                        print("QR code not saved.")
            except Exception as e:
                # Print an error message if an exception occurs
                print(f"An error occurred: {e}")
        
        elif choice == "4":
            # Exit the program
            print("Exiting the program. Goodbye!")
            break
        
        else:
            # Print an error message for invalid menu choices
            print("Invalid choice. Please select 1, 2, 3, or 4.")
            time.sleep(2)  # Pause for 2 seconds
            os.system("cls")  # Clear the terminal screen

if __name__ == "__main__":
    # Run the main function if the script is executed directly
    main()
