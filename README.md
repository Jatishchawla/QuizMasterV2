# QuizMasterV2

Problem Statement 
Design and implement a full-stack web applica on for online quiz management. The system should allow admins to 
create/manage subjects, chapters, quizzes, ques ons, and users. Users can a empt quizzes, view their results, and track their 
analy cs. 
Approach to the Problem Statement 
 Frameworks and Libraries Used: 
o Backend: 
 Python 3.x 
 Flask 
 Flask-RESTful 
 Flask-JWT-Extended 
 Flask-CORS 
 SQLAlchemy (ORM) 
 SQLite (Database) 
 werkzeug.security (for password hashing) 
o Frontend: 
 Vue.js 3 
 Vue Router 
 Axios 
 Chart.js (for analy cs and charts) 
 Bootstrap 5 (for UI components) 
 HTML, CSS & JS 
o Redis – Cachin and Celery task que backend 
o Celery – Asynchronous task processing 
 Approach:  
o Used a modular approach with a clear separa on of backend (Flask) and frontend (Vue.js). 
o Designed the database schema to support subjects, chapters, quizzes, ques ons, users, and scores. 
o Implemented RESTful APIs for all CRUD opera ons and quiz a empts. 
o Used JWT authen ca on for secure access and role-based authoriza on. 
o Built a responsive frontend with Vue.js, suppor ng admin and user dashboards, analy cs, and quiz interfaces. 
o Added analy cs and repor ng features for both admins and users. 
 Admin Capabili es in the Applica on: 
o Subject Management 
1. Add, update, or delete subjects. 
o User Management 
1. Manage customer and professional accounts and can view, edit and delete profiles. 
2. Block or unblock users based on ra ngs, reports or feedback. 
o Analy cs Dashboard 
1. Access dynamic charts showing sta s cs. 
2. Can view total Quizzes, Subjects, Chapters etc. 
o System Maintenance 
1. Ensure pla orm integrity by overseeing key database entries and opera onal data. 
 Designing the Database: 
ER Diagram: 
 Key Features 
1. Admin dashboard: for managing subjects, chapters, quizzes, ques ons, and users 
2. User dashboard with available quizzes, recent ac vity, and performance stats 
3. Quiz: crea on and management (CRUD) for admins 
4. Ques on: crea on and management (MCQ and text type) 
5. Quiz a empt func onality for users with automa c scoring. 
6. User Authen ca on: Implemented JWT token for authoriza on. Used hashing to store passwords. Secure 
login/registra on for all users. 
7. RBAC: Implemented Role Based Access Control  
8. Dynamic Charts: Detailed analy cs for both admins (site-wide) and users (personal progress) 
9. Responsive frontend with modern UI (Bootstrap 5, Chart.js) 
10. Search:  
 Admin: can search users/subjects/quizzes 
 User: can search subjects/quizzes by date/scores. 
 API Resource Endpoint: 
o /api/subjects [GET, POST], /api/subjects/<id> [GET, PUT, DELETE] 
o /api/chapters [GET, POST], /api/chapters/<id> [GET, PUT, DELETE] 
o /api/quizzes [GET, POST], /api/quizzes/<id> [GET, PUT, DELETE] 
o /api/ques ons [GET, POST], /api/ques ons/<id> [GET, PUT, DELETE] 
o /api/scores [GET], /api/scores/<id> [GET] 
o /api/quizzes/<quiz_id>/a empt [POST] 
o /api/subjects/<subject_id>/quizzes [GET] 
o /api/quizzes/ac ve [GET] 
o /api/quizzes/expired [GET] 
o /api/quizzes/<quiz_id>/details [GET] 
o /api/users [GET, POST], /api/users/<id> [GET, PUT, DELETE] 
o /api/profile [GET, PUT] 
o /api/login [POST] 
DRIVE LINK OF THE PRESENTATION VIDEO: 
