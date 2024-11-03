## all routes should be defined here

from flask import Blueprint, jsonify, request
from app.models import User
from app.extensions import db
from app.services.decorators import role


api_routes = Blueprint("api", __name__)

@api_routes.route("/users", methods=["GET"])
# @role("admin")
# @role("instructor")
def get_users():

    from app.jobs.jobs import simpleTask
    print(simpleTask.delay())
    print("test")
    return "test"

