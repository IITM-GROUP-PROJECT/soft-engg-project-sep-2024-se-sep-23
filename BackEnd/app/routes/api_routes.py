## all routes should be defined here

from flask import Blueprint, jsonify, request
from app.models import *
from app.extensions import db
from app.services.project_services import ProjectService
from app.decorators import instructor_required, student_required

from flask import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from sqlalchemy import func


from dotenv import load_dotenv
import google.generativeai as genai

from datetime import datetime

import os

api_routes = Blueprint("api", __name__)

@api_routes.route('/api/instructor_login', methods=['POST'])
def instructor_login():
    data = request.get_json()
    user = Instructor.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Bad credentials'}), 401

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(seconds=900))
    return jsonify({'access_token': access_token}), 200

@api_routes.route('/api/student_login', methods=['POST'])
def student_login():
    data = request.get_json()
    user = Student.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Bad credentials'}), 401

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(seconds=900))
    return jsonify({'access_token': access_token}), 200

@api_routes.route('/api/instructor_signup', methods=['POST'])
def instructor_signup():
    try:
        data = request.get_json()
        email = data['email']
        
        # Check if email already exists in Student or Instructor tables
        if Student.query.filter_by(email=email).first() or Instructor.query.filter_by(email=email).first():
            return jsonify({'message': 'Already Signed up. Email already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = Instructor(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.email, expires_delta=timedelta(seconds=3000))
        return jsonify({'message': 'Registered successfully', 'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_routes.route('/api/student_signup', methods=['POST'])
def student_signup():
    try:
        data = request.get_json()
        email = data['email']
        
        # Check if email already exists in Student or Instructor tables
        if Student.query.filter_by(email=email).first() or Instructor.query.filter_by(email=email).first():
            return jsonify({'message': 'Already Signed up. Email already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = Student(email=email, github_username=data['github_username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.email, expires_delta=timedelta(seconds=3000))
        return jsonify({'message': 'Registered successfully', 'access_token': access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API for Instructor Dashboard
@api_routes.route('/api/instructor_dashboard', methods=['GET'])
@jwt_required()
@instructor_required
def instructor_dashboard():
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()
    projects = instructor.projects
    return jsonify([{
        'id': project.id,
        'title': project.title,
        'problem': project.problem,
        'course': project.course.name,
        'student_count': len(project.students),  # Count of StudentProject relations
        'milestone_count': len(project.milestones)  # Count of Milestone relations
    } for project in projects]), 200


# API to get list of all Students needed to create a new Project
@api_routes.route('/api/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    return jsonify([{
        'id': student.id,
        'email': student.email
    } for student in students]), 200

# API to get list of all Courses needed to create a new Project
@api_routes.route('/api/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in courses])

# API to create a new Course (not in use)
@api_routes.route('/api/create_course', methods=['POST'])
@jwt_required()
def create_course():
    data = request.json

    course = Course(
        name=data['name'],
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'id': course.id, 'name': course.name}), 201

import requests
import uuid

# API to create a new Project
@api_routes.route('/api/create_project', methods=['POST'])
@jwt_required()
@instructor_required
def create_project():
    try:
        data = request.json
        email = get_jwt_identity()
        
        result, status_code = ProjectService.create_project(data, email)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_routes.route('/api/edit_project/<int:project_id>', methods=['GET', 'PUT'])
@jwt_required()
@instructor_required
def edit_project(project_id):
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()

    if request.method == 'GET':
        try:
            project_details = ProjectService.get_project_details(project_id)
            return jsonify(project_details)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Handle PUT request
    try:
        data = request.json
        result = ProjectService.update_project(project_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API to get list of all Projects assigned at the Student Dashboard 
@api_routes.route('/api/student_dashboard', methods=['GET'])
@jwt_required()
@student_required
def student_dashboard():
    email = get_jwt_identity()
    student = Student.query.filter_by(email=email).first()
    student_projects = StudentProject.query.filter_by(student_id=student.id).all()
    projects = []
    for sp in student_projects:
        project = Project.query.get(sp.project_id)
        projects.append({
            'id': project.id,
            'title': project.title,
            'problem': project.problem,
            'course': project.course.name,
            'github_repo_url': sp.github_repo_url
        })
    return jsonify(projects), 200


# API to get Project Info for a Student
@api_routes.route('/api/project_info/<int:project_id>', methods=['GET'])
@jwt_required()
@student_required
def get_project_info(project_id):
    email = get_jwt_identity()
    student = Student.query.filter_by(email=email).first()
    student_project = StudentProject.query.filter_by(student_id=student.id, project_id=project_id).first()
    if not student_project:
        return jsonify({"msg": "Project not found"}), 404

    project = Project.query.get(project_id)
    milestones = Milestone.query.filter_by(project_id=project_id).all()
    student_milestones = StudentMilestone.query.filter_by(student_id=student.id, project_id=project_id).all()

    return jsonify({
        'title': project.title,
        'problem': project.problem,
        'course': project.course.name,
        'milestones': [{
            'id': milestone.id,
            'title': milestone.title,
            'description': milestone.description,
            'deadline': milestone.deadline.strftime('%Y-%m-%d'),
            'status': next((sm.status for sm in student_milestones if sm.milestone_id == milestone.id), 'Pending')
        } for milestone in milestones],
        'github_repo_url': student_project.github_repo_url,
        'project_report': student_project.project_report
    }), 200


# API to Save Project Progress and Resources for a Student
@api_routes.route('/api/project_info/<int:project_id>', methods=['POST'])
@jwt_required()
@student_required
def update_project_info(project_id):
    data = request.json
    email = get_jwt_identity()
    student = Student.query.filter_by(email=email).first()
    student_project = StudentProject.query.filter_by(student_id=student.id, project_id=project_id).first()
    if not student_project:
        return jsonify({"msg": "Project not found"}), 404

    student_project.github_repo_url = data.get('github_repo_url', student_project.github_repo_url)
    student_project.project_report = data.get('project_report', student_project.project_report)

    for milestone_data in data['milestones']:
        student_milestone = StudentMilestone.query.filter_by(
            student_id=student.id,
            project_id=project_id,
            milestone_id=milestone_data['id']
        ).first()
        if student_milestone:
            student_milestone.status = milestone_data['status']
        else:
            new_student_milestone = StudentMilestone(
                student_id=student.id,
                project_id=project_id,
                milestone_id=milestone_data['id'],
                status=milestone_data['status']
            )
            db.session.add(new_student_milestone)

    db.session.commit()
    return jsonify({"msg": "Project info updated successfully"}), 200


# API to get Project Details for an Instructor
@api_routes.route('/api/project_details/<int:project_id>', methods=['GET'])
@jwt_required()
@instructor_required
def get_project_details(project_id):
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()
    
    # Ensure the project belongs to the instructor
    project = Project.query.filter_by(id=project_id, instructor_id=instructor.id).first()
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    # Retrieve milestones and current assigned students
    milestones = Milestone.query.filter_by(project_id=project_id).all()
    student_projects = StudentProject.query.filter_by(project_id=project_id).all()
    assigned_students = [Student.query.get(sp.student_id) for sp in student_projects]

    # Retrieve all students for potential assignment
    all_students = Student.query.all()

    return jsonify({
        'title': project.title,
        'problem': project.problem,
        'course': project.course.name,
        'milestones': [{
            'id': milestone.id,
            'title': milestone.title,
            'description': milestone.description,
            'deadline': milestone.deadline.strftime('%Y-%m-%d')
        } for milestone in milestones],
        'students': [{
            'id': student.id,
            'email': student.email
        } for student in assigned_students],
        'students_add': [{
            'id': student.id,
            'email': student.email,
            'github_username': student.github_username
        } for student in all_students]
    }), 200

@api_routes.route('/api/delete_project/<int:project_id>', methods=['DELETE'])
@jwt_required()
@instructor_required
def delete_project(project_id):
    email = get_jwt_identity()
    return ProjectService.delete_project(project_id, email)


# API to get information about a student's progress on a project
@api_routes.route('/api/track_progress/<int:project_id>/<int:student_id>', methods=['GET'])
@jwt_required()
@instructor_required
def track_progress(project_id, student_id):
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()
    project = Project.query.filter_by(id=project_id, instructor_id=instructor.id).first()
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    student_project = StudentProject.query.filter_by(student_id=student_id, project_id=project_id).first()
    if not student_project:
        return jsonify({"msg": "Student not assigned to this project"}), 404

    milestones = Milestone.query.filter_by(project_id=project_id).all()
    student_milestones = StudentMilestone.query.filter_by(student_id=student_id, project_id=project_id).all()

    return jsonify({
        'title': project.title,
        'problem': project.problem,
        'milestones': [{
            'id': milestone.id,
            'text': milestone.title,
            'description': milestone.description,
            'deadline': milestone.deadline.strftime('%Y-%m-%d'),
            'status': next((sm.status for sm in student_milestones if sm.milestone_id == milestone.id), 'Pending')
        } for milestone in milestones],
        'github_repo_url': student_project.github_repo_url,
        'project_report': student_project.project_report
    }), 200


load_dotenv()

# api to get ai (gemini) insights
@api_routes.route('/api/ai_eval', methods=['POST'])
def ai_evaluation():
    try:
        # Get the API key from .env file
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Get report from request
        data = request.get_json()
        report = data.get('report')
        # Define evaluation guidelines
        guidelines = """
        Please evaluate this project report based on the following criteria:
        1. Technical depth and understanding
        2. Implementation completeness
        3. Documentation quality
        4. Problem-solving approach
        5. Innovation and creativity
        
        Provide specific feedback for each criterion and suggestions for improvement.
        """
        
        # Generate evaluation
        prompt = f"Evaluate the report based on the guidelines. Guidelines: {guidelines}. Report: {report}"
        response = model.generate_content(prompt)
       
        return jsonify({
            'evaluation': response.text
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@api_routes.route('/api/get-commit-data', methods=['GET'])
@jwt_required()
@instructor_required
def get_commit_data():
    user_id = request.args.get('userId')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:

        commit_data = db.session.query(
            func.date(Commits.commit_date).label('commit_date'),
            func.count(Commits.commit_id).label('commit_count')
        ).filter_by(user_id=user_id).group_by(func.date(Commits.commit_date)).all()
        formatted_data = [
            {"date": commit_date, "commits": commit_count}
            for commit_date, commit_count in commit_data
        ]
        return jsonify(formatted_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_routes.route('/api/fetch-commits', methods=['POST'])
@jwt_required()
@instructor_required
def fetch_commits():
    data = request.json
    owner = data.get('owner')
    repo = data.get('repo')
    user_id = data.get('userId')
    try:

        headers =\
            {
            'Authorization': 'Bearer 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',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/commits', headers=headers)

        if response.status_code == 409:
            return jsonify({"error": "No commits found for this repository"}), 409

        if not response.ok:
            return jsonify({"error": "Failed to fetch commit data"}), response.status_code

        commits = response.json()


        for commit in commits:
            sha = commit['sha']
            message = commit['commit']['message']
            date = commit['commit']['author']['date']
            db.session.flush()

            if not Commits.query.filter_by(commit_sha=sha).first():
                new_commit = Commits(
                    commit_message=message,
                    commit_sha=sha,
                    commit_date=datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"),
                    user_id=user_id
                )
                db.session.add(new_commit)
                print(new_commit)

        db.session.commit()
        return jsonify({"message": "Commits fetched and stored successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
