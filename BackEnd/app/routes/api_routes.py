## all routes should be defined here

from flask import Blueprint, jsonify, request, current_app
from app.models import User
from app.extensions import db
from app.services.decorators import role
from app.services.logic import  authenticate_user,add_user

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
    response = add_user(data)
    current_app.logger.info(response.get("message"))
    if response.get("status"):
        return jsonify({"msg": "User created successfully"}), 200
    else:
        return jsonify(response), 400



# LOGIN API
@api_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response = authenticate_user(data)
    user = response.get("user")
    access_token = create_access_token(identity=user.user_id)
    current_app.logger.info(f"User logged in successfully!")
    return jsonify(access_token=access_token), 201

# TO Test Access token and JWT authentication
@api_routes.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    current_app.logger.info(f"Protected route accessed by user: {user.student_email}")
    return jsonify(user.student_email), 200