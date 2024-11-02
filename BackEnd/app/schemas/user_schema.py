# data validation done here (kindly refer marshmellow on youtube for more info)

from marshmallow import Schema, fields, validate
from datetime import datetime

class ProjectSchema(Schema):
    project_id = fields.Int(dump_only=True)
    project_name = fields.Str(required=True, validate=validate.Length(max=264))
    description = fields.Str(allow_none=True)
    deadline = fields.DateTime(required=True)

class MilestoneSchema(Schema):
    milestone_id = fields.Int(dump_only=True)
    milestone_name = fields.Str(required=True, validate=validate.Length(max=264))
    description = fields.Str(required=True)

class MilestoneVsProjectSchema(Schema):
    milestone_project_id = fields.Int(dump_only=True)
    milestone_id = fields.Int(required=True)
    project_id = fields.Int(required=True)
    deadline = fields.DateTime(required=True)

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    student_email = fields.Email(required=True, validate=validate.Length(max=269))
    github_username = fields.Str(required=True, validate=validate.Length(max=150))
    password = fields.Str(required=True, validate=validate.Length(max=150))
    role = fields.Int(required=True, default=2)

class RepositorySchema(Schema):
    repo_id = fields.Int(dump_only=True)
    repo_name = fields.Str(required=True, validate=validate.Length(max=150))

class RepoVsUserSchema(Schema):
    repo_user_id = fields.Int(dump_only=True)
    repo_id = fields.Int(required=True)
    user_id = fields.Int(required=True)

class ProjectVsRepoSchema(Schema):
    project_repo_id = fields.Int(dump_only=True)
    project_id = fields.Int(required=True)
    repo_id = fields.Int(required=True)

class CommitSchema(Schema):
    commit_id = fields.Int(dump_only=True)
    commit_message = fields.Str(allow_none=True)
    commit_date = fields.DateTime(required=True, default=datetime.utcnow)
    github_username = fields.Str(required=True, validate=validate.Length(max=150))
    repository = fields.Str(required=True, validate=validate.Length(max=150))

class UserVsMilestoneSchema(Schema):
    user_milestone_id = fields.Int(dump_only=True)
    milestone_project_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    is_completed = fields.Int(required=True, validate=validate.OneOf([0, 1]))


class IntegrationSchema(Schema):
    integration_id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=150))
    details = fields.Str(required=True)