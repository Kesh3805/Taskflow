from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app.extensions import db
from app.models.user import User
from app.utils.auth_middleware import get_current_user, validate_required_fields

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    valid, error = validate_required_fields(data, ["name", "email", "password"])
    if not valid:
        return jsonify({"error": error}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    user = User(
        name=data["name"],
        email=data["email"],
        role=data.get("role", "MEMBER"),
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict(),
        "access_token": access_token,
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    valid, error = validate_required_fields(data, ["email", "password"])
    if not valid:
        return jsonify({"error": error}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "access_token": access_token,
    }), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    """Get all users for member selection"""
    users = User.query.order_by(User.name).all()
    return jsonify({"users": [u.to_dict() for u in users]}), 200
