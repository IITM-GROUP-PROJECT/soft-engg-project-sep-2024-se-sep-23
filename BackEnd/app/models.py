# db models file

from datetime import datetime
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    project_name = db.Column(db.String(264), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False)

    milestones = db.relationship("MilestoneVsProject", backref="project", lazy=True)


class Milestone(db.Model):
    __tablename__ = 'milestones'
    milestone_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    milestone_name = db.Column(db.String(264), nullable=False)
    description = db.Column(db.Text, nullable=False)

    projects = db.relationship("MilestoneVsProject", backref="milestone", lazy=True)


class MilestoneVsProject(db.Model):
    __tablename__ = 'milestonesvsprojects'
    milestone_project_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    milestone_id = db.Column(db.Integer, db.ForeignKey("milestones.milestone_id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    user_milestones = db.relationship("UserVsMilestone", backref="milestone_project", lazy=True)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    student_email = db.Column(db.String(269), nullable=False)
    github_username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.Integer, default=2, nullable=False)

    user_repositories = db.relationship("RepoVsUser", backref="user", lazy=True)
    user_milestones = db.relationship("UserVsMilestone", backref="user", lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, plaintext_password):
        self._password = generate_password_hash(plaintext_password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def is_admin(self):
        return self.role == 0

    def is_instructor(self):
        return self.role == 1

    def is_student(self):
        return self.role == 2


class Repository(db.Model):
    __tablename__ = 'repositories'
    repo_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    repo_name = db.Column(db.String(150), nullable=False)

    user_repositories = db.relationship("RepoVsUser", backref="repository", lazy=True)
    project_repositories = db.relationship("ProjectVsRepo", backref="repository", lazy=True)


class RepoVsUser(db.Model):
    __tablename__ = 'repovsusers'
    repo_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    repo_id = db.Column(db.Integer, db.ForeignKey("repositories.repo_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)


class ProjectVsRepo(db.Model):
    __tablename__ = 'projectvsrepos'
    project_repo_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"), nullable=False)
    repo_id = db.Column(db.Integer, db.ForeignKey("repositories.repo_id"), nullable=False)


class Commits(db.Model):
    __tablename__ = 'commits'
    commit_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    commit_message = db.Column(db.Text, nullable=True)
    commit_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    github_username = db.Column(db.String(150), nullable=False)
    repository = db.Column(db.String(150), nullable=False)


class UserVsMilestone(db.Model):
    __tablename__ = 'usersvsmilestones'
    user_milestone_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    milestone_project_id = db.Column(db.Integer, db.ForeignKey("milestonesvsprojects.milestone_project_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    is_completed = db.Column(db.Integer, default=0, nullable=False)


class Integration(db.Model):
    __tablename__ = 'integration'
    integration_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    details = db.Column(db.Text, nullable=False)
