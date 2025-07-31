from .database import db
from .models import User, Subject, Chapter, Quiz, Question, Score
from flask import current_app as app, jsonify, request, render_template
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify
from celery.result import AsyncResult
from .tasks import csv_report , monthly_report ,generate_msg
from flask import send_from_directory

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn) # allows us to reuse the decorator with multiple endpoints
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = current_user
            if not user or user.role not in roles:   
                return jsonify({"message": "You do not have access to this resource"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/' ,methods=['GET'])
def home():
    return render_template('index.html') ,200

@app.route('/api/admin')
@roles_required('admin')
def admin_home():
    user = current_user
    return {
        "message" : "admin logged in successfully"
    }

@app.route('/api/home')
@roles_required('admin','user')
def user_home():
    user = current_user
    return jsonify({
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "qualification": user.qualification,
        "dob": user.dob.isoformat() if user.dob else None,
        "role": user.role
    })

@app.route('/api/login', methods=['POST'])
def login():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')
    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400

    user = User.query.filter_by(email=email).one_or_none()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
            "qualification": user.qualification,
            "dob": user.dob.isoformat() if user.dob else None
        }), 200
    elif user:
        return jsonify({"message": "Invalid password"}), 400
    return jsonify({"message": "User not found"}), 404

@app.post('/api/register')
def register():
    credentials = request.get_json()
    required_fields = ["email", "username", "password"]
    for field in required_fields:
        if not credentials.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    if User.query.filter_by(email=credentials["email"]).first():
        return jsonify({"message": "user already exist"}), 400

    dob = credentials.get("dob")
    dob_obj = None
    if dob:
        from datetime import datetime
        try:
            dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid date format for dob. Use YYYY-MM-DD."}), 400

    user = User(
        email=credentials["email"],
        username=credentials["username"],
        password=generate_password_hash(credentials["password"]),
        full_name=credentials.get("full_name"),
        qualification=credentials.get("qualification"),
        dob=dob_obj,
        role="user"
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "user registered successfully"}), 201

@app.route('/api/profile', methods=['GET', 'PUT'])
@roles_required('admin','user')
def profile():
    user = current_user
    if request.method == 'GET':
        return jsonify({
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "qualification": user.qualification,
            "dob": user.dob.isoformat() if user.dob else None
        })
    elif request.method == 'PUT':
        data = request.get_json()
        user.full_name = data.get("full_name", user.full_name)
        user.qualification = data.get("qualification", user.qualification)
        if data.get("dob"):
            from datetime import datetime
            try:
                user.dob = datetime.strptime(data["dob"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"message": "Invalid date format for dob. Use YYYY-MM-DD."}), 400
        db.session.commit()
        return jsonify({"message": "Profile updated"}), 200

@app.get("/who_am_i")
@roles_required('admin','user')
def protected():
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role
    )

@app.route('/api/logout', methods=['POST'])
@roles_required('admin', 'user')
def logout():
    # For JWT, logout is handled client-side by deleting the token.
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/dashboard', methods=['GET'])
@roles_required('admin', 'user')
def dashboard():
    user = current_user
    if user.role == "admin":
        total_users = User.query.count()
        total_subjects = Subject.query.count()
        total_chapters = Chapter.query.count()
        total_quizzes = Quiz.query.count()
        total_scores = Score.query.count()
        return jsonify({
            "role": user.role,
            "total_users": total_users,
            "total_subjects": total_subjects,
            "total_chapters": total_chapters,
            "total_quizzes": total_quizzes,
            "total_scores": total_scores
        })
    else:
        total_attempted = Score.query.filter_by(user_id=user.id).count()
        avg_score = (
            db.session.query(db.func.avg(Score.total_scored))
            .filter(Score.user_id == user.id)
            .scalar()
        )
        subjects = Subject.query.all()
        return jsonify({
            "role": user.role,
            "total_quizzes_attempted": total_attempted,
            "average_score": float(avg_score) if avg_score is not None else 0,
            "subjects": [
                {"id": s.id, "name": s.name, "description": s.description}
                for s in subjects
            ]
        })

# backend jobs trigger
@app.route('/export_csv')
def export():
    result = csv_report.delay()
    return {
        "id":result.id, 
        "result":result.result
    }

@app.route('/api/csv_result/<id>') # just create to test the status of result
def csv_result(id):
    res = AsyncResult(id)
    # return {
    #     "filename": res.result
    # }
    return send_from_directory('static', res.result)

@app.route('/api/send_mail')
def send_mail():
    res = monthly_report.delay()
    return {
        "message": res.result
    }