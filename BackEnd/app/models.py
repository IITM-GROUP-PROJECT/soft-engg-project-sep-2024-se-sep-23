    # db models file

from datetime import datetime
from .extensions import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    github_username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    projects = db.relationship('StudentProject', back_populates='student')

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    projects = db.relationship('Project', back_populates='instructor')

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    problem = db.Column(db.Text, nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    instructor = db.relationship('Instructor', back_populates='projects')
    milestones = db.relationship('Milestone', back_populates='project', cascade='all, delete-orphan')
    students = db.relationship('StudentProject', back_populates='project')
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', back_populates='projects')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    projects = db.relationship('Project', back_populates='course')

class Milestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    project = db.relationship('Project', back_populates='milestones')
    student_milestones = db.relationship('StudentMilestone', back_populates='milestone', cascade='all, delete-orphan')

class StudentProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    github_repo_url = db.Column(db.String(200), nullable=True)
    project_report = db.Column(db.Text, nullable=True)
    report_created_at = db.Column(db.DateTime, nullable=True)
    student = db.relationship('Student', back_populates='projects')
    project = db.relationship('Project', back_populates='students')

class AIEvaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_project_id = db.Column(db.Integer, db.ForeignKey('student_project.id'), nullable=False)
    evaluation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    student_project = db.relationship('StudentProject', backref=db.backref('ai_evaluation', uselist=False))

class StudentMilestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    milestone_id = db.Column(db.Integer, db.ForeignKey('milestone.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    milestone_completion_date = db.Column(db.DateTime, nullable=True)
    milestone = db.relationship('Milestone', back_populates='student_milestones')

class Commits(db.Model):
    commit_id = db.Column(db.Integer, primary_key=True)
    commit_message = db.Column(db.String(300), unique=False, nullable=True)
    commit_sha = db.Column(db.String(256), unique=True, nullable=False)
    commit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)