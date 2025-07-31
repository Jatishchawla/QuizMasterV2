from flask_restful import Api, Resource, reqparse
from .models import *
# from flask_security import auth_required, roles_required, roles_accepted, current_user
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, current_user
from datetime import datetime, date
from .models import ist_now
from flask import request , jsonify
import json
from functools import wraps
api = Api()

def roles_list(roles):
    return [role.name for role in roles]



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


# --- Parsers ---
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('subject_id')
parser.add_argument('chapter_id')
parser.add_argument('date_of_quiz')
parser.add_argument('time_duration')
parser.add_argument('remarks')
parser.add_argument('quiz_id')
parser.add_argument('question_statement')
parser.add_argument('option1')
parser.add_argument('option2')
parser.add_argument('option3')
parser.add_argument('option4')
parser.add_argument('correct_option')  # already string by default
parser.add_argument('answers', type=dict, location='json')
parser.add_argument('marks', type=int)  # <-- add this line
parser.add_argument('question_type')  # "mcq" or "text"

# --- Subject Resource ---
class SubjectApi(Resource):
    @roles_required('admin' , 'user' )
    def get(self, subject_id=None):
        if subject_id:
            subject = Subject.query.get(subject_id)
            if subject:
                return {
                    "id": subject.id,
                    "name": subject.name,
                    "description": subject.description
                }
            return {"message": "Subject not found"}, 404
        subjects = Subject.query.all()
        return [
            {"id": s.id, "name": s.name, "description": s.description}
            for s in subjects
        ], 200

    @roles_required('admin')
    def post(self):
        args = parser.parse_args()
        subject = Subject(name=args['name'], description=args['description'])
        db.session.add(subject)
        db.session.commit()
        return {"message": "Subject created", "id": subject.id}, 201

    @roles_required('admin')
    def put(self, subject_id):
        args = parser.parse_args()
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404
        subject.name = args['name']
        subject.description = args['description']
        db.session.commit()
        return {"message": "Subject updated"}, 200

    @roles_required('admin')
    def delete(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404
        db.session.delete(subject)
        db.session.commit()
        return {"message": "Subject deleted"}, 200

# --- Chapter Resource ---
class ChapterApi(Resource):
    @roles_required('user', 'admin')
    def get(self, chapter_id=None):
        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if chapter:
                return {
                    "id": chapter.id,
                    "name": chapter.name,
                    "description": chapter.description,
                    "subject_id": chapter.subject_id
                }
            return {"message": "Chapter not found"}, 404
        chapters = Chapter.query.all()
        return [
            {"id": c.id, "name": c.name, "description": c.description, "subject_id": c.subject_id}
            for c in chapters
        ], 200

    @roles_required('admin')
    def post(self):
        args = parser.parse_args()
        chapter = Chapter(
            name=args['name'],
            description=args['description'],
            subject_id=args['subject_id']
        )
        db.session.add(chapter)
        db.session.commit()
        return {"message": "Chapter created", "id": chapter.id}, 200

    @roles_required('admin')
    def put(self, chapter_id):
        args = parser.parse_args()
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404
        # Only update name if provided
        if args.get('name') is not None:
            chapter.name = args['name']
        # Only update description if provided and not blank
        if args.get('description') is not None:
            chapter.description = args['description']
        # Only update subject_id if provided
        if args['subject_id'] is not None:
            chapter.subject_id = args['subject_id']
        # Optionally update questions_count if your model supports it
        if hasattr(chapter, 'questions_count') and args.get('questions_count') is not None:
            chapter.questions_count = args['questions_count']
        db.session.commit()
        return {"message": "Chapter updated"}, 200

    @roles_required('admin')
    def delete(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404
        db.session.delete(chapter)
        db.session.commit()
        return {"message": "Chapter deleted"}, 200

# --- Quiz Resource ---
class QuizApi(Resource):
    @roles_required('user', 'admin')
    def get(self, quiz_id=None):
        if quiz_id:
            quiz = Quiz.query.get(quiz_id)
            if quiz:
                return {
                    "id": quiz.id,
                    "chapter_id": quiz.chapter_id,
                    "name": quiz.name,
                    "date_of_quiz": quiz.date_of_quiz.isoformat() if quiz.date_of_quiz else None,
                    "time_duration": quiz.time_duration,
                    "remarks": quiz.remarks
                }
            return {"message": "Quiz not found"}, 404
        quizzes = Quiz.query.all()
        result = []
        for q in quizzes:
            chapter = Chapter.query.get(q.chapter_id) if q.chapter_id else None
            subject = Subject.query.get(chapter.subject_id) if chapter and chapter.subject_id else None
            question_count = len(q.questions) if hasattr(q, 'questions') and q.questions else 0
            # Defensive: ensure all required fields are present and not None
            result.append({
                "id": q.id,
                "chapter_id": q.chapter_id,
                "name": q.name or "",
                "date_of_quiz": q.date_of_quiz.isoformat() if q.date_of_quiz else "",
                "time_duration": q.time_duration or "",
                "remarks": q.remarks or "",
                "questions_count": question_count,
                "subject_id": chapter.subject_id if chapter else None,
                "subject_name": subject.name if subject else "",
                "chapter_name": chapter.name if chapter else ""
            })
        return result, 200

    @roles_required('admin')
    def post(self):
        args = parser.parse_args()
        # get subject_id from chapter_id
        chapter = Chapter.query.get(args['chapter_id'])
        subject_id = chapter.subject_id
        quiz = Quiz(
            chapter_id=args['chapter_id'],
            subject_id=subject_id ,
            name=args['name'],  # <-- set name
            date_of_quiz=datetime.strptime(args['date_of_quiz'], '%Y-%m-%d') if args['date_of_quiz'] else None,
            time_duration=args['time_duration'],
            remarks=args['remarks']
        )
        db.session.add(quiz)
        db.session.commit()
        return {"message": "Quiz created", "id": quiz.id}, 201

    @roles_required('admin')
    def put(self, quiz_id):
        args = parser.parse_args()
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
        quiz.chapter_id = args['chapter_id']
        quiz.name = args['name']  # <-- update name
        quiz.date_of_quiz = datetime.strptime(args['date_of_quiz'], '%Y-%m-%d') if args['date_of_quiz'] else None
        quiz.time_duration = args['time_duration']
        quiz.remarks = args['remarks']
        db.session.commit()
        return {"message": "Quiz updated"}, 200

    @roles_required('admin')
    def delete(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
        db.session.delete(quiz)
        db.session.commit()
        return {"message": "Quiz deleted"}, 200

# --- Question Resource ---
class QuestionApi(Resource):
    @roles_required('user', 'admin')
    def get(self, question_id=None):
        if question_id:
            question = Question.query.get(question_id)
            if question:
                return {
                    "id": question.id,
                    "quiz_id": question.quiz_id,
                    "question_statement": question.question_statement,
                    "option1": question.option1,
                    "option2": question.option2,
                    "option3": question.option3,
                    "option4": question.option4,
                    "correct_option": question.correct_option
                }
            return {"message": "Question not found"}, 404
        questions = Question.query.all()
        return [
            {
                "id": q.id,
                "quiz_id": q.quiz_id,
                "question_statement": q.question_statement,
                "option1": q.option1,
                "option2": q.option2,
                "option3": q.option3,
                "option4": q.option4,
                "correct_option": q.correct_option
            }
            for q in questions
        ], 200

    @roles_required('admin')
    def post(self):
        args = parser.parse_args()
        question = Question(
            quiz_id=args['quiz_id'],
            question_statement=args['question_statement'],
            option1=args['option1'],
            option2=args['option2'],
            option3=args['option3'],
            option4=args['option4'],
            correct_option=args['correct_option'],
            marks=args['marks'] if args['marks'] is not None else 1,
            question_type=args['question_type'] if args['question_type'] else "mcq"
        )
        db.session.add(question)
        db.session.commit()
        return {"message": "Question created", "id": question.id}, 201

    @roles_required('admin')
    def put(self, question_id):
        args = parser.parse_args()
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404
        question.quiz_id = args['quiz_id']
        question.question_statement = args['question_statement']
        question.option1 = args['option1']
        question.option2 = args['option2']
        question.option3 = args['option3']
        question.option4 = args['option4']
        question.correct_option = args['correct_option']
        question.marks = args['marks'] if args['marks'] is not None else question.marks
        question.question_type = args['question_type'] if args['question_type'] else question.question_type
        db.session.commit()
        return {"message": "Question updated"}, 200

    @roles_required('admin')
    def delete(self, question_id):
        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404
        db.session.delete(question)
        db.session.commit()
        return {"message": "Question deleted"}, 200

# --- Score (Quiz Attempt) Resource ---
class ScoreApi(Resource):
    @roles_required('user', 'admin')
    def get(self, score_id=None):
        if score_id:
            score = Score.query.get(score_id)
            if score:
                quiz_name = score.quiz.name if score.quiz else ""
                # Prepare answer review
                answer_review = []
                if score.user_answers:
                    answers = json.loads(score.user_answers)
                    for q in score.quiz.questions:
                        qid = str(q.id)
                        marked = answers.get(qid)
                        answer_review.append({
                            "question_id": q.id,
                            "question_statement": q.question_statement,
                            "marked_option": marked,
                            "correct_option": q.correct_option,
                            "is_correct": int(marked) == q.correct_option if marked is not None else False
                        })
                return {
                    "id": score.id,
                    "quiz_id": score.quiz_id,
                    "quiz_name": quiz_name,
                    "user_id": score.user_id,
                    "time_stamp_of_attempt": score.time_stamp_of_attempt.isoformat() if score.time_stamp_of_attempt else None,
                    "total_scored": score.total_scored,
                    "answers_review": answer_review
                }
            return {"message": "Score not found"}, 404
        # Only show current user's scores unless admin
        if "admin" == current_user.role:
            scores = Score.query.all()
        else:
            scores = Score.query.filter_by(user_id=current_user.id).all()
        result = []
        for s in scores:
            answer_review = []
            quiz_name = s.quiz.name if s.quiz else ""
            if s.user_answers:
                answers = json.loads(s.user_answers)
                for q in s.quiz.questions:
                    qid = str(q.id)
                    marked = answers.get(qid)
                    iscorrect = False
                    if q.question_type == "mcq":
                        iscorrect = int(marked) == q.correct_option if marked is not None else False
                    else:
                        iscorrect = str(marked).strip().lower() == str(q.correct_option).strip().lower()
                    answer_review.append({
                        "question_id": q.id,
                        "question_statement": q.question_statement,
                        "marked_option": marked,
                        "correct_option": q.correct_option,
                        "is_correct": iscorrect
                    })
            result.append({
                "id": s.id,
                "quiz_id": s.quiz_id,
                "quiz_name": quiz_name,
                "user_id": s.user_id,
                "time_stamp_of_attempt": s.time_stamp_of_attempt.isoformat() if s.time_stamp_of_attempt else None,
                "total_scored": s.total_scored,
                "answers_review": answer_review
            })
        return result, 200

# --- Quiz Attempt Endpoint ---
class QuizAttemptApi(Resource):
    @roles_required('user')
    def post(self, quiz_id):
        args = parser.parse_args()
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
        questions = quiz.questions
        answers = args.get('answers') or request.json.get('answers')
        if not answers:
            return {"message": "Answers required"}, 400
        
        # Calculate score
        score = 0
        for q in questions:
            qid = str(q.id)
            user_ans = answers.get(qid)
            if q.question_type == "mcq":
                if user_ans is not None and str(user_ans).strip() == str(q.correct_option).strip():
                    score += q.marks
            elif q.question_type == "text":
                if user_ans is not None and str(user_ans).strip().lower() == str(q.correct_option).strip().lower():
                    score += q.marks
        
        # Create Score record
        score_obj = Score(
            quiz_id=quiz_id,
            user_id=current_user.id,
            total_scored=score,
            time_stamp_of_attempt=ist_now(),
            user_answers=json.dumps(answers)  # Store user responses as JSON
        )
        db.session.add(score_obj)
        db.session.commit()
        return {"message": "Quiz submitted", "score": score, "score_id": score_obj.id}, 200

# --- Subject Quizzes Resource ---
class SubjectQuizzesApi(Resource):
    @roles_required('user', 'admin')
    def get(self, subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404
        quizzes = []
        for chapter in subject.chapters:
            for quiz in chapter.quizzes:
                quizzes.append({
                    "id": quiz.id,
                    "chapter_id": quiz.chapter_id,
                    "chapter_name": chapter.name,
                    "date_of_quiz": quiz.date_of_quiz.isoformat() if quiz.date_of_quiz else None,
                    "time_duration": quiz.time_duration,
                    "remarks": quiz.remarks
                })
        return quizzes, 200

# --- Active and Expired Quizzes Resource ---
class ActiveQuizzesApi(Resource):
    @roles_required('user', 'admin')
    def get(self):
        today = date.today()
        quizzes = Quiz.query.filter(Quiz.date_of_quiz >= today).all()
        return [
            {
                "id": q.id,
                "chapter_id": q.chapter_id,
                "date_of_quiz": q.date_of_quiz.isoformat() if q.date_of_quiz else None,
                "time_duration": q.time_duration,
                "remarks": q.remarks
            }
            for q in quizzes
        ], 200

class ExpiredQuizzesApi(Resource):
    @roles_required('user', 'admin')
    def get(self):
        today = date.today()
        quizzes = Quiz.query.filter(Quiz.date_of_quiz < today).all()
        return [
            {
                "id": q.id,
                "chapter_id": q.chapter_id,
                "date_of_quiz": q.date_of_quiz.isoformat() if q.date_of_quiz else None,
                "time_duration": q.time_duration,
                "remarks": q.remarks
            }
            for q in quizzes
        ], 200

# --- Quiz Detail Resource ---
class QuizDetailApi(Resource):
    @roles_required('user', 'admin')
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
        chapter = Chapter.query.get(quiz.chapter_id)
        subject = Subject.query.get(chapter.subject_id) if chapter else None
        questions = [
            {
                "id": q.id,
                "question_statement": q.question_statement,
                "question_type": q.question_type,
                "option1": q.option1,
                "option2": q.option2,
                "option3": q.option3,
                "option4": q.option4,
                "correct_option": q.correct_option,
                "marks": q.marks
            }
            for q in quiz.questions
        ]
        return {
            "id": quiz.id,
            "name": quiz.name,
            "date_of_quiz": quiz.date_of_quiz.isoformat() if quiz.date_of_quiz else None,
            "time_duration": quiz.time_duration,
            "remarks": quiz.remarks,
            "chapter_id": quiz.chapter_id,
            "chapter_name": chapter.name if chapter else "",
            "subject_id": chapter.subject_id if chapter else None,
            "subject_name": subject.name if subject else "",
            "questions": questions
        }, 200

# --- Sample Data Resource ---
class SampleDataApi(Resource):
    def get(self):
        try:
            from .models import seed_sample_data, db
            seed_sample_data(db)
            return {"message": "Sample data seeded successfully"}, 200
        except Exception as e:
            return {"message": f"Error seeding sample data: {str(e)}"}, 500

# --- User Management Resource ---
class UserApi(Resource):
    @roles_required('admin')
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {
                    "id": user.id,
                    "username": user.full_name,
                    "email": user.email,
                    "role": user.role
                }
            return {"message": "User not found"}, 404
        users = User.query.all()
        return [
            {"id": u.id, "username": u.full_name, "email": u.email, "role": u.role}
            for u in users
        ], 200

    @roles_required('admin')
    def post(self):
        args = parser.parse_args()
        user = User(
            username=args['username'],
            email=args['email'],
            password=args['password'],  # Ensure this is hashed in the model
            role=args['role']
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created", "id": user.id}, 201

    @roles_required('admin')
    def put(self, user_id):
        args = parser.parse_args()
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.username = args['username']
        user.email = args['email']
        user.role = args['role']
        # Password update should be handled separately with validation
        if args.get('password'):
            user.password = args['password']  # Ensure this is hashed in the model
        db.session.commit()
        return {"message": "User updated"}, 200

    @roles_required('admin')
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 200

# --- User Profile Resource ---
class UserProfileApi(Resource):
    @jwt_required()
    def get(self):
        user = current_user
        if not user:
            return {"message": "User not found"}, 404
        return {
            "id": user.id,
            "full_name": user.full_name or user.username or "",
            "email": user.email or "",
            "username": user.username or "",
            "qualification": user.qualification or "",
            "dob": user.dob.isoformat() if user.dob else "",
            "created_at": user.created_at.isoformat() if user.created_at else ""
        }, 200

    @jwt_required()
    def put(self):
        user = current_user
        if not user:
            return {"message": "User not found"}, 404
        data = request.get_json() or {}
        user.full_name = data.get("full_name", user.full_name)
        user.email = data.get("email", user.email)
        user.username = data.get("username", user.username)
        user.qualification = data.get("qualification", user.qualification)
        dob = data.get("dob")
        if dob:
            try:
                # Accept both "YYYY-MM-DD" and "YYYY-MM-DDTHH:MM:SS" formats
                if "T" in dob:
                    user.dob = datetime.fromisoformat(dob).date()
                else:
                    user.dob = datetime.strptime(dob, "%Y-%m-%d").date()
            except Exception:
                pass  # Ignore invalid date
        db.session.commit()
        return {"message": "Profile updated successfully"}, 200

# --- Resource Registration ---
api.add_resource(SubjectApi, '/api/subjects', '/api/subjects/<int:subject_id>')
api.add_resource(ChapterApi, '/api/chapters', '/api/chapters/<int:chapter_id>')
api.add_resource(QuizApi, '/api/quizzes', '/api/quizzes/<int:quiz_id>')
api.add_resource(QuestionApi, '/api/questions', '/api/questions/<int:question_id>')
api.add_resource(ScoreApi, '/api/scores', '/api/scores/<int:score_id>')
api.add_resource(QuizAttemptApi, '/api/quizzes/<int:quiz_id>/attempt')
api.add_resource(SubjectQuizzesApi, '/api/subjects/<int:subject_id>/quizzes')
api.add_resource(ActiveQuizzesApi, '/api/quizzes/active')
api.add_resource(ExpiredQuizzesApi, '/api/quizzes/expired')
api.add_resource(QuizDetailApi, '/api/quizzes/<int:quiz_id>/details')
api.add_resource(SampleDataApi, '/api/sampledata')
api.add_resource(UserApi, '/api/users', '/api/users/<int:user_id>')
api.add_resource(UserProfileApi, '/api/profile')

# Other useful admin routes you may want to add:

# 1. User Management
#   - List all users (GET /api/users)
#   - Create a user (POST /api/users)
#   - Edit a user (PUT /api/users/<id>)
#   - Delete a user (DELETE /api/users/<id>)
#   - Assign roles to users

# 2. Quiz Management
#   - Create quiz (already present)
#   - Edit quiz (already present)
#   - Delete quiz (already present)
#   - List all quizzes (already present)
#   - Assign chapters to quizzes (if needed)

# 3. Question Management
#   - Create question (already present)
#   - Edit question (already present)
#   - Delete question (already present)
#   - List all questions (already present)
#   - Bulk upload questions (POST /api/questions/bulk)

# 4. Chapter Management
#   - Already present (CRUD)

# 5. Subject Management
#   - Already present (CRUD)

# 6. Score/Attempt Management
#   - View all attempts (already present)
#   - Delete attempt (DELETE /api/scores/<id>) (if needed)

# 7. Dashboard/Statistics
#   - Get summary stats (GET /api/admin/stats)
#   - Get quiz/chapter/subject analytics

# 8. Settings/Config
#   - Update site settings (POST/PUT /api/admin/settings)

# 9. Logs/Audit
#   - View logs (GET /api/admin/logs)

# 10. Role Management
#   - Create/edit/delete roles (if you want dynamic roles)

# For each, you would create a Resource class and register it with api.add_resource.

# Example for users:
# api.add_resource(UserApi, '/api/users', '/api/users/<int:user_id>')

# You may also want to add endpoints for file uploads, notifications, etc., depending on your app's needs.
# You may also want to add endpoints for file uploads, notifications, etc., depending on your app's needs.

# --- Quiz Response Resource ---
class QuizResponseApi(Resource):
    @roles_required('user', 'admin')
    def get(self, quiz_id):
        # Get the latest attempt for this user and quiz
        score = Score.query.filter_by(quiz_id=quiz_id, user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).first()
        quiz = Quiz.query.get(quiz_id)
        if not quiz or not score:
            return {"message": "No attempt found"}, 404
        answers = json.loads(score.user_answers) if score.user_answers else {}
        questions = []
        for q in quiz.questions:
            qid = str(q.id)
            marked = answers.get(qid)
            
            if q.question_type == "mcq":
                correct = int(marked) == int(q.correct_option) if marked is not None else False
                question_data = {
                    "id": q.id,
                    "statement": q.question_statement,
                    "question_type": q.question_type,
                    "options": [q.option1, q.option2, q.option3, q.option4],
                    "marked_option": marked,
                    "correct_option": q.correct_option,
                    "is_correct": correct
                }
            else:  # text question
                correct = str(marked).strip().lower() == str(q.correct_option).strip().lower() if marked is not None else False
                question_data = {
                    "id": q.id,
                    "statement": q.question_statement,
                    "question_type": q.question_type,
                    "options": [],  # Empty for text questions
                    "marked_option": marked,
                    "correct_option": q.correct_option,
                    "is_correct": correct
                }
            
            questions.append(question_data)
        return {
            "quiz_id": quiz.id,
            "quiz_title": quiz.name,
            "subject": quiz.subject.name if quiz.subject else "",
            "chapter": quiz.chapter.name if quiz.chapter else "",
            "attempt_date": score.time_stamp_of_attempt.isoformat() if score.time_stamp_of_attempt else "",
            "score": score.total_scored,
            "questions": questions
        }, 200

# --- Quiz Response by Score ID Resource ---
class ScoreResponseApi(Resource):
    @roles_required('user', 'admin')
    def get(self, score_id):
        # Get specific score attempt
        score = Score.query.filter_by(id=score_id, user_id=current_user.id).first()
        if not score:
            return {"message": "Score not found"}, 404
        
        quiz = Quiz.query.get(score.quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
            
        answers = json.loads(score.user_answers) if score.user_answers else {}
        questions = []
        for q in quiz.questions:
            qid = str(q.id)
            marked = answers.get(qid)
            correct = int(marked) == int(q.correct_option) if marked is not None else False
            questions.append({
                "id": q.id,
                "statement": q.question_statement,
                "options": [q.option1, q.option2, q.option3, q.option4],
                "marked_option": marked,
                "correct_option": q.correct_option,
                "is_correct": correct
            })
        return {
            "quiz_id": quiz.id,
            "quiz_title": quiz.name,
            "subject": quiz.subject.name if quiz.subject else "",
            "chapter": quiz.chapter.name if quiz.chapter else "",
            "attempt_date": score.time_stamp_of_attempt.isoformat() if score.time_stamp_of_attempt else "",
            "score": score.total_scored,
            "questions": questions
        }, 200

api.add_resource(QuizResponseApi, '/api/response/<int:quiz_id>')
api.add_resource(ScoreResponseApi, '/api/score/<int:score_id>/response')
