# app.py

from flask import Flask, request, jsonify, render_template

# To store notifications in memory.
# In a real app, this would be a database like Firestore, PostgreSQL, or MongoDB.
# This approach is for demonstration only and will be reset when the server restarts.
sales_notifications = []

# Create a Flask application instance.
app = Flask(__name__)

# --- Notification Function (updated for a web-based solution) ---
def record_sale_and_notify(sale_data):
    """
    Saves the new sale data to a list for a web-based dashboard to display.

    Args:
        sale_data (dict): A dictionary containing the details of the new sale.
    """
    # Add a timestamp and unique ID to the notification for better handling.
    import time
    notification = {
        "id": int(time.time()),
        "message": (
            f"Item: {sale_data['item_name']}, "
            f"Price: ${sale_data['price']:.2f}, "
            f"Customer: {sale_data['customer_email']}"
        )
    }
    sales_notifications.insert(0, notification) # Add to the beginning of the list

    print("--- NEW SALE RECORDED ---")
    print(f"Sale data saved: {notification}")
    print("-------------------------")

# --- Web UI Endpoint ---
@app.route('/')
def admin_dashboard():
    """
    Renders the web-based admin dashboard.
    This is what the admin will see in their web browser.
    """
    # The HTML for the dashboard is included directly as a multi-line string.
    # We use a f-string to inject the Tailwind CSS CDN link.
    dashboard_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #f3f4f6;
        }}
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden p-6 md:p-8">
        <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">Sales Dashboard</h1>
        <p class="text-center text-gray-600 mb-8">Notifications will appear here automatically.</p>

        <div id="notifications-list" class="space-y-4">
            <!-- Notifications will be inserted here by JavaScript -->
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const notificationsList = document.getElementById('notifications-list');

            const fetchNotifications = async () => {{
                try {{
                    // Fetch the notifications from our new API endpoint.
                    const response = await fetch('/api/notifications');
                    const notifications = await response.json();
                    
                    // Clear the current list.
                    notificationsList.innerHTML = '';

                    // Add a new card for each notification.
                    if (notifications.length === 0) {{
                        notificationsList.innerHTML = '<p class="text-center text-gray-400">No new sales yet.</p>';
                    }} else {{
                        notifications.forEach(notification => {{
                            const notificationCard = document.createElement('div');
                            notificationCard.className = 'bg-green-50 border-l-4 border-green-400 text-green-700 p-4 rounded-lg shadow-sm animate-pulse-once';
                            notificationCard.innerHTML = `<div class="font-semibold">New Sale!</div><div>${{notification.message}}</div>`;
                            notificationsList.appendChild(notificationCard);
                        }});
                    }}
                }} catch (error) {{
                    console.error('Error fetching notifications:', error);
                }}
            }};

            // Fetch notifications initially and then every 5 seconds.
            fetchNotifications();
            setInterval(fetchNotifications, 5000);
        }});
    </script>
</body>
</html>
    """
    return dashboard_html


# --- API Endpoint to get notifications for the dashboard ---
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """
    Returns the list of all sales notifications as a JSON object.
    The web dashboard calls this endpoint to get updates.
    """
    return jsonify(sales_notifications)


# --- API Endpoint for Sales (same as before, but with new notification logic) ---
@app.route('/api/sale', methods=['POST'])
def record_sale():
    """
    Handles POST requests to record a new sale.
    This is the endpoint your client app or e-commerce platform would call.
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    sale_data = request.get_json()

    # --- Data Validation ---
    required_fields = ["item_name", "price", "customer_email"]
    if not all(field in sale_data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields"}), 400

    # --- Trigger the new web-based notification logic ---
    record_sale_and_notify(sale_data)

    return jsonify({"message": "Sale recorded successfully and admin notified"}), 201


if __name__ == "__main__":
    app.run(debug=True)

