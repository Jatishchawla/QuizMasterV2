## User Based Routes
- GET    /api/home                - user dashboard (requires user or admin role)
- GET    /api/admin               - admin dashboard (requires admin role)
- POST   /api/register            - user registration
- POST   /api/login               - user login
- POST   /api/logout              - user logout
- GET/PUT /api/profile            - view or update user profile

## Subject Based API
- GET    /api/subjects                            - get all subjects
- POST   /api/subjects                            - create a new subject (admin only)
- GET    /api/subjects/<subject_id>               - get details of a subject
- PUT    /api/subjects/<subject_id>               - update a subject (admin only)
- DELETE /api/subjects/<subject_id>               - delete a subject (admin only)
- GET    /api/subjects/<subject_id>/chapters      - get all chapters under a subject

## Chapter Based API
- GET    /api/chapters                            - get all chapters
- POST   /api/chapters                            - create a new chapter (admin only)
- GET    /api/chapters/<chapter_id>               - get details of a chapter
- PUT    /api/chapters/<chapter_id>               - update a chapter (admin only)
- DELETE /api/chapters/<chapter_id>               - delete a chapter (admin only)

## Quiz Based API
- GET    /api/quizzes                             - get all quizzes
- POST   /api/quizzes                             - create a new quiz (admin only)
- GET    /api/quizzes/<quiz_id>                   - get details of a quiz
- PUT    /api/quizzes/<quiz_id>                   - update a quiz (admin only)
- DELETE /api/quizzes/<quiz_id>                   - delete a quiz (admin only)
- GET    /api/quizzes/<quiz_id>/questions         - get all questions under a quiz

## Question Based API
- GET    /api/questions                           - get all questions
- POST   /api/questions                           - create a new question (admin only)
- GET    /api/questions/<question_id>             - get details of a question
- PUT    /api/questions/<question_id>             - update a question (admin only)
- DELETE /api/questions/<question_id>             - delete a question (admin only)

## Quiz Attempt & Score API
- POST   /api/quizzes/<quiz_id>/attempt           - attempt a quiz (user)
- GET    /api/scores                              - get all quiz attempts/scores for current user (admin gets all)
- GET    /api/scores/<score_id>                   - get details of a quiz attempt/score

## Admin Based Routes
- GET    /api/admin/users                         - get all users (admin only)
- GET    /api/admin/scores                        - get all scores/attempts (admin only)

## Export & Batch Jobs
- GET    /api/export/csv                          - export user quiz history as CSV (user triggers async job)
- POST   /api/admin/send-reminders                - trigger daily reminders (admin only, for testing)
- POST   /api/admin/send-monthly-report           - trigger monthly report (admin only, for testing)

---

## Example Usage

### Register a new user
```
POST /api/register
{
  "username": "john",
  "password": "password123",
  "email": "john@example.com"
}
```

### Attempt a quiz
```
POST /api/quizzes/5/attempt
Headers: { Authorization: Bearer <token> }
{
  "answers": {
    "1": 2,
    "2": 4,
    ...
  }
}
```

### Get all scores for a user
```
GET /api/scores
Headers: { Authorization: Bearer <token> }
```

### Export user quiz history as CSV
```
GET /api/export/csv
Headers: { Authorization: Bearer <token> }
```

### Trigger daily reminders (admin only)
```
POST /api/admin/send-reminders
Headers: { Authorization: Bearer <admin_token> }
```

### Trigger monthly report (admin only)
```
POST /api/admin/send-monthly-report
Headers: { Authorization: Bearer <admin_token> }
```

---

## Notes
- All `/api/admin/*` routes require admin privileges.
- All `/api/*` routes (except `/register` and `/login`) require authentication.
- Replace `<subject_id>`, `<chapter_id>`, `<quiz_id>`, `<question_id>`, `<score_id>` with actual IDs.
- All endpoints return JSON.
- Pagination/filtering can be added as needed for large datasets.
