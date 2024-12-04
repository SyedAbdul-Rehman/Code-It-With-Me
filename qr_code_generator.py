import qrcode
import os

def generate_qr_terminal(data):
    """
    Generates a QR code and displays it in the terminal as ASCII art.
    :param data: The data to encode into the QR code.
    """
    try:
        # Create a QR code object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,  # Smaller box size for terminal
            border=2,    # Minimum border for QR codes
        )
        
        # Add data to the QR code
        qr.add_data(data)
        qr.make(fit=True)
        
        # Print the QR code in ASCII format
        qr.print_ascii(invert=True)
        print("\nQR Code successfully displayed in the terminal.")
        
        return qr  # Return the QR code object for saving later
    except Exception as e:
        print(f"An error occurred while generating the QR code: {e}")
        return None

def save_qr_code(qr, data):
    """
    Saves the QR code as an image in a folder named 'qr_codes'.
    :param qr: The QRCode object to save.
    :param data: The data encoded in the QR code, used to create a filename.
    """
    try:
        # Ensure the folder 'qr_codes' exists
        folder_name = "qr_codes"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Create a valid filename by replacing invalid characters
        filename = f"{folder_name}/{data.replace(' ', '_').replace('/', '_')[:50]}.png"

        # Save the QR code as an image
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)

        print(f"QR Code saved as {filename}")
    except Exception as e:
        print(f"An error occurred while saving the QR code: {e}")

def main():
    print("Welcome to the Terminal QR Code Generator!")
    
    while True:
        try:
            # Ask the user for data to encode
            data = input("Enter the data (text, URL, etc.) for the QR code (or type 'exit' to quit): ").strip()
            
            if data.lower() == "exit":
                print("Exiting the program. Goodbye!")
                break
            
            # Validate input
            if not data:
                raise ValueError("Input cannot be empty. Please provide valid data.")
            
            print("\nHere is your QR Code:")
            # Generate and display the QR code in the terminal
            qr = generate_qr_terminal(data)

            if qr:  # If the QR code was successfully generated
                # Ask the user if they want to save the QR code
                save_option = input("Do you want to save this QR code as an image file? (yes/no): ").strip().lower()
                
                if save_option == "yes":
                    save_qr_code(qr, data)
                else:
                    print("QR code not saved.")
        
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        from PIL import Image
    except ImportError:
        print("Pillow library is required to save QR codes as images. Please install it using 'pip install pillow'.")
        exit()

    main()
