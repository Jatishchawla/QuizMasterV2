from application.database import db
from application.models import User, Subject, Chapter, Quiz, Question
from application.config import LocalDevelopmentConfig
from application.resources import api
from application.security import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask import session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import uuid
import bcrypt
from datetime import timedelta
from application.celery_init import celery_init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)  # 12 hours
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=["http://localhost:5173"])
    api.init_app(app)
    app.app_context().push()
    return app



app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        monthly_report.s(),
    )

with app.app_context():
    db.create_all()
    # Create admin user if not exists
    if not User.query.filter_by(email="admin@quiz.com").first():
        user = User(
            email="admin@quiz.com",
            username="admin",
            password=generate_password_hash("1111"),
            full_name="Quiz Master",
            role="admin"
        )
        db.session.add(user)
    # Create normal user if not exists
    if not User.query.filter_by(email="user1@quiz.com").first():
        user = User(
            email="user1@quiz.com",
            username="user1",
            password=generate_password_hash("1234"),
            full_name="First User",
            role="user"
        )
        db.session.add(user)
    db.session.commit()




from application.routes import *

if __name__ == "__main__":
    app.run()