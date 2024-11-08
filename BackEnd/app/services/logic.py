# here we will create all business logic like how we process all app data
from flask import jsonify

from app.models import User
from app.utils import helpers
import json
import os
from dotenv import load_dotenv
from app.extensions import db



load_dotenv()


def process_project_report(filepath):
    report = helpers.pdf_to_text(filepath)
    guidelines = load_static_data().report_eval_prompt
    data = {"report":report,"guidelines": guidelines}
    response = helpers.ai_eval(data)

    if not response.status:
        return "Error while processing report with Gemini, Contact Support "
    else:
        return  response.text



def load_static_data():
    with open(os.getenv("APP_DATA_JSON_PATH", "app/resources/application_data.json")) as file:
        data = json.load(file)
    return data

def authenticate_user(data):
    response = {}
    student_email = data.get("student_email")
    password = data.get("password")

    user = User.query.filter_by(student_email=student_email).first()

    if not user or not user.verify_password(password):
        response["status"] = False
        response["message"] = "Bad email or password"
    else:
        response["status"] = True
        response["data"] = user

    return response

def add_user(data):
    response = {}

    student_email = data.get("student_email")
    github_username = data.get("github_username")
    password = data.get("password")

    if User.query.filter_by(student_email=student_email).first():
        response["status"] = False
        response["message"] = "Student email already exists."
        return response

    if User.query.filter_by(github_username=github_username).first():
        response["status"] = False
        response["message"] = "github username already exists."
        return response

    new_user = User(
        student_email=student_email,
        github_username=github_username,
        role=1
    )

    new_user.plain_password = password
    db.session.add(new_user)
    db.session.commit()

    response["status"] = True
    response["message"] = "User Successfully registered"

    return response




