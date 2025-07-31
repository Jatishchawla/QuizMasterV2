from .database import db, bcrypt, datetime
import json
from datetime import timezone, timedelta

# Define IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def ist_now():
    """Return current time in IST"""
    return datetime.now(IST)

class User(db.Model):  
    __tablename__ = "users"
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(), nullable=False, unique=True)
    password      = db.Column(db.String(), nullable=False)
    username      = db.Column(db.String(), nullable=False)
    full_name     = db.Column(db.String(), nullable=True)
    qualification = db.Column(db.String(), nullable=True)
    dob           = db.Column(db.Date, nullable=True)
    active        = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=ist_now)
    updated_at    = db.Column(db.DateTime, default=ist_now)
    role          = db.Column(db.String(20), nullable=False, default="user")  # "admin" or "user"
    scores        = db.relationship('Score', back_populates='user', lazy=True)

# --- Quiz Master Models ---

class Subject(db.Model):
    __tablename__ = "subjects"
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    chapters    = db.relationship('Chapter', back_populates='subject', cascade="all, delete-orphan", lazy=True)

class Chapter(db.Model):
    __tablename__ = "chapters"
    id          = db.Column(db.Integer, primary_key=True)
    subject_id  = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    name        = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    subject     = db.relationship('Subject', back_populates='chapters')
    quizzes     = db.relationship('Quiz', back_populates='chapter', cascade="all, delete-orphan", lazy=True)

class Quiz(db.Model):
    __tablename__ = "quizzes"
    id            = db.Column(db.Integer, primary_key=True)
    chapter_id    = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    name          = db.Column(db.String(255), nullable=True)  # <-- Quiz title
    date_of_quiz  = db.Column(db.Date)
    time_duration = db.Column(db.String(10))  # e.g. "01:30"
    remarks       = db.Column(db.Text)
    chapter       = db.relationship('Chapter', back_populates='quizzes')
    questions     = db.relationship('Question', back_populates='quiz', cascade="all, delete-orphan", lazy=True)
    scores        = db.relationship('Score', back_populates='quiz', cascade="all, delete-orphan", lazy=True)
    # Add subject_id for direct access
    subject_id    = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)
    subject       = db.relationship('Subject', foreign_keys=[subject_id])

class Question(db.Model):
    __tablename__ = "questions"
    id                  = db.Column(db.Integer, primary_key=True)
    quiz_id             = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement  = db.Column(db.Text, nullable=False)
    option1             = db.Column(db.String(255))
    option2             = db.Column(db.String(255))
    option3             = db.Column(db.String(255))
    option4             = db.Column(db.String(255))
    correct_option      = db.Column(db.String(255), nullable=False)
    marks               = db.Column(db.Integer, nullable=False, default=1)
    question_type       = db.Column(db.String(20), nullable=False, default="mcq")  # "mcq" or "text"
    quiz                = db.relationship('Quiz', back_populates='questions')
    # Add chapter_id and subject_id for direct access
    chapter_id          = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=True)
    subject_id          = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=True)

class Score(db.Model):
    __tablename__ = "scores"
    id                  = db.Column(db.Integer, primary_key=True)
    quiz_id             = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id             = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=ist_now)
    total_scored        = db.Column(db.Integer)
    user_answers        = db.Column(db.Text)  # <-- new field to store answers as JSON
    quiz                = db.relationship('Quiz', back_populates='scores')
    user                = db.relationship('User', back_populates='scores')

def seed_sample_data(db):
    # Create subjects
    math = Subject(name="Mathematics", description="Math subject")
    physics = Subject(name="Physics", description="Physics subject")
    db.session.add_all([math, physics])
    db.session.commit()

    # Create chapters
    algebra = Chapter(name="Algebra", description="Algebra chapter", subject_id=math.id)
    calculus = Chapter(name="Calculus", description="Calculus chapter", subject_id=math.id)
    mechanics = Chapter(name="Mechanics", description="Mechanics chapter", subject_id=physics.id)
    db.session.add_all([algebra, calculus, mechanics])
    db.session.commit()

    # Create quizzes
    quiz1 = Quiz(name="Algebra Basics", chapter_id=algebra.id, date_of_quiz=datetime(2024, 7, 1), time_duration="30", remarks="Basic algebra quiz", subject_id=math.id)
    quiz2 = Quiz(name="Calculus Fundamentals", chapter_id=calculus.id, date_of_quiz=datetime(2024, 7, 2), time_duration="40", remarks="Calculus quiz", subject_id=math.id)
    quiz3 = Quiz(name="Newton's Laws", chapter_id=mechanics.id, date_of_quiz=datetime(2024, 7, 3), time_duration="25", remarks="Mechanics quiz", subject_id=physics.id)
    db.session.add_all([quiz1, quiz2, quiz3])
    db.session.commit()

    # Create questions for quiz1
    q1 = Question(quiz_id=quiz1.id, question_statement="What is 2+2?", option1="3", option2="4", option3="5", option4="6", correct_option="2", marks=1, question_type="mcq", chapter_id=algebra.id, subject_id=math.id)
    q2 = Question(quiz_id=quiz1.id, question_statement="Solve for x: x+3=5", option1="1", option2="2", option3="3", option4="4", correct_option="2", marks=1, question_type="mcq", chapter_id=algebra.id, subject_id=math.id)
    q3 = Question(quiz_id=quiz1.id, question_statement="What is the value of x in x^2=9?", option1="1", option2="3", option3="-3", option4="Both 2 and 3", correct_option="4", marks=1, question_type="mcq", chapter_id=algebra.id, subject_id=math.id)
    db.session.add_all([q1, q2, q3])

    # Create questions for quiz2
    q4 = Question(quiz_id=quiz2.id, question_statement="Derivative of x^2?", option1="2x", option2="x", option3="x^2", option4="None", correct_option="1", marks=1, question_type="mcq", chapter_id=calculus.id, subject_id=math.id)
    q5 = Question(quiz_id=quiz2.id, question_statement="Integral of 2x dx?", option1="x^2 + C", option2="2x + C", option3="x + C", option4="None", correct_option="1", marks=1, question_type="mcq", chapter_id=calculus.id, subject_id=math.id)
    db.session.add_all([q4, q5])

    # Create questions for quiz3
    q6 = Question(quiz_id=quiz3.id, question_statement="Who formulated the laws of motion?", option1="Einstein", option2="Newton", option3="Galileo", option4="Tesla", correct_option="2", marks=1, question_type="mcq", chapter_id=mechanics.id, subject_id=physics.id)
    q7 = Question(quiz_id=quiz3.id, question_statement="State Newton's first law.", option1="Law of inertia", option2="Law of gravity", option3="Law of acceleration", option4="Law of action-reaction", correct_option="1", marks=1, question_type="mcq", chapter_id=mechanics.id, subject_id=physics.id)
    db.session.add_all([q6, q7])

    db.session.commit()