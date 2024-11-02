## all routes should be defined here

from flask import Blueprint, jsonify, request
from app.models import User
from app.extensions import db

api_routes = Blueprint("api", __name__)

@api_routes.route("/users", methods=["GET"])
def get_users():
    return "test"

