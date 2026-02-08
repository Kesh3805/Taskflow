from functools import wraps
from typing import Optional, Tuple, Any
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User


def admin_required(fn):
    """Decorator that requires the user to be an ADMIN."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "ADMIN":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def get_current_user() -> Optional[User]:
    """Get the current authenticated user from JWT identity."""
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def validate_required_fields(data: dict, fields: list) -> Tuple[bool, Optional[str]]:
    """Validate that required fields are present in the request data."""
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None
