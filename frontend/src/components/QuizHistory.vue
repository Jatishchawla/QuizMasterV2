<template>
  <div class="user-scores-page">
    <div class="py-4 container-fluid">
      <!-- Header -->
      <div class="mb-4 row">
        <div class="col-12">
          <div class="border-0 card">
            <div class="card-body">
              <div class="d-flex align-items-center justify-content-between">
                <h2 class="mb-0 fw-bold">My Quiz Scores</h2>
                <div>
                  <router-link to="/user/dashboard" class="btn-outline-secondary btn btn-sm">
                    <i class="fa-arrow-left me-1 fas"></i>
                    Back to Dashboard
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="mb-4 row">
        <div class="col-lg-8">
          <div class="d-flex gap-2">
            <select class="form-select-sm form-select" v-model="selectedSubject">
              <option value="">All Subjects</option>
              <option v-for="subject in subjects" :key="subject" :value="subject">
                {{ subject }}
              </option>
            </select>
            <select class="form-select-sm form-select" v-model="selectedDifficulty">
              <option value="">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
            <select class="form-select-sm form-select" v-model="sortBy">
              <option value="date-desc">Date: Newest First</option>
              <option value="date-asc">Date: Oldest First</option>
              <option value="score-desc">Score: High to Low</option>
              <option value="score-asc">Score: Low to High</option>
              <option value="name-asc">Quiz Name: A to Z</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Scores Table -->
      <div class="mb-4 row">
        <div class="col-lg-8">
          <div class="border-0 card">
            <div class="card-body">
              <div v-if="filteredScores.length">
                <table class="table table-bordered table-hover">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Quiz Title</th>
                      <th>Subject</th>
                      <th>Chapter</th>
                      <th>Difficulty</th>
                      <th>Score</th>
                      <th>Date</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(score, idx) in paginatedScores" :key="score.id">
                      <td>{{ idx + 1 }}</td>
                      <td>{{ score.quizTitle }}</td>
                      <td>{{ score.subject }}</td>
                      <td>{{ score.chapter }}</td>
                      <td>
                        <span class="badge" :class="getDifficultyClass(score.difficulty)">
                          {{ score.difficulty }}
                        </span>
                      </td>
                      <td>
                        {{ score.score }}
                      </td>
                      <td>
                        {{ formatDate(score.attemptDate) }}
                      </td>
                      <td>
                        <button class="btn-outline-info btn btn-sm" @click="openAttemptModal(score.quizId)">
                          View
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-muted">No quiz scores found.</div>

              <!-- Pagination -->
              <div v-if="totalPages > 1" class="mt-4">
                <nav>
                  <ul class="justify-content-center pagination">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                      <a class="page-link" @click="changePage(currentPage - 1)" tabindex="-1">Previous</a>
                    </li>
                    <li v-for="page in visiblePages" :key="page" class="page-item" :class="{ active: currentPage === page }">
                      <a class="page-link" @click="changePage(page)">{{ page }}</a>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                      <a class="page-link" @click="changePage(currentPage + 1)">Next</a>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary Stats -->
      <div class="mb-4 row">
        <div class="col-lg-8">
          <div class="border-0 card">
            <div class="card-body">
              <h5 class="mb-3 fw-bold">Summary</h5>
              <div class="row">
                <div class="col-md-3">
                  <div class="text-center">
                    <h4 class="fw-bold">{{ totalQuizzes }}</h4>
                    <small class="text-muted">Total Quizzes</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Quiz Details Modal -->
  <div v-if="showAttemptModal" class="modal fade show" style="display:block;" tabindex="-1" aria-labelledby="quizDetailsModalLabel" aria-modal="true" role="dialog">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="bg-primary text-white modal-header">
          <h6 class="modal-title" id="quizDetailsModalLabel">
            <i class="me-2 fas fa-clipboard-list"></i>
            Quiz Attempt Details
          </h6>
          <button type="button" class="btn-close btn-close-white" @click="closeAttemptModal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="attemptDetails">
            <div class="mb-3 quiz-summary-header">
              <div class="row">
                <div class="col-md-8">
                  <h5 class="text-primary fw-bold">{{ attemptDetails.quiz_title }}</h5>
                  <p class="mb-2 text-muted small">
                    <i class="me-1 fas fa-book"></i>{{ attemptDetails.subject }} - {{ attemptDetails.chapter }}
                  </p>
                </div>
                <div class="text-end col-md-4">
                  <div class="score-display">
                    <h4 class="text-success fw-bold">{{ attemptDetails.score }}/{{ getTotalQuestions() }}</h4>
                    <small class="text-muted">Final Score</small>
                  </div>
                </div>
              </div>
            </div>
            <div class="questions-review">
              <h6 class="mb-3 fw-bold">
                <i class="me-2 fa-list-alt fas"></i>
                Questions Review
              </h6>
              <div v-for="(question, idx) in attemptDetails.questions" :key="question.id" class="mb-3 question-card">
                <div :class="['question-header', questionHeaderClass(question)]">
                  <div class="d-flex align-items-center justify-content-between">
                    <small class="mb-0 fw-bold">
                      <span class="question-number">Q{{ idx + 1 }}</span>
                      <span class="badge badge-sm" :class="questionBadgeClass(question)">
                        <i :class="questionBadgeIcon(question)"></i>
                        {{ questionBadgeText(question) }}
                      </span>
                    </small>
                  </div>
                </div>
                <div class="question-body">
                  <div class="mb-2 question-text">
                    <p class="fw-semibold small">{{ question.statement }}</p>
                  </div>
                  
                  <!-- Show options only for MCQ questions -->
                  <div v-if="question.question_type === 'mcq'" class="options-list">
                    <div v-for="(option, optIdx) in question.options" :key="optIdx"
                      :class="getOptionItemClass(question, optIdx)">
                      <div class="option-content">
                        <div :class="getOptionCircleClass(question, optIdx)">
                          <span class="option-letter">{{ String.fromCharCode(65 + optIdx) }}</span>
                          <i v-if="isCorrectOption(question, optIdx)" class="fas fa-check option-icon"></i>
                          <i v-if="isIncorrectSelected(question, optIdx)" class="fas fa-times option-icon"></i>
                        </div>
                        <div class="option-text">
                          {{ option }}
                          <div class="option-badges">
                            <span v-if="isCorrectOption(question, optIdx)" class="bg-success ms-1 badge small">
                              <i class="me-1 fas fa-check"></i>Correct
                            </span>
                            <span v-if="isUserSelected(question, optIdx) && !question.is_correct" class="bg-danger ms-1 badge small">
                              <i class="me-1 fas fa-times"></i>Your Answer
                            </span>
                            <span v-if="isUserSelected(question, optIdx) && question.is_correct" class="bg-success ms-1 badge small">
                              <i class="me-1 fas fa-check"></i>Your Answer
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Show text answer for text questions -->
                  <div v-else class="text-answer-section">
                    <div class="mb-3">
                      <label class="form-label fw-semibold small">Your Answer:</label>
                      <div class="user-text-answer" :class="question.is_correct ? 'correct-answer' : 'incorrect-answer'">
                        {{ question.marked_option || '' }}
                        <span v-if="question.is_correct" class="bg-success ms-2 badge small">
                          <i class="me-1 fas fa-check"></i>Correct
                        </span>
                        <span v-else class="bg-danger ms-2 badge small">
                          <i class="me-1 fas fa-times"></i>Incorrect
                        </span>
                      </div>
                    </div>
                    <div v-if="!question.is_correct">
                      <label class="form-label fw-semibold small">Correct Answer:</label>
                      <div class="correct-text-answer">
                        {{ question.correct_option }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-muted">Loading attempt details...</div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary btn-sm" @click="closeAttemptModal">
            <i class="me-1 fas fa-times"></i>Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'UserScores',
  data() {
    return {
      searchQuery: '',
      selectedSubject: '',
      selectedDifficulty: '',
      selectedTimeRange: '',
      sortBy: 'date-desc',
      currentPage: 1,
      itemsPerPage: 10,
      subjects: [],
      scores: [],
      showAttemptModal: false,
      attemptDetails: null
    }
  },
  computed: {
    totalQuizzes() {
      return this.scores.length
    },
    filteredScores() {
      let filtered = [...this.scores];
      // Subject filter (match by subject name, not id)
      if (this.selectedSubject) {
        filtered = filtered.filter(score => score.subject === this.selectedSubject);
      }
      // Difficulty filter (case-insensitive match)
      if (this.selectedDifficulty) {
        filtered = filtered.filter(score => score.difficulty.toLowerCase() === this.selectedDifficulty.toLowerCase());
      }
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'date-desc':
            return new Date(b.attemptDate) - new Date(a.attemptDate)
          case 'date-asc':
            return new Date(a.attemptDate) - new Date(b.attemptDate)
          case 'score-desc':
            return b.score - a.score
          case 'score-asc':
            return a.score - b.score
          case 'name-asc':
            return a.quizTitle.localeCompare(b.quizTitle)
          default:
            return 0
        }
      })
      return filtered;
    },
    totalPages() {
      return Math.ceil(this.filteredScores.length / this.itemsPerPage)
    },
    paginatedScores() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredScores.slice(start, end)
    },
    visiblePages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2))
      let end = Math.min(this.totalPages, start + maxVisible - 1)
      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    },
    hasFilters() {
      return this.searchQuery || this.selectedSubject || this.selectedDifficulty || this.selectedTimeRange
    }
  },
  methods: {
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = seconds % 60
      return `${minutes}m ${remainingSeconds}s`
    },
    formatDate(dateString) {
      const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }
      return new Date(dateString).toLocaleDateString(undefined, options)
    },
    getRelativeTime(dateString) {
      const now = new Date()
      const date = new Date(dateString)
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      if (diffDays === 1) return 'Yesterday'
      if (diffDays < 7) return `${diffDays} days ago`
      if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`
      return `${Math.ceil(diffDays / 30)} months ago`
    },
    getScoreClass(score) {
      if (score >= 90) return 'text-success'
      if (score >= 80) return 'text-primary'
      if (score >= 70) return 'text-warning'
      return 'text-danger'
    },
    getScoreBadgeClass(score) {
      if (score >= 90) return 'bg-success'
      if (score >= 80) return 'bg-primary'
      if (score >= 70) return 'bg-warning'
      return 'bg-danger'
    },
    getDifficultyClass(difficulty) {
      switch (difficulty.toLowerCase()) {
        case 'easy': return 'bg-success text-white'
        case 'medium': return 'bg-warning text-white'
        case 'hard': return 'bg-danger text-white'
        default: return 'bg-secondary text-white'
      }
    },
    getPerformanceBadgeClass(score) {
      if (score >= 90) return 'badge bg-success'
      if (score >= 80) return 'badge bg-primary'
      if (score >= 70) return 'badge bg-warning'
      return 'badge bg-danger'
    },
    getPerformanceIcon(score) {
      if (score >= 90) return 'fas fa-star'
      if (score >= 80) return 'fas fa-thumbs-up'
      if (score >= 70) return 'fas fa-check'
      return 'fas fa-exclamation'
    },
    getPerformanceText(score) {
      if (score >= 90) return 'Excellent'
      if (score >= 80) return 'Good'
      if (score >= 70) return 'Average'
      return 'Needs Work'
    },
    getProgressBarClass(score) {
      if (score >= 90) return 'bg-success'
      if (score >= 80) return 'bg-primary'
      if (score >= 70) return 'bg-warning'
      return 'bg-danger'
    },
    clearFilters() {
      this.searchQuery = ''
      this.selectedSubject = ''
      this.selectedDifficulty = ''
      this.selectedTimeRange = ''
      this.currentPage = 1
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
      }
    },
    viewDetails(score) {
      this.$router.push(`/user/results`) // or `/user/quiz/${score.quizId}/results` if you want per-quiz result
    },
    async openAttemptModal(quizId) {
      this.showAttemptModal = true;
      const token = localStorage.getItem("token") || "";
      try {
        const res = await axios.get(`http://127.0.0.1:5000/api/response/${quizId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        // Defensive: ensure marked_option is int or null for MCQ, and options are always array of 4
        if (res.data && Array.isArray(res.data.questions)) {
          res.data.questions = res.data.questions.map(q => ({
            ...q,
            marked_option: q.marked_option !== undefined && q.marked_option !== null ? parseInt(q.marked_option) : null,
            correct_option: q.correct_option !== undefined && q.correct_option !== null ? parseInt(q.correct_option) : null,
            options: Array.isArray(q.options) ? q.options : []
          }));
        }
        this.attemptDetails = res.data;
      } catch {
        this.attemptDetails = null;
      }
    },
    closeAttemptModal() {
      this.showAttemptModal = false;
      this.attemptDetails = null;
    },
    questionHeaderClass(question) {
      if (question.marked_option === null) return "question-header-skipped";
      return question.is_correct ? "question-header-correct" : "question-header-incorrect";
    },
    questionBadgeClass(question) {
      if (question.marked_option === null) return "bg-warning";
      return question.is_correct ? "bg-success" : "bg-danger";
    },
    questionBadgeIcon(question) {
      if (question.marked_option === null) return "fas fa-question";
      return question.is_correct ? "fas fa-check" : "fas fa-times";
    },
    questionBadgeText(question) {
      if (question.marked_option === null) return "Skipped";
      return question.is_correct ? "Correct" : "Incorrect";
    },
    getOptionItemClass(question, optIdx) {
      if (question.marked_option === optIdx + 1 && question.is_correct) return "option-item option-correct-selected";
      if (question.marked_option === optIdx + 1 && !question.is_correct) return "option-item option-incorrect-selected";
      if (question.correct_option === optIdx + 1) return "option-item option-correct";
      return "option-item option-default";
    },
    getOptionCircleClass(question, optIdx) {
      if (question.marked_option === optIdx + 1 && question.is_correct) return "option-circle option-circle-correct-selected";
      if (question.marked_option === optIdx + 1 && !question.is_correct) return "option-circle option-circle-incorrect";
      if (question.correct_option === optIdx + 1) return "option-circle option-circle-correct";
      return "option-circle option-circle-default";
    },
    isCorrectOption(question, optIdx) {
      return question.correct_option === optIdx + 1;
    },
    isUserSelected(question, optIdx) {
      return question.marked_option === optIdx + 1;
    },
    isIncorrectSelected(question, optIdx) {
      return question.marked_option === optIdx + 1 && !question.is_correct;
    },
    getTotalQuestions() {
      if (this.attemptDetails && this.attemptDetails.questions) {
        return this.attemptDetails.questions.length;
      }
      return 0;
    }
  },
  async mounted() {
    // Fetch scores from backend
    const token = localStorage.getItem("token") || "";
    try {
      const scoresRes = await axios.get("http://127.0.0.1:5000/api/scores", {
        headers: { Authorization: `Bearer ${token}` }
      });
      const scores = Array.isArray(scoresRes.data) ? scoresRes.data : [];
      // Fetch quiz details for each score
      const quizIds = [...new Set(scores.map(s => s.quiz_id))];
      const quizDetailsMap = {};
      for (let quizId of quizIds) {
        try {
          const quizRes = await axios.get(`http://127.0.0.1:5000/api/quizzes/${quizId}/details`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          quizDetailsMap[quizId] = quizRes.data;
        } catch {
          quizDetailsMap[quizId] = {};
        }
      }
      // Build subjects list from quizzes
      this.subjects = [...new Set(Object.values(quizDetailsMap).map(q => q.subject_name).filter(Boolean))];
      // Build scores array for table
      this.scores = scores.map((s, idx) => {
        const quiz = quizDetailsMap[s.quiz_id] || {};
        let difficulty = "Medium";
        if (quiz.time_duration) {
          const dur = parseInt(quiz.time_duration);
          if (dur <= 20) difficulty = "Easy";
          else if (dur <= 35) difficulty = "Medium";
          else difficulty = "Hard";
        }
        let correctAnswers = 0;
        if (Array.isArray(s.answers_review)) {
          correctAnswers = s.answers_review.filter(r => r.is_correct).length;
        }
        return {
          id: s.id,
          quizId: s.quiz_id,
          quizTitle: quiz.name || "Quiz",
          subject: quiz.subject_name || "",
          chapter: quiz.chapter_name || "",
          difficulty,
          score: s.total_scored || 0,
          correctAnswers,
          totalQuestions: Array.isArray(quiz.questions) ? quiz.questions.length : 0,
          timeTaken: 0,
          timeLimit: quiz.time_duration || 0,
          attemptDate: s.time_stamp_of_attempt,
          rank: 1
        };
      });
    } catch (err) {
      this.scores = [];
      this.subjects = [];
    }

    // Check if we need to auto-open modal for specific score
    const scoreId = this.$route.params.scoreId;
    if (scoreId && this.$route.query.autoOpen === 'true') {
      // Find the quiz ID from the score
      const score = this.scores.find(s => s.id === parseInt(scoreId));
      if (score) {
        await this.$nextTick();
        setTimeout(() => {
          this.openAttemptModal(score.quizId);
        }, 500);
      }
    } else if (this.$route.query.autoOpen === 'true' && this.$route.query.quizId) {
      // Fallback to quiz ID based auto-open
      const quizId = parseInt(this.$route.query.quizId);
      await this.$nextTick();
      setTimeout(() => {
        this.openAttemptModal(quizId);
      }, 500);
    }
  },
  watch: {
    filteredScores() {
      this.currentPage = 1
    }
  }
}
</script>

<style scoped>
.user-scores-page {
  background-color: #f8fafc;
  min-height: 100vh;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card {
  border-radius: 1rem;
}

.badge {
  border-radius: 0.5rem;
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.text-info {
  color: #0dcaf0 !important;
}

.completion-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 2rem;
  text-align: center;
  margin-top: 2rem;
}

.completion-icon {
  font-size: 4rem;
  color: #198754;
  margin-bottom: 1rem;
}

.nav-legend {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #6c757d;
  margin-top: 1rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin-right: 0.5rem;
}

.btn-primary {
  background-color: #2563eb;
  border-color: #2563eb;
}

.btn-primary:hover {
  background-color: #1d4ed8;
  border-color: #1d4ed8;
}

.btn-success {
  background-color: #10b981;
  border-color: #10b981;
}

.btn-success:hover {
  background-color: #0f9f77;
  border-color: #0f9f77;
}

.btn-info {
  background-color: #0dcaf0;
  border-color: #0dcaf0;
}

.btn-info:hover {
  background-color: #0ab8e1;
  border-color: #0ab8e1;
}

.btn-outline-secondary {
  color: #6c757d;
  border-color: #6c757d;
}

.btn-outline-secondary:hover {
  color: #fff;
  background-color: #6c757d;
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

/* Modal Styles - Reduced Size */
.modal-lg {
  max-width: 800px;
}

.quiz-summary-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.score-display h4 {
  font-size: 1.5rem;
  margin-bottom: 0;
}

/* Question Card Styles - Compact */
.question-card {
  border: 1px solid #e9ecef;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.05);
}

.question-header {
  padding: 0.5rem 0.75rem;
  font-weight: bold;
}

.question-header-correct {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border-left: 3px solid #28a745;
}

.question-header-incorrect {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  border-left: 3px solid #dc3545;
}

.question-header-skipped {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  border-left: 3px solid #ffc107;
}

.question-number {
  background: rgba(255, 255, 255, 0.8);
  padding: 0.15rem 0.5rem;
  border-radius: 0.5rem;
  margin-right: 0.5rem;
  font-size: 0.75rem;
}

.badge-sm {
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
}

.question-body {
  padding: 0.75rem;
}

.question-text {
  font-size: 0.9rem;
  line-height: 1.4;
}

/* Option Styles - Compact */
.option-item {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  border-radius: 0.5rem;
  border: 1px solid transparent;
  transition: all 0.3s ease;
}

.option-correct {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border-color: #28a745;
}

.option-correct-selected {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border-color: #1e7e34;
}

.option-incorrect-selected {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  color: white;
  border-color: #bd2130;
}

.option-default {
  background: #f8f9fa;
  border-color: #e9ecef;
}

.option-content {
  display: flex;
  align-items: center;
}

.option-circle {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.5rem;
  font-weight: bold;
  position: relative;
  font-size: 0.75rem;
}

.option-circle-default {
  background: #6c757d;
  color: white;
}

.option-circle-correct {
  background: #28a745;
  color: white;
}

.option-circle-correct-selected {
  background: #155724;
  color: white;
}

.option-circle-incorrect {
  background: #dc3545;
  color: white;
}

.option-letter {
  font-size: 0.75rem;
  font-weight: bold;
}

.option-icon {
  position: absolute;
  top: -3px;
  right: -3px;
  background: white;
  border-radius: 50%;
  width: 12px;
  height: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.5rem;
}

.option-text {
  flex: 1;
  font-size: 0.85rem;
  line-height: 1.3;
}

.option-badges {
  margin-top: 0.25rem;
}

.badge.small {
  font-size: 0.65rem;
  padding: 0.15rem 0.4rem;
}

/* Text Answer Styles */
.text-answer-section {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 0.5rem;
  border-left: 4px solid #6c757d;
}

.user-text-answer {
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  position: relative;
}

.user-text-answer.correct-answer {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 1px solid #28a745;
  color: #155724;
}

.user-text-answer.incorrect-answer {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  border: 1px solid #dc3545;
  color: #721c24;
}

.correct-text-answer {
  padding: 0.75rem;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 1px solid #28a745;
  border-radius: 0.5rem;
  color: #155724;
  font-weight: 500;
}

.form-label {
  color: #495057;
  margin-bottom: 0.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .modal-lg {
    max-width: 95%;
    margin: 0.5rem auto;
  }
  
  .quiz-summary-header {
    padding: 0.75rem;
  }
  
  .score-display h4 {
    font-size: 1.25rem;
  }
  
  .option-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .option-circle {
    margin-right: 0;
    margin-bottom: 0.25rem;
  }
}
</style>

<!-- This file implements the user scores page.
It shows the list of quizzes attempted by the user, with scores and other details.
Users can filter, sort, and paginate the scores.
The page also shows summary statistics like total quizzes, average score, best score, etc. -->

<!-- If all questions are showing as "unattempted" or "skipped" in the attempt history modal,
it is likely because the backend is not saving the user's selected response for each question correctly.

Check these points:
1. In QuizInterface.vue, when submitting the quiz, make sure you send the user's selected answers for each question.
   - The answers object should map question IDs to the selected option (for MCQ, index+1).
2. In backend (ScoreApi), the 'user_answers' field in Score should store this mapping as JSON.
3. When fetching attempt history, the backend should parse 'user_answers' and include the user's marked option in 'answers_review'.
4. In QuizHistory.vue, you should use 'marked_option' from 'answers_review' to show which option the user selected.

If 'marked_option' is always null, it means the user's response was not saved or not parsed correctly.
Fix: Ensure you are sending and saving the user's answers for each question when submitting the quiz. -->