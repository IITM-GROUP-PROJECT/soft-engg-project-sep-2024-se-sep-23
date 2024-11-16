from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import Instructor, Student

def instructor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        email = get_jwt_identity()
        user = Instructor.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Instructor access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        email = get_jwt_identity()
        user = Student.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Student access required"}), 403
        return fn(*args, **kwargs)
    return wrapper