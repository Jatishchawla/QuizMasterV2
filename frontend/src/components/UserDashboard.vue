<template>
  <div class="user-dashboard">
    <div class="py-4 container-fluid">
      <!-- Welcome Section -->
      <div class="mb-4 row">
        <div class="col-12">
          <div class="bg-gradient-primary border-0 text-white welcome-card card">
            <div class="p-4 card-body">
              <div class="align-items-center row">
                <div class="col-md-8">
                  <h2 class="mb-2 fw-bold">Welcome back, {{ user.username }}! 👋</h2>
                  <p class="opacity-75 mb-3">Ready to continue your learning journey? You have {{ availableQuizzes.length }} new quizzes available.</p>
                  <button class="btn btn-light btn-lg" @click="goToQuiz">
                    <i class="me-2 fas fa-play"></i>
                    Start Learning
                  </button>
                </div>
                <div class="text-center col-md-4">
                  <div class="welcome-stats">
                    <div class="stat-item">
                      <h3 class="fw-bold">{{ stats.totalQuizzesAttempted }}</h3>
                      <small>Quizzes Completed</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      

      <!-- Search and Filters -->
      <div class="mb-4 row">
        <div class="col-lg-8">
          <div class="d-flex align-items-center gap-2">
            <input
              v-model="searchQuery"
              class="form-control form-control-sm"
              placeholder="Search by quiz name, subject, or chapter"
              style="max-width: 320px;"
            />
            <select class="form-select-sm form-select" v-model="selectedSubject">
              <option value="">All Subjects</option>
              <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                {{ subject.name }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- Available Quizzes -->
        <div class="mb-4 col-lg-8">
          <div class="border-0 card">
            <div class="bg-white pb-0 border-0 card-header">
              <div class="d-flex align-items-center justify-content-between">
                <h5 class="mb-0 fw-bold">Available Quizzes</h5>
                <!-- Removed duplicate filter select -->
              </div>
            </div>
            <div class="card-body">
              <div class="quiz-grid">
                <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="mb-3 border quiz-item card">
                  <div class="card-body">
                    <div class="d-flex align-items-start justify-content-between mb-3">
                      <div class="quiz-info">
                        <h6 class="mb-1 fw-bold">{{ quiz.name }}</h6>
                        <p class="mb-2 text-muted small">{{ quiz.subjectName }} • {{ quiz.chapterName }}</p>
                        <div class="quiz-meta">
                          <span class="bg-light me-2 text-dark badge">
                            <i class="me-1 fas fa-question-circle"></i>
                            {{ quiz.questionCount }} Questions
                          </span>
                          <span class="bg-light me-2 text-dark badge">
                            <i class="me-1 fas fa-clock"></i>
                            {{ quiz.time_duration }} mins
                          </span>
                          <span class="badge" :class="getDifficultyClass(quiz.difficulty)">
                            {{ quiz.difficulty }}
                          </span>
                        </div>
                      </div>
                      <div class="quiz-actions">
                        <button class="btn btn-primary btn-sm" @click="startQuiz(quiz.id)">
                          <i class="me-1 fas fa-play"></i>
                          Start
                        </button>
                      </div>
                    </div>
                    <div class="progress" style="height: 4px;">
                      <div class="progress-bar" :style="`width: ${quiz.completionRate}%`"></div>
                    </div>
                    <small class="text-muted">{{ quiz.completionRate }}% of students completed</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
          <!-- Recent Activity -->
          <div class="mb-4 border-0 card">
            <div class="bg-white pb-0 border-0 card-header">
              <h6 class="mb-0 fw-bold">Recent Activity</h6>
            </div>
            <div class="card-body">
              <div class="activity-list">
                <div v-for="activity in recentActivity" :key="activity.id" class="d-flex align-items-center mb-3 activity-item">
                  <div class="me-3 activity-icon">
                    <i :class="activity.icon" :style="`color: ${activity.color}`"></i>
                  </div>
                  <div class="flex-grow-1 activity-content">
                    <p class="mb-1 small">{{ activity.description }}</p>
                    <small class="text-muted">{{ activity.time }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="border-0 card">
            <div class="bg-white pb-0 border-0 card-header">
              <h6 class="mb-0 fw-bold">Quick Actions</h6>
            </div>
            <div class="card-body">
              <div class="gap-2 d-grid">
                <button class="btn-outline-primary btn" @click="exportResults">
                  <i class="me-2 fas fa-download"></i>
                  Export Results
                </button>
                <button class="btn-outline-success btn" @click="viewAnalytics">
                  <i class="me-2 fas fa-chart-bar"></i>
                  View Analytics
                </button>
                <button class="btn-outline-info btn" @click="viewQuizHistory">
                  <i class="me-2 fas fa-history"></i>
                  Quiz History
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'UserDashboard',
  data() {
    return {
      searchQuery: '',
      selectedSubject: '',
      user: {},
      stats: {
        totalQuizzesAttempted: 0,
        averageScore: 0,
        totalTime: '0h',
        streak: 0,
        rank: '#--'
      },
      subjects: [],
      chapters: [],
      availableQuizzes: [],
      recentActivity: [],
      token: localStorage.getItem("token") || ""
    }
  },
  computed: {
    filteredQuizzes() {
      let quizzes = this.availableQuizzes;
      // Filter by subject if selected
      if (this.selectedSubject) {
        quizzes = quizzes.filter(quiz => quiz.subjectId === parseInt(this.selectedSubject));
      }
      // Search by quiz name, subject, or chapter
      if (this.searchQuery && this.searchQuery.trim() !== '') {
        const q = this.searchQuery.trim().toLowerCase();
        quizzes = quizzes.filter(quiz =>
          (quiz.name && quiz.name.toLowerCase().includes(q)) ||
          (quiz.subjectName && quiz.subjectName.toLowerCase().includes(q)) ||
          (quiz.chapterName && quiz.chapterName.toLowerCase().includes(q))
        );
      }
      return quizzes;
    }
  },
  methods: {
    async fetchUserDashboard() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/dashboard", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        console.log("Dashboard data:", res.data);
        this.user = res.data;
        this.stats.totalQuizzesAttempted = res.data.total_quizzes_attempted || 0;
        this.stats.averageScore = res.data.average_score || 0;
        this.stats.totalTime = res.data.total_time || '0h';
        this.stats.streak = res.data.streak || 0;
        this.stats.rank = res.data.rank || '#--';
        this.subjects = res.data.subjects || [];
      } catch (err) {
        console.log("Dashboard error:", err);
        this.user = { full_name: "User" };
        this.subjects = [];
      }
    },
    async fetchChapters() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/chapters", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        console.log("Chapters data:", res.data);
        this.chapters = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        console.log("Chapters error:", err);
        this.chapters = [];
      }
    },
    async fetchQuizzes() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/quizzes", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        const quizzes = Array.isArray(res.data) ? res.data : [];
        const chapters = Array.isArray(this.chapters) ? this.chapters : [];
        const subjects = Array.isArray(this.subjects) ? this.subjects : [];
        console.log("Quizzes data:", quizzes);
        console.log("Chapters for quizzes:", chapters);
        console.log("Subjects for quizzes:", subjects);
        this.availableQuizzes = quizzes.map(q => {
          // Defensive: fallback to quiz.subject_id if chapter is missing
          let chapter = chapters.find(c => c.id === q.chapter_id);
          let subject = chapter
            ? subjects.find(s => s.id === chapter.subject_id)
            : subjects.find(s => s.id === q.subject_id);
          return {
            id: q.id,
            name: q.name || "Untitled Quiz",
            subjectId: chapter ? chapter.subject_id : q.subject_id || null,
            subjectName: subject ? subject.name : '',
            chapterName: chapter ? chapter.name : '',
            questionCount: q.questions_count || 0,
            time_duration: q.time_duration || '',
            difficulty: this.getDifficulty(q),
            completionRate: q.completion_rate || 0
          };
        });
        console.log("Available quizzes for dashboard:", this.availableQuizzes);
      } catch (err) {
        console.log("Quizzes error:", err);
        this.availableQuizzes = [];
      }
    },
    async fetchRecentActivity() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/scores", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        console.log("Scores data:", res.data);
        this.recentActivity = (res.data || []).slice(0, 4).map(score => ({
          id: score.id,
          description: `Completed "${this.getQuizName(score.quiz_id)}" with ${score.total_scored} score`,
          time: score.time_stamp_of_attempt ? new Date(score.time_stamp_of_attempt).toLocaleString() : '',
          icon: score.total_scored > 0 ? 'fas fa-check-circle' : 'fas fa-times-circle',
          color: score.total_scored > 0 ? '#10b981' : '#ef4444'
        }));
        console.log("Recent activity for dashboard:", this.recentActivity);
      } catch (err) {
        console.log("Scores error:", err);
        this.recentActivity = [];
      }
    },
    getQuizName(quizId) {
      const quiz = this.availableQuizzes.find(q => q.id === quizId);
      return quiz ? quiz.name : "Quiz";
    },
    getDifficulty(quiz) {
      if (quiz.time_duration && parseInt(quiz.time_duration) <= 20) return "Easy";
      if (quiz.time_duration && parseInt(quiz.time_duration) <= 35) return "Medium";
      return "Hard";
    },
    getDifficultyClass(difficulty) {
      switch (difficulty.toLowerCase()) {
        case 'easy': return 'bg-success';
        case 'medium': return 'bg-warning';
        case 'hard': return 'bg-danger';
        default: return 'bg-secondary';
      }
    },
    startQuiz(quizId) {
      this.$router.push(`/user/quiz/${quizId}`);
    },
    goToQuiz() {
      if (this.availableQuizzes.length > 0) {
        this.startQuiz(this.availableQuizzes[0].id);
      }
    },
    exportResults() {
      axios.get("http://127.0.0.1:5000/api/export/csv", {
        headers: { Authorization: `Bearer ${this.token}` }
      }).then(() => {
        alert("Export started! You will be notified when ready.");
      });
    },
    viewAnalytics() {
      this.$router.push("/user/analytics");
    },
    viewQuizHistory() {
      this.$router.push("/user/results");
    }
  },
  async mounted() {
    await this.fetchUserDashboard();
    await this.fetchChapters();
    await this.fetchQuizzes();
    await this.fetchRecentActivity();
    this.initPerformanceChart();
    console.log("UserDashboard mounted, state:", {
      user: this.user,
      stats: this.stats,
      subjects: this.subjects,
      chapters: this.chapters,
      availableQuizzes: this.availableQuizzes,
      recentActivity: this.recentActivity
    });
  }
};
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
}

.welcome-card {
  border-radius: 1rem;
  overflow: hidden;
}

.stats-card {
  transition: all 0.3s ease;
  border-radius: 1rem;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.quiz-item {
  transition: all 0.3s ease;
  border-radius: 0.75rem;
}

.quiz-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.activity-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 50%;
}

.quiz-filters .form-select {
  min-width: 150px;
}

@media (max-width: 768px) {
  .welcome-card .row {
    text-align: center;
  }
  
  .stats-card {
    margin-bottom: 1rem;
  }
  
  .quiz-item .d-flex {
    flex-direction: column;
    align-items: start !important;
  }
  
  .quiz-actions {
    margin-top: 1rem;
    width: 100%;
  }
  
  .quiz-actions .btn {
    width: 100%;
  }
}
</style>


<!-- 
1. Do we have data to show study time, day streak, global rank, etc.?
- These fields (study time, day streak, global rank) are shown on the dashboard, but your backend must provide them in the /api/dashboard response.
- If your backend does not calculate or return these fields, they will be empty or default values on the frontend.
- You should ensure your backend /api/dashboard endpoint returns:
  - total_time (study time)
  - streak (day streak)
  - rank (global rank)
  - total_quizzes_attempted
  - average_score

2. How are you calculating average score?
- The frontend expects averageScore from /api/dashboard.
- Typically, average score is calculated in the backend as:
    average_score = (sum of all user's quiz scores) / (number of quizzes attempted)
- If you want to show percentage, multiply by 100 or ensure your backend returns it as a percentage.

If you want to implement these calculations in the backend, you should aggregate the user's quiz attempts (from the Score table), sum the scores, and divide by the number of attempts. For streak and study time, you need to track quiz attempt timestamps and durations.

Example backend logic for average score:
```python
# ...inside your dashboard endpoint...
scores = Score.query.filter_by(user_id=current_user.id).all()
total_score = sum(s.total_scored for s in scores)
quiz_count = len(scores)
average_score = (total_score / quiz_count) if quiz_count > 0 else 0 -->
