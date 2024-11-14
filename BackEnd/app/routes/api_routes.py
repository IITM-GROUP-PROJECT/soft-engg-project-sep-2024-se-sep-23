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

@api_routes.route('/api/student_signup', methods=['POST'])
def student_signup():
    try:
        data = request.get_json()
        user = Student.query.filter_by(email=data['email']).first()
        if not user:
            hashed_password = generate_password_hash(data['password'])
            new_user = Student(email=data['email'], github_username=data['github_username'], password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=new_user.email, expires_delta=timedelta(seconds=3000))
            return jsonify({'message': 'Registered successfully', 'access_token': access_token}), 200

        return jsonify({'message': 'User already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
def create_project():
    data = request.json
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()

    # Create course if needed
    if data.get('new_course'):
        course = Course(
            name=data['course_name'],
        )
        db.session.add(course)
        db.session.commit()
        course_id = course.id
    else:
        course_id = data['course_id']
    
    # Step 1: Create the Project
    project = Project(
        title=data['title'],
        problem=data['problem'],
        instructor_id=instructor.id,
        course_id=course_id
    )
    db.session.add(project)
    db.session.commit()

    # Step 2: Add Milestones
    for milestone_data in data['milestones']:
        milestone = Milestone(
            title=milestone_data['title'],
            description=milestone_data['description'],
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
        repo_name = f"{project.title.replace(' ', '_')}-{student_id}-{unique_id}"

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

# API to edit project 
@api_routes.route('/api/edit_project/<int:project_id>', methods=['GET', 'PUT'])
@jwt_required()
def edit_project(project_id):
    email = get_jwt_identity()
    instructor = Instructor.query.filter_by(email=email).first()

    if request.method == 'GET':
        # Get project details including unassigned students
        project = Project.query.get_or_404(project_id)
        
        # Get currently assigned student IDs
        assigned_student_ids = [sp.student_id for sp in project.students]
        
        # Get unassigned students
        unassigned_students = Student.query.filter(~Student.id.in_(assigned_student_ids)).all()
        
        return jsonify({
            'project': {
                'id': project.id,
                'title': project.title,
                'problem': project.problem,
                'course_id': project.course_id,
                'milestones': [{
                    'id': m.id,
                    'title': m.title,
                    'description': m.description,
                    'deadline': m.deadline.strftime('%Y-%m-%d')
                } for m in project.milestones],
                'assigned_students': assigned_student_ids,
            },
            'unassigned_students': [{
                'id': s.id,
                'email': s.email,
                'github_username': s.github_username
            } for s in unassigned_students]
        })

    # Handle PUT request
    data = request.json
    project = Project.query.get_or_404(project_id)

    # Handle course creation/update
    if data.get('new_course'):
        course = Course(
            name=data['course_name'],
        )
        db.session.add(course)
        db.session.commit()
        course_id = course.id
    else:
        course_id = data['course_id']
    
    project.title = data['title']
    project.problem = data['problem']
    project.course_id = course_id

    # Update milestones
    existing_milestone_ids = set(m.id for m in project.milestones)
    updated_milestone_ids = set(m.get('id') for m in data['milestones'] if m.get('id'))


    # Update/Add milestones
    for milestone_data in data['milestones']:
        if milestone_data.get('id'):
            # Update existing milestone
            milestone = Milestone.query.get(milestone_data['id'])
            milestone.title = milestone_data['title']
            milestone.description = milestone_data['description']
            milestone.deadline = datetime.strptime(milestone_data['deadline'], '%Y-%m-%d')
        else:
            # Add new milestone
            milestone = Milestone(
                title=milestone_data['title'],
                description=milestone_data['description'],
                deadline=datetime.strptime(milestone_data['deadline'], '%Y-%m-%d'),
                project_id=project.id
            )
            db.session.add(milestone)

    # Delete removed milestones
    for milestone in project.milestones:
        if milestone.id not in updated_milestone_ids:
            # Delete associated StudentMilestone records first
            StudentMilestone.query.filter_by(milestone_id=milestone.id).delete()
            db.session.delete(milestone)

    # Handle new student assignments
    new_student_ids = set(data['student_ids']) - set(s.student_id for s in project.students)
    
    # Create repositories for new students
    github_token = "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"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    for student_id in new_student_ids:
        student = Student.query.get(student_id)
        if not student or not student.github_username:
            continue

        unique_id = uuid.uuid4().hex[:6]
        repo_name = f"{project.title.replace(' ', '_')}-{student_id}-{unique_id}"

        repo_payload = {
            "name": repo_name,
            "description": "This is your project repository",
            "private": True,
            "has_issues": True,
            "has_projects": True,
            "has_wiki": True
        }

        try:
            response = requests.post(
                "https://api.github.com/orgs/integrationTestORG12/repos", 
                json=repo_payload, 
                headers=headers
            )
            response.raise_for_status()
            repo_data = response.json()
            github_repo_url = f"https://github.com/{repo_data['full_name']}"

            # Add student to project
            student_project = StudentProject(
                student_id=student_id,
                project_id=project.id,
                github_repo_url=github_repo_url
            )
            db.session.add(student_project)

            # Add student as collaborator
            collaborator_url = f"https://api.github.com/repos/integrationTestORG12/{repo_name}/collaborators/{student.github_username}"
            collaborator_payload = {"permission": "maintain"}
            collaborator_response = requests.put(
                collaborator_url, 
                json=collaborator_payload, 
                headers=headers
            )
            collaborator_response.raise_for_status()

        except requests.RequestException as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    db.session.commit()
    return jsonify({"msg": "Project updated successfully"})

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
            'course': project.course.name,
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