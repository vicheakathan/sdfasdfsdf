from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid
import json
from functools import wraps
from login import token_required

sale_bp = Blueprint('sale', __name__)

SALES_FILE = "sales.json"

@sale_bp.route('/sales', methods=['GET'])
@token_required
def get_all_sale_transaction():
    try:
        with open(SALES_FILE, 'r') as f:
            sales = json.load(f)
    except json.JSONDecodeError:
        return jsonify([])
    except Exception as e:
        return jsonify({'error' : f"Error loading sales from file: {e}"})

    return jsonify({'data': sales}), 200

@sale_bp.route('/sales', methods=['POST'])
@token_required
def add_sale_transaction():
    data = request.get_json()

    try:
        with open(SALES_FILE, 'r') as f:
            sales = json.load(f)
    except Exception as e:
        sales = []

    for item in data:
        item['id'] = str(uuid.uuid4())
        item['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sales.append(item)

    try:
        with open(SALES_FILE, 'w') as f:
            json.dump(sales, f, indent=4)
    except json.JSONDecodeError:
        return jsonify([])
    except Exception as e:
        return jsonify({'error' : f"Error loading sales from file: {e}"})

    return jsonify({
        'status' : True,
        'message' : 'Sale Transaction added successfully!',
        'data' : data
    }), 200

@sale_bp.route('/sales/<id>', methods=['PUT'])
@token_required
def update_sale_transaction(id):
    data = request.get_json()

    try:
        with open(SALES_FILE, 'r') as f:
            sales = json.load(f)
    except Exception as e:
        sales = []
    
    update = False
    for i, item in enumerate(sales):
        if item['id'] == id:
            sales[i].update(data)
            update = True
            break
    
    if not update:
        return jsonify({"error": f"Sale ID not found: {id}"}), 404
    try:
        with open(SALES_FILE, 'w') as f:
            json.dump(sales, f, indent=4)
    except Exception as e:
        return jsonify({'error': f"Error saving sales to file: {e}"}), 500
    
    return jsonify({
        f"status": "OK",
        "message" : "Updated successfully!",
        "data" : data
    })

@sale_bp.route('/sales/<id>', methods=['DELETE'])
@token_required
def delete_sale_transaction(id):
    try:
        with open(SALES_FILE, 'r') as f:
            sales = json.load(f)
    except Exception as e:
        sales = []

    original_length = len(sales)
    sales = [sale for sale in sales if sale.get('id') != id]

    if len(sales) == original_length:
        return jsonify({"error": f"Sale ID {id} not found."}), 404

    try:
        with open(SALES_FILE, 'w') as f:
            json.dump(sales, f, indent=4)
    except Exception as e:
        return jsonify({"error": f"Failed to save updated sales: {e}"}), 500
    
    return jsonify({
        f"status": "OK",
        "message" : "Deleted successfully!",
    })
