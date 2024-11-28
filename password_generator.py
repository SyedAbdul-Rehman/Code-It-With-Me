import secrets  # Import the 'secrets' module for cryptographically secure random number generation.
import string  # Import 'string' to use pre-defined sets of characters like letters, digits, and punctuation.

# Function to generate a random password
def generate_password(length, include_special_chars=True):
    """
    Generate a random password of a specified length.
    
    Args:
        length (int): Length of the password to generate.
        include_special_chars (bool): Whether to include special characters in the password.
        
    Returns:
        str: A randomly generated password.
    """
    # Define character pools for the password
    letters = string.ascii_letters  # All uppercase and lowercase letters.
    digits = string.digits  # Numbers 0-9.
    special_chars = string.punctuation  # Special characters like !, @, #, etc.

    # Combine pools based on whether special characters are included
    if include_special_chars:
        pool = letters + digits + special_chars
    else:
        pool = letters + digits

    # Generate the password by selecting random characters from the pool
    password = "".join(secrets.choice(pool) for _ in range(length))
    return password  # Return the generated password.

# Main function to handle user input and display the generated password
def main():
    """
    Main function to interact with the user for password generation.
    """
    print("Welcome to Random Password Generator.")  # Welcome message
    try:
        # Prompt the user for the desired password length
        length = int(input("Enter password length: "))
        
        # Ask if special characters should be included
        include_special_chars = input("Include special characters? (yes/no): ").strip().lower() == 'yes'
        
        # Generate the password using the user input
        password = generate_password(length, include_special_chars)
        
        # Display the generated password
        print("Generated Password: ", password)
    except:
        # Handle invalid inputs
        print("Invalid input. Please enter a valid number for password length and yes/no for special characters.")

# Entry point for the script
if __name__ == "__main__":
    main()
