# professor_routes.py
from flask import Blueprint, jsonify
from app.models import Project
from app.decorators import instructor_required

professor_routes = Blueprint("professor", __name__)

@professor_routes.route('/prof/projects/<int:project_id>', methods=['GET'])
def get_prof_project_details(project_id):
    project = Project.query.get_or_404(project_id)
    
    return jsonify({
        'id': project.id,
        'title': project.title,
        'problem': project.problem,
        'course': project.course.name,
        'instructor': {
            'id': project.instructor.id,
            'email': project.instructor.email
        },
        'milestones': [{
            'title': m.title,
            'description': m.description,
            'deadline': m.deadline.isoformat()
        } for m in project.milestones]
    }), 200