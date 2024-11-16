# services/project_service.py
from app.models import *
from datetime import datetime
import uuid
import requests
from flask import jsonify
from app.extensions import db


class ProjectService:
    @staticmethod
    def create_project(data, instructor_email):
        try:
            instructor = Instructor.query.filter_by(email=instructor_email).first()
            
            # Create or get course
            course_id = ProjectService._handle_course(data)
            
            # Create project
            project = ProjectService._create_project_record(data, instructor.id, course_id)
            
            # Create milestones
            ProjectService._create_milestones(project.id, data['milestones'])
            
            # Handle student assignments and GitHub repos
            ProjectService._assign_students_to_project(project, data['student_ids'])
            
            db.session.commit()
            return {"msg": "Project created successfully"}, 201
            
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def _handle_course(data):
        if data.get('new_course'):
            course = Course(name=data['course_name'])
            db.session.add(course)
            db.session.commit()
            return course.id
        return data['course_id']

    @staticmethod
    def _create_project_record(data, instructor_id, course_id):
        project = Project(
            title=data['title'],
            problem=data['problem'],
            instructor_id=instructor_id,
            course_id=course_id
        )
        db.session.add(project)
        db.session.commit()
        return project

    @staticmethod
    def _create_milestones(project_id, milestones_data):
        for milestone_data in milestones_data:
            milestone = Milestone(
                title=milestone_data['title'],
                description=milestone_data['description'],
                deadline=datetime.strptime(milestone_data['deadline'], '%Y-%m-%d'),
                project_id=project_id
            )
            db.session.add(milestone)

    @staticmethod
    def _assign_students_to_project(project, student_ids):
        github_token = "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"
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json"
        }

        for student_id in student_ids:
            student = Student.query.get(student_id)
            if not student or not student.github_username:
                continue

            unique_id = uuid.uuid4().hex[:6]
            repo_name = f"{project.title.replace(' ', '_')}-{student_id}-{unique_id}"
            ProjectService._create_github_repo(project, student, repo_name, headers)

    @staticmethod
    def get_project_details(project_id):
        project = Project.query.get_or_404(project_id)
        assigned_student_ids = [sp.student_id for sp in project.students]
        unassigned_students = Student.query.filter(~Student.id.in_(assigned_student_ids)).all()
        
        return {
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
        }

    @staticmethod
    def update_project(project_id, data):
        project = Project.query.get_or_404(project_id)
        
        # Create or get course
        course_id = ProjectService._handle_course(data)
        
        # Update project details
        project.title = data['title']
        project.problem = data['problem']
        project.course_id = course_id

        # Handle milestones
        ProjectService._handle_milestones(project, data['milestones'])
        
        # Handle new students
        ProjectService._handle_new_students(project, data['student_ids'])
        
        db.session.commit()
        return {"msg": "Project updated successfully"}

    @staticmethod
    def _handle_milestones(project, milestone_data_list):
        updated_milestone_ids = set(m.get('id') for m in milestone_data_list if m.get('id'))
        
        # Delete removed milestones
        for milestone in project.milestones:
            if milestone.id not in updated_milestone_ids:
                print("milestone")
                print(milestone)
                StudentMilestone.query.filter_by(milestone_id=milestone.id).delete()
                db.session.delete(milestone)
                
        # Update/Add milestones
        for milestone_data in milestone_data_list:
            if milestone_data.get('id'):
                print("milestone_data")
                print(milestone_data)
                milestone = Milestone.query.get(milestone_data['id'])
                milestone.title = milestone_data['title']
                milestone.description = milestone_data['description']
                milestone.deadline = datetime.strptime(milestone_data['deadline'], '%Y-%m-%d')
            else:
                print(milestone_data)
                milestone = Milestone(
                    title=milestone_data['title'],
                    description=milestone_data['description'],
                    deadline=datetime.strptime(milestone_data['deadline'], '%Y-%m-%d'),
                    project_id=project.id
                )
                print(milestone)
                print(milestone.project_id)
                print(project.milestones)
                db.session.add(milestone)
                db.session.commit()

    @staticmethod
    def _handle_new_students(project, student_ids):
        new_student_ids = set(student_ids) - set(s.student_id for s in project.students)
        print(new_student_ids)
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
            
            # Create repository
            ProjectService._create_github_repo(project, student, repo_name, headers)

    @staticmethod
    def _create_github_repo(project, student, repo_name, headers):
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

            student_project = StudentProject(
                student_id=student.id,
                project_id=project.id,
                github_repo_url=github_repo_url
            )
            db.session.add(student_project)

            # Add collaborator
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
            raise e
        
    @staticmethod
    def delete_project(project_id, instructor_email):
        """
        Delete a project and all its related records
        """
        try:
            # Verify instructor ownership
            instructor = Instructor.query.filter_by(email=instructor_email).first()
            if not instructor:
                return {"msg": "Instructor not found"}, 404
    
            project = Project.query.filter_by(id=project_id, instructor_id=instructor.id).first()
            if not project:
                return {"msg": "Project not found"}, 404
    
            # Delete StudentMilestone records
            StudentMilestone.query.filter_by(project_id=project_id).delete()
            
            # Delete StudentProject records
            StudentProject.query.filter_by(project_id=project_id).delete()
            
            # Delete project (milestones will be deleted by cascade)
            db.session.delete(project)
            db.session.commit()
            
            return {"msg": "Project deleted successfully"}, 200
            
        except Exception as e:
            db.session.rollback()
            return {"msg": f"Error deleting project: {str(e)}"}, 500