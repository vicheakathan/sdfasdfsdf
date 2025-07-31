# app.py

from flask import Flask, request, jsonify
from notifypy import Notify

# Create a Flask application instance.
app = Flask(__name__)

# --- Notification Function (updated to use desktop notifications) ---
def send_desktop_notification_to_admin(sale_data):
    """
    Sends a desktop notification to the administrator on the machine
    where this script is running.

    Args:
        sale_data (dict): A dictionary containing the details of the new sale.
    """
    # Create a new notification instance.
    notification = Notify()

    # Set the notification title and message.
    notification.title = "New Sale Alert!"
    notification.message = (
        f"A new item has been sold:\n"
        f"Item: {sale_data['item_name']}\n"
        f"Price: ${sale_data['price']:.2f}\n"
        f"Customer: {sale_data['customer_email']}"
    )

    # You can also set an icon, but this is optional.
    # notification.icon = "path/to/your/icon.png"

    # Send the notification.
    # This will display a native desktop notification on the OS.
    notification.send()

    print("--- NEW SALE NOTIFICATION ---")
    print("Desktop notification sent to the admin.")
    print("-----------------------------")


# --- API Endpoint for Sales ---
@app.route('/api/sale', methods=['POST'])
def record_sale():
    """
    Handles POST requests to record a new sale.

    The request body is expected to be a JSON object with sale details.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    sale_data = request.get_json()

    # --- Data Validation ---
    required_fields = ["item_name", "price", "customer_email"]
    if not all(field in sale_data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields"}), 400

    print(f"Received new sale data: {sale_data}")

    # --- Trigger the Desktop Notification ---
    send_desktop_notification_to_admin(sale_data)

    return jsonify({"message": "Sale recorded successfully and admin notified"}), 201


# --- Main entry point to run the app ---
if __name__ == "__main__":
    app.run(debug=True)

# Instructions to run this code:
# 1. Ensure you have Python installed.
# 2. Install Flask: `pip install Flask`
# 3. Install the desktop notification library: `pip install notify-py`
# 4. Save this code as `app.py`.
# 5. Open your terminal and run: `python app.py`
# 6. Use a tool like `curl` or Postman to send a POST request to `http://127.0.0.1:5000/api/sale`.
#    Example `curl` command:
#    curl -X POST -H "Content-Type: application/json" -d '{"item_name": "Webcam", "price": 85.50, "customer_email": "jane.smith@example.com"}' http://127.0.0.1:5000/api/sale
