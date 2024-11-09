## all routes should be defined here

from flask import Blueprint, jsonify, request
from app.models import *
from app.extensions import db

from flask import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from dotenv import load_dotenv
import google.generativeai as genai

import os

api_routes = Blueprint("api", __name__)

@api_routes.route('/instructor_login', methods=['POST'])
def instructor_login():
    data = request.get_json()
    user = Instructor.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Bad credentials'}), 401

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(seconds=900))
    return jsonify({'access_token': access_token}), 200

@api_routes.route('/student_login', methods=['POST'])
def student_login():
    data = request.get_json()
    user = Student.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Bad credentials'}), 401

    access_token = create_access_token(identity=user.email, expires_delta=timedelta(seconds=900))
    return jsonify({'access_token': access_token}), 200

@api_routes.route('/instructor_signup', methods=['POST'])
def instructor_signup():
    data = request.get_json()
    user = Instructor.query.filter_by(email=data['email']).first()
    if not user:
        hashed_password = generate_password_hash(data['password'])
        new_user = Instructor(email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.email, expires_delta=timedelta(seconds=3000))
        return jsonify({'message': 'Registered successfully', 'access_token': access_token}), 200

    return jsonify({'message': 'User already exists'}), 400

@api_routes.route('/student_signup', methods=['POST'])
def student_signup():
    data = request.get_json()
    print(data)
    user = Student.query.filter_by(email=data['email']).first()
    if not user:
        hashed_password = generate_password_hash(data['password'])
        new_user = Student(email=data['email'], github_username = data['github_username'],password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.email, expires_delta=timedelta(seconds=3000))
        return jsonify({'message': 'Registered successfully', 'access_token': access_token}), 200

    return jsonify({'message': 'User already exists'}), 400


# API for Instructor Dashboard
@api_routes.route('/api/instructor_dashboard', methods=['GET'])
@jwt_required()
def instructor_dashboard():
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()
    projects = instructor.projects
    return jsonify([{
        'id': project.id,
        'title': project.title,
        'problem': project.problem,
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

import requests
import uuid

# API to create a new Project
@api_routes.route('/api/create_project', methods=['POST'])
@jwt_required()
def create_project():
    data = request.json
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()
    
    # Step 1: Create the Project
    project = Project(
        title=data['title'],
        problem=data['problem'],
        instructor_id=instructor.id
    )
    db.session.add(project)
    db.session.commit()

    # Step 2: Add Milestones
    for milestone_data in data['milestones']:
        milestone = Milestone(
            text=milestone_data['text'],
            deadline=datetime.strptime(milestone_data['deadline'], '%Y-%m-%d'),
            project_id=project.id
        )
        db.session.add(milestone)
    
    db.session.commit()

    # GitHub API authentication token
    github_token = "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"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    # Step 3: Create GitHub repository for each student and add as collaborator
    for student_id in data['student_ids']:
        # Fetch the student's GitHub username
        student = Student.query.get(student_id)
        if not student or not student.github_username:
            continue  # Skip if student or GitHub username is missing
        
        # Repository name format
        # Generate a unique repository name using a UUID
        unique_id = uuid.uuid4().hex[:6]
        repo_name = f"{project.title}-{student_id}-{unique_id}"

        # GitHub Repository creation payload
        repo_payload = {
            "name": repo_name,
            "description": "This is your project repository",
            "homepage": "https://github.com",
            "private": True,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        }

        # Create GitHub repository
        repo_url = f"https://api.github.com/orgs/integrationTestORG12/repos"
        try:
            response = requests.post(repo_url, json=repo_payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            repo_data = response.json()
            github_repo_url = f"https://github.com/{repo_data['full_name']}"
        except requests.RequestException as e:
            db.session.rollback()
            return jsonify({"error": "Failed to create GitHub repository", "details": str(e)}), 500

        # Store the GitHub repository URL in the database
        student_project = StudentProject(
            student_id=student_id,
            project_id=project.id,
            github_repo_url=github_repo_url
        )
        db.session.add(student_project)

        # Add student as a collaborator with 'maintain' permissions
        collaborator_url = f"https://api.github.com/repos/integrationTestORG12/{repo_name}/collaborators/{student.github_username}"
        collaborator_payload = {
            "permission": "maintain"
        }
        try:
            collaborator_response = requests.put(collaborator_url, json=collaborator_payload, headers=headers)
            collaborator_response.raise_for_status()
        except requests.RequestException as e:
            db.session.rollback()
            return jsonify({"error": "Failed to add collaborator", "details": str(e)}), 500

    # Final commit for student projects and GitHub URLs
    db.session.commit()
    return jsonify({"msg": "Project created successfully"}), 201


# API to get list of all Projects assigned at the Student Dashboard 
@api_routes.route('/api/student_dashboard', methods=['GET'])
@jwt_required()
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
            'github_repo_url': sp.github_repo_url
        })
    return jsonify(projects), 200


# API to get Project Info for a Student
@api_routes.route('/api/project_info/<int:project_id>', methods=['GET'])
@jwt_required()
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
        'milestones': [{
            'id': milestone.id,
            'text': milestone.text,
            'deadline': milestone.deadline.strftime('%Y-%m-%d'),
            'status': next((sm.status for sm in student_milestones if sm.milestone_id == milestone.id), 'Pending')
        } for milestone in milestones],
        'github_repo_url': student_project.github_repo_url,
        'project_report': student_project.project_report
    }), 200


# API to update Project Info for a Student
@api_routes.route('/api/project_info/<int:project_id>', methods=['POST'])
@jwt_required()
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
def get_project_details(project_id):
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()
    project = Project.query.filter_by(id=project_id, instructor_id=instructor.id).first()
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    milestones = Milestone.query.filter_by(project_id=project_id).all()
    student_projects = StudentProject.query.filter_by(project_id=project_id).all()
    students = [Student.query.get(sp.student_id) for sp in student_projects]

    return jsonify({
        'title': project.title,
        'problem': project.problem,
        'milestones': [{
            'id': milestone.id,
            'text': milestone.text,
            'deadline': milestone.deadline.strftime('%Y-%m-%d')
        } for milestone in milestones],
        'students': [{
            'id': student.id,
            'email': student.email
        } for student in students]
    }), 200


# API to delete Project Details for an Instructor
@api_routes.route('/api/delete_project/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()
    project = Project.query.filter_by(id=project_id, instructor_id=instructor.id).first()
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    try:
        # Delete StudentMilestone records
        StudentMilestone.query.filter_by(project_id=project_id).delete()
        
        # Delete StudentProject records
        StudentProject.query.filter_by(project_id=project_id).delete()
        
        # Delete project (milestones will be deleted by cascade)
        db.session.delete(project)
        db.session.commit()
        return jsonify({"msg": "Project deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error deleting project: {str(e)}"}), 500

# NEED to work on Updating an existing project


# API to get information about a student's progress on a project
@api_routes.route('/api/track_progress/<int:project_id>/<int:student_id>', methods=['GET'])
@jwt_required()
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
            'text': milestone.text,
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
        print('ai eval')
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
        print('response: ')
        print(response)        
        return jsonify({
            'evaluation': response.text
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500