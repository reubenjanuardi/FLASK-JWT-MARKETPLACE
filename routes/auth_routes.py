from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token,  create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

# In-memory blacklist token storage
blacklist = set()

# Register endpoint
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Validate input fields are present
    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# Login endpoint
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    # Validate input fields are present
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    # Authenticate user credentials
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate access token (short lived - 15 minutes)
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(minutes=15)
    )
    # Generate refresh token (long lived - 7 days)
    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=timedelta(days=7)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


# Protected route to check user profile
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    }), 200

# Protected route to update user profile
@auth_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if name:
        user.name = name
    if email:
        # Check if new email is already taken
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 400
        user.email = email
    if password:
        user.password = generate_password_hash(password)

    db.session.commit()

    return jsonify(
        {"message": "Profile updated successfully", 
         "profile": {"name":name, "email":email}} 
        ), 200

# Logout (blacklist token)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

# REFRESH TOKEN
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, expires_delta=timedelta(minutes=30))
    return jsonify({"access_token": new_access_token}), 200


# Token verification — prevent reuse of blacklisted token
from flask_jwt_extended import JWTManager

def register_jwt_callbacks(jwt: JWTManager):
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklist
    
    # Ketika tidak ada token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401
    
    # Ketika token invalid/rusak
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Invalid token"}), 401

    # Ketika token direvoke
    @jwt.revoked_token_loader
    def revoked_token_response(jwt_header, jwt_payload):
        return jsonify({"error": "Token has been revoked"}), 401
    
    # Ketika token expired
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired",}), 401
    