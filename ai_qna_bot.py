import google.generativeai as genai     # for API calls
import os       # for checking if file exists

# Set your API key for Google Generative AI
genai.configure(api_key="Your API Here")  # Enter your API key here

# Function to interact with Google Generative AI
def ask_question(question):
    try:
        model = genai.GenerativeModel("gemini-pro")  # specifies AI model
        chat = model.start_chat()
        response = chat.send_message(question)
        # extract generated response
        return response.text
    except KeyError:
        return "Error: Unable to parse response from the API."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Function to save conversation history
def save_conversation(question, answer, file_name="conversation_history.txt"):
    try:
        with open(file_name, "a") as f:
            f.write(f"User: {question}\nAI: {answer}\n\n")
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return

# Function to handle user greeting and clear data
def get_user_name():
    name_file = "name.txt"
    conversation_file = "conversation_history.txt"
    
    # Check if name file exists and read it
    if os.path.exists(name_file) and os.path.getsize(name_file) > 0:
        with open(name_file, "r") as f:
            name = f.read().strip()
        print(f"\nWelcome back, {name}!")
    else:
        name = input("It seems you're using this program for the first time! What's your name? ").strip()
        with open(name_file, "w") as f:
            f.write(name)
        print(f"\nNice to meet you, {name}! Your name has been saved for future sessions.")
    
    # Ask to clear data if conversation file exists and contains data
    if os.path.exists(conversation_file) and os.path.getsize(conversation_file) > 0:
        clear_data_choice = input("\nDo you want to clear your saved conversation history? (yes/no): ").strip().lower()
        if clear_data_choice == "yes":
            clear_data(conversation_file)

    return name

# Function to clear data
def clear_data(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"{file_name} has been cleared.")
    else:
        print(f"No {file_name} file found to delete.")

# Function to display previous conversation history
def display_previous_conversations(file_name="conversation_history.txt"):
    if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
        print("\nPrevious Conversations:")
        with open(file_name, "r") as f:
            print(f.read())
    else:
        print("\nNo previous conversations found.")

# Function to display a good bye message with a fun quote
def goodbye_message(user_name):
    quotes = [
        "Goodbye, and remember: Every day is a new opportunity!",
        "Thanks for chatting, and may your day be filled with possibilities!",
        "Farewell, my friend! See you next time!",
        "Take care, and may the world be kind to you today!"
    ]
    import random
    print(f"\nGoodbye, {user_name}! {random.choice(quotes)}")

# Main Function
def main():
    user_name = get_user_name()  # Get the user's name
    print("\n\t  Welcome to the AI-Powered Q & A Bot!")
    print("\n" + "_" * 30)
    
    # After clear data prompt, ask to show previous conversations if available
    if os.path.exists("conversation_history.txt") and os.path.getsize("conversation_history.txt") > 0:
        show_history = input("\nDo you want to view your previous conversation history? (yes/no): ").strip().lower()
        if show_history == "yes":
            display_previous_conversations()

    print("\nType your questions below.")
    print("Type 'Exit' to quit")

    while True:
        try:
            question = input(f"\n{user_name}, what's your question? ").strip()
            if question.lower() == "exit":
                goodbye_message(user_name)  # Display goodbye message
                break  # Exit the loop and end the program
            # Get response from bot
            answer = ask_question(question)
            print(f"AI's Answer: {answer}\n")
            # Save conversation history
            save_conversation(question, answer)
        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting gracefully...")
            goodbye_message(user_name)  # Display goodbye message
            break  # Exit loop on Ctrl + C without abrupt termination
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            goodbye_message(user_name)  # Display goodbye message
            break  # Exit loop on unforeseen error

# Run Program
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Critical error encountered: {e}")
        # Handle critical error gracefully
