# admin_routes.py
from flask import Blueprint, jsonify, request
from app.models import *
from app.extensions import db
from app.decorators import admin_required
from werkzeug.security import generate_password_hash

admin_routes = Blueprint("admin", __name__)

@admin_routes.route('/students', methods=['GET'])
@admin_required
def get_all_students():
    students = Student.query.all()
    return jsonify([{
        'id': s.id,
        'email': s.email,
        'github_username': s.github_username
    } for s in students]), 200


@admin_routes.route('/students/<int:id>', methods=['GET'])
@admin_required
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({
        'id': student.id,
        'email': student.email,
        'github_username': student.github_username
    }), 200

@admin_routes.route('/students', methods=['POST'])
@admin_required
def create_student():
    data = request.get_json()
    
    if not all(k in data for k in ('email', 'github_username', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    student = Student(
        email=data['email'],
        github_username=data['github_username'],
        password=generate_password_hash(data['password'])
    )
    
    db.session.add(student)
    db.session.commit()
    
    return jsonify({
        'id': student.id,
        'email': student.email,
        'github_username': student.github_username
    }), 201

@admin_routes.route('/students/<int:id>', methods=['PUT'])
@admin_required
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    
    if 'email' in data:
        student.email = data['email']
    if 'github_username' in data:
        student.github_username = data['github_username']
    if 'password' in data:
        student.password = generate_password_hash(data['password'])
        
    db.session.commit()
    
    return jsonify({
        'id': student.id,
        'email': student.email,
        'github_username': student.github_username
    }), 200

@admin_routes.route('/students/<int:id>', methods=['DELETE'])
@admin_required
def delete_student(id):
    try:
        # Start transaction
        student = Student.query.get_or_404(id)
        
        # Delete associated student milestones
        StudentMilestone.query.filter_by(student_id=id).delete()
        
        # Get all student projects to delete AI evaluations
        student_projects = StudentProject.query.filter_by(student_id=id).all()
        for student_project in student_projects:
            # Delete associated AI evaluation if exists
            if student_project.ai_evaluation:
                db.session.delete(student_project.ai_evaluation)
        
        # Delete all student projects
        StudentProject.query.filter_by(student_id=id).delete()
        
        # Finally delete the student
        db.session.delete(student)
        db.session.commit()
        return 'Student Deleted', 204
        
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

# Instructor Account Management
@admin_routes.route('/instructors', methods=['GET'])
@admin_required
def get_all_instructors():
    instructors = Instructor.query.all()
    return jsonify([{
        'id': i.id,
        'email': i.email
    } for i in instructors]), 200

@admin_routes.route('/instructors/<int:id>', methods=['GET'])
@admin_required
def get_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    return jsonify({
        'id': instructor.id,
        'email': instructor.email
    }), 200

@admin_routes.route('/instructors', methods=['POST'])
@admin_required
def create_instructor():
    data = request.get_json()
    
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if Instructor.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    instructor = Instructor(
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    
    db.session.add(instructor)
    db.session.commit()
    
    return jsonify({
        'id': instructor.id,
        'email': instructor.email
    }), 201

@admin_routes.route('/instructors/<int:id>', methods=['PUT'])
@admin_required
def update_instructor(id):
    instructor = Instructor.query.get_or_404(id)
    data = request.get_json()
    
    if 'email' in data:
        instructor.email = data['email']
    if 'password' in data:
        instructor.password = generate_password_hash(data['password'])
        
    db.session.commit()
    
    return jsonify({
        'id': instructor.id,
        'email': instructor.email
    }), 200

@admin_routes.route('/instructors/<int:id>', methods=['DELETE'])
@admin_required
def delete_instructor(id):
    try:
        instructor = Instructor.query.get_or_404(id)
        
        # Get all projects by instructor
        instructor_projects = Project.query.filter_by(instructor_id=id).all()
        
        for project in instructor_projects:
            # Delete student milestones for this project
            StudentMilestone.query.filter_by(project_id=project.id).delete()
            
            # Handle student projects and their AI evaluations
            student_projects = StudentProject.query.filter_by(project_id=project.id).all()
            for student_project in student_projects:
                # Delete AI evaluation if exists
                if student_project.ai_evaluation:
                    db.session.delete(student_project.ai_evaluation)
            
            # Delete all student projects for this project
            StudentProject.query.filter_by(project_id=project.id).delete()
            
            # Delete all milestones (cascade will handle student_milestones)
            Milestone.query.filter_by(project_id=project.id).delete()
            
            # Delete the project
            db.session.delete(project)
        
        # Finally delete the instructor
        db.session.delete(instructor)
        db.session.commit()
        return 'Instructor Deleted', 204
        
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500