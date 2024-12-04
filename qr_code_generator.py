import qrcode

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
        qr_ascii = qr.print_ascii(invert=True)
        print("\nQR Code successfully generated and displayed in the terminal.")
    except Exception as e:
        print(f"An error occurred while generating the QR code: {e}")

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
            generate_qr_terminal(data)
        
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
