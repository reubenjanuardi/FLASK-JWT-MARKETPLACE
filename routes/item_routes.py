import os
from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from extensions import db
from models.item import Item
from models.user import User

item_bp = Blueprint('item', __name__, url_prefix='/item')

# Get all items (PUBLIC ENDPOINT)
@item_bp.route('/', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify({"items":[item.to_dict() for item in items]}), 200

# Create new item (PROTECTED ENDPOINT)
@item_bp.route("/", methods=["POST"])
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    description = data.get('description')
    
    if not name or not price:
        return jsonify({"error": "Name and price are required"}), 400

    new_item = Item(
        name=name,
        price=float(price),
        description=description,
        user_id=user_id
    )
    
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Item created successfully"}), 201


# Get item by ID (PROTECTED ENDPOINT)
@item_bp.route("/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "description": item.description
    })

# Update item (PROTECTED ENDPOINT)
@item_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Hanya admin atau pemilik item yang boleh edit
    if user.role != 'admin' and item.user_id != int(user_id):
        return jsonify({"error": "Unauthorized to update this item"}), 403

    data = request.get_json()
    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    item.description = data.get('description', item.description)

    db.session.commit()
    return jsonify({"message": "Item updated successfully"}), 200

# Delete item (PROTECTED ENDPOINT)
@item_bp.route("/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    item = Item.query.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Hanya admin atau pemilik item yang boleh hapus
    if user.role != 'admin' and item.user_id != int(user_id):
        return jsonify({"error": "Unauthorized to delete this item"}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200
