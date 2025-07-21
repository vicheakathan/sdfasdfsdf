# app.py
from flask import Flask, jsonify
from login import login_bp
from staff import staff_bp
from sale import sale_bp


app = Flask(__name__)

# Register all blueprints
app.register_blueprint(login_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(sale_bp)

@app.route('/', methods=['GET'])
def default():
    return jsonify('Server is running...')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
