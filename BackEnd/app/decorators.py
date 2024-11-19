from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.models import Instructor, Student

# custom decorator for instructor required
def instructor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        email = get_jwt_identity()
        user = Instructor.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Instructor access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# custom decorator for student required
def student_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        email = get_jwt_identity()
        user = Student.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Student access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

# custom decorator for system admin required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization header is missing'}), 401
            
        try:
            # Check if it's a bearer token
            auth_type, token = auth_header.split(' ')
            if auth_type.lower() != 'bearer':
                return jsonify({'error': 'Invalid authorization type'}), 401
                
            # Validate admin token
            if token != 'Sys-Admin-Secret':
                return jsonify({'error': 'Invalid admin token'}), 403
                
            return f(*args, **kwargs)
            
        except ValueError:
            return jsonify({'error': 'Invalid authorization header format'}), 401
            
    return decorated_function