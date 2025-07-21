from flask import Blueprint, jsonify
from login import token_required

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/staff', methods=['GET'])
@token_required
def get_staff():
    return jsonify({
        "staff": ["Alice", "Bob", "Charlie"]
    })
