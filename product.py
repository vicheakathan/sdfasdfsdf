from flask import Blueprint, jsonify
from login import token_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/product', methods=['GET'])
@token_required
def get():
    return jsonify({
        "staff": ["Alice", "Bob", "Charlie"]
    })
