import secrets  # Import the 'secrets' module for cryptographically secure random number generation.
import string  # Import 'string' to use pre-defined sets of characters like letters, digits, and punctuation.
from datetime import datetime  # Import 'datetime' to handle date and time for timestamping saved passwords.

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

# Function to save a selected password to a file
def save_password_to_file(passwords):
    """
    Save a selected password from the list to a file with a timestamp.
    
    Args:
        passwords (list): List of generated passwords.
    """
    try:
        # Prompt the user to select which password to save
        choice = int(input("\nWhich password you wanna save? "))
        with open("password.txt", "+a") as file:
            # Get the current timestamp
            timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
            # Write the selected password with the timestamp to the file
            file.write(f"{timestamp} - {passwords[choice-1]}\n")
            print("\nPassword saved....")
            print("\n" + "_" * 30)
    except:
        # Handle invalid choice input
        print("\nInvalid choice...")
        print("\n" + "_" * 30)
    finally:
        # Ask if the user wants to save another password
        choice_2 = input("\nWanna save another password?(yes/no) ").strip().lower() == 'yes'
        if choice_2:
            save_password_to_file(passwords)

# Main function to handle user input and display the generated password
def main():
    """
    Main function to interact with the user for password generation.
    """
    print("\n                    Welcome to Random Password Generator.\n\n")  # Welcome message
    try:
        # Prompt the user for the desired password length
        passwords = []
        length = int(input("Enter password length: "))
        
        # Ask if special characters should be included
        include_special_chars = input("\nInclude special characters? (yes/no): ").strip().lower() == 'yes'
        
        # Ask how many passwords to generate
        num_of_password = int(input("\nHow many password you wanna generate? "))
        
        # Generate the passwords using the user input
        for num in range(num_of_password):
            password = generate_password(length, include_special_chars)
            passwords.append(password)
            # Display the generated password
            print(f"\n{num+1}. Generated Password: {password}")
        
        # Ask if the user wants to save any password
        choice = input("\nWanna any save passowrd?(yes/no) ").strip().lower() == 'yes'
        if choice:
            save_password_to_file(passwords)
        
    except:
        # Handle invalid inputs
        print("\nInvalid input. Please enter a valid number for password length and yes/no for special characters.")
    finally:
        # Final message to the user
        print("\n" + "_" * 30)
        print("\nThanks for using it. Bye")

# Entry point for the script
if __name__ == "__main__":
    main()
