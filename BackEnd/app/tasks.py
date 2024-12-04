# tasks.py
from celery_app import celery
from flask_mail import Message
from .extensions import mail

@celery.task
def send_email(subject, recipients, body):
    msg = Message(subject=subject, recipients=recipients, body=body)
    mail.send(msg)