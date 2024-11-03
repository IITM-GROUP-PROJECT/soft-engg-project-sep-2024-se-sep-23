from functools import wraps
from flask import jsonify
from flask_login import current_user

def role(role):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error": "unauthorized"}), 401
            if role == "admin" and not current_user.is_admin():
                return jsonify({"error": "admin access is required"}), 403
            elif role == "instructor" and not current_user.is_instructor():
                return jsonify({"error": "instructor access is required"}), 403
            elif role == "student" and not current_user.is_student():
                return jsonify({"error": "student access is required"}), 403
            return func(*args, **kwargs)
        return wrapper

    return decorator
