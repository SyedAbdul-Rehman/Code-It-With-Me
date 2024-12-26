import sqlite3
from datetime import datetime, timezone
from twilio.rest import Client
import pytz
import schedule
import time

# Twilio credentials (replace with your own)
ACCOUNT_SID = 'your_account_sid'
AUTH_TOKEN = 'your_auth_token'
FROM_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio sandbox number

def setup_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()

    # Create a table to store scheduled messages
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scheduled_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            recipient_number TEXT NOT NULL,
            message_content TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            timezone TEXT NOT NULL
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def schedule_message(user_id, recipient_number, message_content, scheduled_time, timezone_str):
    # Convert scheduled_time from user's timezone to UTC
    local_tz = pytz.timezone(timezone_str)
    local_time = local_tz.localize(datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S'))
    utc_time = local_time.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')

    # Connect to the SQLite database
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()

    # Insert the scheduled message into the database
    cursor.execute('''
        INSERT INTO scheduled_messages (user_id, recipient_number, message_content, scheduled_time, timezone)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, recipient_number, message_content, utc_time, timezone_str))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Message scheduled successfully!")

def send_scheduled_messages():
    # Connect to the SQLite database
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()

    # Get the current time in UTC
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    # Query for messages that are due to be sent
    cursor.execute('''
        SELECT id, recipient_number, message_content FROM scheduled_messages
        WHERE scheduled_time <= ?
    ''', (current_time,))

    messages_to_send = cursor.fetchall()

    # Initialize the Twilio client
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # Send each scheduled message
    for message in messages_to_send:
        message_id, recipient_number, message_content = message
        client.messages.create(
            body=message_content,
            from_=FROM_WHATSAPP_NUMBER,
            to=f'whatsapp:{recipient_number}'  # Ensure the number is prefixed with 'whatsapp:'
        )
        print(f"Message sent to {recipient_number}")

        # Optionally, delete the message from the database after sending
        cursor.execute('DELETE FROM scheduled_messages WHERE id = ?', (message_id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def main():
    setup_database()

    # Get user input
    user_id = input("Enter your user ID: ")
    recipient_number = input("Enter the recipient's WhatsApp number (with country code): ")
    message_content = input("Enter the message content: ")
    scheduled_time = input("Enter the scheduled time (YYYY-MM-DD HH:MM:SS): ")
    timezone_str = input("Enter your time zone (e.g., Asia/Karachi): ")

    # Schedule the message
    schedule_message(user_id, recipient_number, message_content, scheduled_time, timezone_str)

    # Schedule the send_scheduled_messages function to run every minute
    schedule.every(1).minutes.do(send_scheduled_messages)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
