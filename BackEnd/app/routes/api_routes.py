## major routes should be defined here
import json

# Importing required libraries
from app.models import *
from app.extensions import db
from app.services.project_services import ProjectService
from app.decorators import instructor_required, student_required
from flask import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from sqlalchemy import func
from collections import defaultdict
import fitz


import re
from sqlalchemy.exc import SQLAlchemyError

from dotenv import load_dotenv
import google.generativeai as genai

from datetime import datetime
from pytz import timezone
import requests

# Set timezone to IST
ist = timezone('Asia/Kolkata')

import os

# from BackEnd.app.models import *
GET_UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = {'pdf'}

api_routes = Blueprint("api", __name__)

# API for Instructor Login
@api_routes.route('/api/instructor_login', methods=['POST'])
def instructor_login():
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400

        try:
            user = Instructor.query.filter_by(email=data['email']).first()
        except SQLAlchemyError as e:
            return jsonify({'message': 'Database error', 'error': str(e)}), 500

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401

        try:
            access_token = create_access_token(
                identity=user.email,
                expires_delta=timedelta(seconds=900)
            )
            return jsonify({'access_token': access_token,  'instructor_id': user.id}), 200
        except Exception as e:
            return jsonify({'message': 'Error creating access token', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# API for Student Login
@api_routes.route('/api/student_login', methods=['POST'])
def student_login():
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400

        try:
            user = Student.query.filter_by(email=data['email']).first()
        except SQLAlchemyError as e:
            return jsonify({'message': 'Database error', 'error': str(e)}), 500

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401

        try:
            access_token = create_access_token(
                identity=user.email,
                expires_delta=timedelta(seconds=900)
            )
            return jsonify({'access_token': access_token}), 200
        except Exception as e:
            return jsonify({'message': 'Error creating access token', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# API for Instructor Signup
@api_routes.route('/api/instructor_signup', methods=['POST'])
def instructor_signup():
    try:
        data = request.get_json()

        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400

        email = data['email']

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'message': 'Invalid email format'}), 400

        # Validate password strength
        if len(data['password']) < 4:
            return jsonify({'message': 'Password must be at least 4 characters long'}), 400

        # Check if email already exists
        if Student.query.filter_by(email=email).first() or Instructor.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = Instructor(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        try:
            access_token = create_access_token(
                identity=new_user.email,
                expires_delta=timedelta(seconds=3000)
            )
            return jsonify({
                'message': 'Registered successfully',
                'access_token': access_token
            }), 200
        except Exception as e:
            return jsonify({'message': 'Error creating access token', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# API for Student Signup
@api_routes.route('/api/student_signup', methods=['POST'])
def student_signup():
    try:
        data = request.get_json()

        # Validate required fields
        if not all(key in data for key in ['email', 'password', 'github_username']):
            return jsonify({'message': 'Missing required fields'}), 400

        email = data['email']

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'message': 'Invalid email format'}), 400

        # Validate password strength
        if len(data['password']) < 4:
            return jsonify({'message': 'Password must be at least 4 characters long'}), 400

        # Validate github username
        if not data['github_username'].strip():
            return jsonify({'message': 'GitHub username cannot be empty'}), 400

        # Check if email already exists
        if Student.query.filter_by(email=email).first() or Instructor.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = Student(
            email=email,
            github_username=data['github_username'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        try:
            access_token = create_access_token(
                identity=new_user.email,
                expires_delta=timedelta(seconds=3000)
            )
            return jsonify({
                'message': 'Registered successfully',
                'access_token': access_token
            }), 200
        except Exception as e:
            return jsonify({'message': 'Error creating access token', 'error': str(e)}), 500

    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

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


# API to get list of all Students needed to create a new Project (no longer needed, modified to csv instead of checklist)
@api_routes.route('/api/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    return jsonify([{
        'id': student.id,
        'email': student.email
    } for student in students]), 200

# API to convert emails to IDs for project creation.
@api_routes.route('/api/get_student_ids', methods=['POST'])
@jwt_required()
@instructor_required
def get_student_ids():
    try:
        data = request.get_json()
        if not data or 'emails' not in data:
            return jsonify({'message': 'Missing emails list'}), 400
            
        emails = data['emails']
        registered_students = []
        unregistered_emails = []
        
        for email in emails:
            student = Student.query.filter_by(email=email).first()
            if student:
                registered_students.append(student.id)
            else:
                unregistered_emails.append(email)
                
        return jsonify({
            'registered_student_ids': registered_students,
            'unregistered_emails': unregistered_emails
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# API to send reminders to students not registered on the app to register on the portal
@api_routes.route('/api/send_reminder_to_register', methods=['POST'])
@jwt_required()
@instructor_required
def send_reminder_to_register():
    try:
        data = request.get_json()
        if not data or 'emails' not in data:
            return jsonify({'message': 'Missing emails list'}), 400
            
        emails = data['emails']

        from app.tasks import send_email
        send_email.delay('Final Reminder to Register', emails, 'Please register at the earlier on the IIT Madras Project Portal otherwise you will miss out on Project this term.')
        
        return jsonify({
            'message': 'Registration reminders sent successfully',
            'emails': data['emails']
        }), 200
        
    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

# API to get list of all Courses needed to create a new Project
@api_routes.route('/api/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in courses])

# API to create a new Project
@api_routes.route('/api/create_project', methods=['POST'])
@jwt_required()
@instructor_required
def create_project():
    try:
        if not request.is_json:
            return jsonify({'message': 'Missing JSON in request'}), 400

        data = request.json
        required_fields = ['title', 'problem', 'milestones', 'student_ids']

        # Check for required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        # Validate course data
        if not data.get('new_course') and not data.get('course_id'):
            return jsonify({'message': 'Either new_course or course_id must be provided'}), 400

        if data.get('new_course') and not data.get('course_name'):
            return jsonify({'message': 'Course name is required for new course'}), 400

        # Validate milestones data
        if not isinstance(data['milestones'], list):
            return jsonify({'message': 'Milestones must be a list'}), 400

        for milestone in data['milestones']:
            if not all(key in milestone for key in ['title', 'description', 'deadline']):
                return jsonify({'message': 'Invalid milestone data'}), 400
            try:
                datetime.strptime(milestone['deadline'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'message': 'Invalid deadline format. Use YYYY-MM-DD'}), 400

        # Validate student_ids
        if not isinstance(data['student_ids'], list):
            return jsonify({'message': 'student_ids must be a list'}), 400

        email = get_jwt_identity()
        result, status_code = ProjectService.create_project(data, email)
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

# API to edit a Project
@api_routes.route('/api/edit_project/<int:project_id>', methods=['GET', 'PUT'])
@jwt_required()
@instructor_required
def edit_project(project_id):
    try:
        email = get_jwt_identity()
        instructor = Instructor.query.filter_by(email=email).first()

        if not instructor:
            return jsonify({'message': 'Instructor not found'}), 404

        # Verify project ownership
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'message': 'Project not found'}), 404
        if project.instructor_id != instructor.id:
            return jsonify({'message': 'Unauthorized access'}), 403

        if request.method == 'GET':
            try:
                project_details = ProjectService.get_project_details(project_id)
                return jsonify(project_details), 200
            except Exception as e:
                return jsonify({"message": "Error retrieving project details", "error": str(e)}), 500

        # Handle PUT request
        if not request.is_json:
            return jsonify({'message': 'Missing JSON in request'}), 400

        data = request.json
        required_fields = ['title', 'problem', 'milestones', 'student_ids']

        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400

        # Validate milestones
        if not isinstance(data['milestones'], list):
            return jsonify({'message': 'Milestones must be a list'}), 400

        for milestone in data['milestones']:
            if not all(key in milestone for key in ['title', 'description', 'deadline']):
                return jsonify({'message': 'Invalid milestone data'}), 400
            try:
                datetime.strptime(milestone['deadline'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'message': 'Invalid deadline format. Use YYYY-MM-DD'}), 400

        try:
            result = ProjectService.update_project(project_id, data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"message": "Error updating project", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

# API to delete a Project
@api_routes.route('/api/delete_project/<int:project_id>', methods=['DELETE'])
@jwt_required()
@instructor_required
def delete_project(project_id):
    email = get_jwt_identity()
    return ProjectService.delete_project(project_id, email)

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
        'project_report': student_project.project_report,
    }), 200



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_pdf_to_text(pdf_path):
    pdf_text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pdf_text += page.get_text()
    return pdf_text

# API to update Project Info for a Student
@api_routes.route('/api/project_info/<int:project_id>', methods=['POST'])
@jwt_required()
@student_required
def update_project_info(project_id):
    try:
        data = json.loads(request.form.get('data'))

        # Validate required data
        if 'milestones' not in data:
            return jsonify({'message': 'Missing milestones data'}), 400

        if not isinstance(data['milestones'], list):
            return jsonify({'message': 'Milestones must be a list'}), 400

        # Validate milestone data
        for milestone in data['milestones']:
            if not isinstance(milestone, dict):
                return jsonify({'message': 'Invalid milestone format'}), 400
            if 'id' not in milestone or 'status' not in milestone:
                return jsonify({'message': 'Missing milestone id or status'}), 400
            if milestone['status'] not in ['Pending', 'Completed']:
                return jsonify({'message': 'Invalid milestone status'}), 400

        email = get_jwt_identity()
        student = Student.query.filter_by(email=email).first()
        if not student:
            return jsonify({'message': 'Student not found'}), 404

        # Validate project assignment
        student_project = StudentProject.query.filter_by(
            student_id=student.id,
            project_id=project_id
        ).first()
        if not student_project:
            return jsonify({'message': 'Project not found or not assigned to student'}), 404


        if 'project_report' in request.files:
            file = request.files['project_report']
            if file and allowed_file(file.filename):
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                fileName = str(project_id) + "_" + str(student.id) + "_projectReport.pdf"
                file_path = os.path.join(UPLOAD_FOLDER,fileName)
                file.save(file_path)
                pdf_text = convert_pdf_to_text(file_path)
                student_project.project_report = pdf_text
                student_project.report_created_at = datetime.now(ist)

        # Update milestones
        for milestone_data in data['milestones']:
            student_milestone = StudentMilestone.query.filter_by(
                student_id=student.id,
                project_id=project_id,
                milestone_id=milestone_data['id']
            ).first()

            if student_milestone:
                if (student_milestone.status == 'Pending' and
                    milestone_data['status'] == 'Completed'):
                    student_milestone.status = 'Completed'
                    student_milestone.milestone_completion_date = datetime.now(ist)
            else:
                new_student_milestone = StudentMilestone(
                    student_id=student.id,
                    project_id=project_id,
                    milestone_id=milestone_data['id'],
                    status=milestone_data['status']
                )
                if milestone_data['status'] == 'Completed':
                    new_student_milestone.milestone_completion_date = datetime.now(ist)
                db.session.add(new_student_milestone)

        db.session.commit()
        return jsonify({'message': 'Project info updated successfully'}), 200

    except Exception as e:
        return jsonify({
            'message': 'Internal server error',
            'error': str(e)
        }), 500



@api_routes.route('/api/project_info/project_report/<int:project_id>/<int:student_id>', methods=['GET'])
@jwt_required()
@instructor_required
def project_report(project_id, student_id):
    fileName = str(project_id) + "_" + str(student_id) + "_projectReport.pdf"
    file_path = os.path.join(GET_UPLOAD_FOLDER, fileName)

    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return {"message": "Report not submitted"}, 404

@api_routes.route('/api/project_info/student/project_report/<int:project_id>', methods=['GET'])
@jwt_required()
@student_required
def project_report_student(project_id):
    student_id = Student.query.filter_by(email=get_jwt_identity()).first().id
    fileName = str(project_id) + "_" + str(student_id) + "_projectReport.pdf"
    file_path = os.path.join(GET_UPLOAD_FOLDER, fileName)

    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return {"message": "Report not submitted"}, 404


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

    if student_project.report_created_at:
        report_created_at = student_project.report_created_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        report_created_at = None

    return jsonify({
        'title': project.title,
        'problem': project.problem,
        'milestones': [{
            'id': milestone.id,
            'text': milestone.title,
            'description': milestone.description,
            'deadline': milestone.deadline.strftime('%Y-%m-%d'),
            'status': next((sm.status for sm in student_milestones if sm.milestone_id == milestone.id), 'Pending'),
            'completion_date': next((sm.milestone_completion_date.strftime('%Y-%m-%d %H:%M:%S')
                                  for sm in student_milestones
                                  if sm.milestone_id == milestone.id and sm.milestone_completion_date), None)
        } for milestone in milestones],
        'github_repo_url': student_project.github_repo_url,
        'project_report': student_project.project_report,
        'report_created_at': report_created_at,
        'student_project_id': student_project.id,
        'report_url' : "http://127.0.0.1:5000/api/project_info/project_report/"+ str(project_id) + "/" + str(student_id)
    }), 200


load_dotenv()

@api_routes.route('/api/ai_eval/<int:student_project_id>', methods=['POST'])
@jwt_required()
@instructor_required
def ai_evaluation(student_project_id):
    try:
        # Get student project
        student_project = StudentProject.query.get_or_404(student_project_id)
        project = student_project.project

        # Check if report exists
        if not student_project.project_report:
            return jsonify({'error': 'No project report found'}), 400

        # Get the API key from .env file
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
            
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Define evaluation guidelines with project context
        guidelines = f"""
        Project Title: {project.title}
        Problem Statement: {project.problem}

        Please evaluate this project report based on the following criteria:
        1. Technical depth and understanding
        2. Implementation completeness
        3. Documentation quality
        4. Problem-solving approach
        5. Innovation and creativity
        
        Consider how well the solution addresses the original problem statement.
        Provide specific feedback for each criterion and suggestions for improvement.
        """
        
        # Generate evaluation
        prompt = f"Project Context and Guidelines: {guidelines}\n\nStudent Report: {student_project.project_report}"
        response = model.generate_content(prompt)

        # Store or update evaluation in database
        evaluation = AIEvaluation.query.filter_by(student_project_id=student_project_id).first()
        if evaluation:
            evaluation.evaluation = response.text
            evaluation.created_at = datetime.now(ist)
        else:
            evaluation = AIEvaluation(
                student_project_id=student_project_id,
                evaluation=response.text,
                created_at=datetime.now(ist)
            )
            db.session.add(evaluation)

        db.session.commit()

        return jsonify({
            'evaluation': response.text,
            'created_at': evaluation.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@api_routes.route('/api/stats', methods=['GET'])
@jwt_required()
def get_instructor_projects():
    # Fetch the current instructor's ID from JWT
    instructor_id = get_jwt_identity()

    # Fetch projects for the current instructor
    projects = Project.query.filter_by(instructor_id=instructor_id).all()

    projects_data = []
    for project in projects:
        # Prepare project data
        project_info = {
            'id': project.id,
            'title': project.title,
            'course': {
                'id': project.course.id,
                'name': project.course.name
            },
            'students': [],
            'milestones': []
        }

        # Add student details
        for student_project in project.students:
            student_info = {
                'id': student_project.student.id,
                'email': student_project.student.email,
                'github_repo_url': student_project.github_repo_url,
                'status': 'In Progress'  # Modify logic as needed
            }
            project_info['students'].append(student_info)

        # Add milestone details
        for milestone in project.milestones:
            milestone_info = {
                'id': milestone.id,
                'title': milestone.title,
                'deadline': milestone.deadline.isoformat(),
                'status': 'Completed' if milestone.student_milestones else 'Pending'
            }
            project_info['milestones'].append(milestone_info)

        projects_data.append(project_info)

    return jsonify(projects_data)

@api_routes.route('/api/ai_eval/<int:student_project_id>', methods=['GET'])
@jwt_required()
def get_ai_evaluation(student_project_id):
    evaluation = AIEvaluation.query.filter_by(student_project_id=student_project_id).first()
    if evaluation:
        return jsonify({
            'evaluation': evaluation.evaluation,
            'created_at': evaluation.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'evaluation': None}), 404

@api_routes.route('/api/get-commit-data', methods=['GET'])
@jwt_required()
@instructor_required
def get_commit_data():
    student_project_id = request.args.get('student_project_id')

    if not student_project_id:
        return jsonify({"error": "Student-Project ID is required"}), 400

    try:

        commit_data = db.session.query(
            func.date(Commits.commit_date).label('commit_date'),
            func.count(Commits.commit_id).label('commit_count')
        ).filter_by(student_project_id=student_project_id).group_by(func.date(Commits.commit_date)).all()
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
    student_project_id = data.get('student_project_id')
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
                    student_project_id=student_project_id
                )
                db.session.add(new_commit)
                print(new_commit)

        db.session.commit()
        return jsonify({"message": "Commits fetched and stored successfully"}), 200

    except Exception as e:  
        return jsonify({"error": str(e)}), 500
    



@api_routes.route('/api/instructor_stats/<int:instructor_id>', methods=['GET'])
def instructor_stats(instructor_id):

    # Fetch data from the database
    courses = (
        Course.query
        .join(Project, Course.id == Project.course_id)
        .filter(Project.instructor_id == instructor_id)
        .distinct()
        .all()
    )
    total_courses = len(courses)
    total_projects = Project.query.count()
    total_students = Student.query.count()
    print("Total courses:", total_courses, "Total projects:", total_projects,"Total students:" ,total_students)
    course_data = []
    for course in courses:
        course_projects = Project.query.filter_by(course_id=course.id).all()
        course_project_data = []
        for project in course_projects:
            milestones = Milestone.query.filter_by(project_id=project.id).all()
            students = StudentProject.query.filter_by(project_id=project.id).all()

            # Create a dictionary to hold stats per milestone title
            milestone_stats = defaultdict(lambda: {"completed": 0, "pending": 0, "deadline": None})

            # Iterate over milestones to get stats and deadlines
            for milestone in milestones:
                milestone_title = milestone.title
                milestone_id = milestone.id
                milestone_deadline = milestone.deadline.strftime('%a, %d %b %Y %H:%M:%S GMT')  # Get milestone deadline

                # Count completed and pending for the milestone from StudentMilestone table
                completed_count = StudentMilestone.query.filter_by(
                    milestone_id=milestone_id, project_id=project.id, status="Completed"
                ).count()

                pending_count = StudentMilestone.query.filter_by(
                    milestone_id=milestone_id, project_id=project.id, status="Pending"
                ).count()

                # Add counts for students who don't have a StudentMilestone entry (default to "Pending")
                total_student = len(students)
                students_with_entries = (
                    StudentMilestone.query.filter_by(milestone_id=milestone_id, project_id=project.id)
                    .distinct(StudentMilestone.student_id)
                    .count()
                )
                missing_entries_count = total_student - students_with_entries

                # Aggregate stats including the milestone deadline
                milestone_stats[milestone_title]["completed"] += completed_count
                milestone_stats[milestone_title]["pending"] += pending_count + missing_entries_count
                milestone_stats[milestone_title]["deadline"] = milestone_deadline

            # Convert defaultdict to a regular dictionary if needed
            milestone_stats = dict(milestone_stats)

            # Result Example
            result = [
                {
                    "title": title,
                    "completed": stats["completed"],
                    "pending": stats["pending"],
                    "deadline": stats["deadline"],  # Include deadline in the result
                }
                for title, stats in milestone_stats.items()
            ]

            project_students = StudentProject.query.filter_by(project_id=project.id).all()
            student_data = [
                {
                    "student_email": Student.query.filter_by(id=sp.student_id).first().email,
                    "github_repo_url": sp.github_repo_url,
                    "completed_milestones": StudentMilestone.query.filter_by(student_id=sp.student_id, project_id=project.id, status='Completed').count(),
                    "pending_milestones": StudentMilestone.query.filter_by(student_id=sp.student_id, project_id=project.id, status='Pending').count(),
                }
                for sp in project_students
            ]
            course_project_data.append({
                "project_id": project.id,
                "title": project.title,
                "students": student_data,
                "milestone_stats": milestone_stats,
            })
        course_data.append({
            "course_id": course.id,
            "name": course.name,
            "projects": course_project_data,
        })

    # Response structure
    response = {
        "overview": {
            "total_courses": total_courses,
            "total_projects": total_projects,
            "total_students": total_students,
        },
        "courses": course_data,
    }
    return jsonify(response)



