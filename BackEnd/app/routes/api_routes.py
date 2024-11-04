## all routes should be defined here

from flask import Blueprint, jsonify, request, current_app
from app.models import User
from app.extensions import db
from app.services.decorators import role

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api_routes = Blueprint("api", __name__)

@api_routes.route("/users", methods=["GET"])
# @role("admin")
# @role("instructor")
def get_users():

    from app.jobs.jobs import simpleTask
    print(simpleTask.delay())
    print("test")
    return "test"

# SIGNUP API
@api_routes.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    student_email = data.get("student_email")
    github_username = data.get("github_username")
    password = data.get("password")

    if User.query.filter_by(student_email=student_email).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(
        student_email=student_email,
        github_username=github_username,
        role=1
    )
    new_user.plain_password = password

    db.session.add(new_user)
    db.session.commit()

    current_app.logger.info(f"User created successfully: {student_email}")
    return jsonify({"msg": "User created successfully"}), 201

# LOGIN API
@api_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    student_email = data.get("student_email")
    password = data.get("password")

    user = User.query.filter_by(student_email=student_email).first()

    if not user or not user.verify_password(password):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=user.user_id)
    current_app.logger.info(f"User logged in successfully: {student_email}")
    return jsonify(access_token=access_token, role=user.role), 200

# TO Test Access token and JWT authentication
@api_routes.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    current_app.logger.info(f"Protected route accessed by user: {user.student_email}")
    return jsonify(user.student_email), 200