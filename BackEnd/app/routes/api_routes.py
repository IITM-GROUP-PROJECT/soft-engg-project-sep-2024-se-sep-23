## all routes should be defined here

from flask import Blueprint, jsonify, request
from app.models import User
from app.extensions import db

api_routes = Blueprint("api", __name__)

@api_routes.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

@api_routes.route("/users/create", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201
