# First, you need to install the plyer library if you haven't already.
# Open your terminal or command prompt and run:
# pip install plyer

from plyer import notification
import time

def send_basic_notification():
    """
    Sends a simple desktop notification with a title and message.
    """
    print("Sending a basic notification...")
    notification.notify(
        title='Hello from Python!',
        message='This is a simple notification sent from a Python script.',
        # The 'app_name' parameter is optional but can be useful for
        # grouping notifications and setting an app icon on some platforms.
        app_name='Python Notifier'
    )
    print("Notification sent. It will disappear after a default timeout.")

def send_scheduled_notification():
    """
    Sends a notification after a short delay and includes a longer message.
    The timeout parameter controls how long the notification stays on screen.
    """
    print("Waiting 5 seconds to send a scheduled notification...")
    # time.sleep() is used to pause the script for a specified number of seconds.
    # This is useful for scheduling notifications.
    time.sleep(5)

    print("Sending a scheduled notification...")
    notification.notify(
        title='Reminder: Time to Take a Break',
        message='You have been working for a while. '
                'Remember to stand up and stretch!',
        app_name='Python Notifier',
        # Set the timeout to 20 seconds.
        # Note: Some operating systems may ignore this parameter.
        timeout=20
    )
    print("Scheduled notification sent.")

if __name__ == "__main__":
    # Call the functions to demonstrate the notifications.
    send_basic_notification()
    
    # Send the second notification after the first one is likely gone.
    send_scheduled_notification()
