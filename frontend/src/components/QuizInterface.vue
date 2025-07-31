<template>
  <div class="quiz-interface">
    <div class="py-4 container-fluid">
      <!-- Quiz Header -->
      <div class="mb-4 row">
        <div class="col-12">
          <div class="border-0 quiz-header card">
            <div class="card-body">
              <div class="align-items-center row">
                <div class="col-md-8">
                  <h3 class="mb-2 fw-bold">{{ quiz.name }}</h3>
                  <p class="mb-0 text-muted">{{ quiz.subjectName }} • {{ quiz.chapterName }}</p>
                </div>
                <div class="text-md-end col-md-4">
                  <div class="quiz-progress">
                    <div class="mb-2 progress" style="height: 8px;">
                      <div 
                        class="bg-primary progress-bar" 
                        :style="`width: ${(currentQuestion / quiz.questions.length) * 100}%`"
                      ></div>
                    </div>
                    <small class="text-muted">
                      Question {{ currentQuestion }} of {{ quiz.questions.length }}
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz Content -->
      <div class="row" v-if="!quizCompleted">
        <div class="mx-auto col-lg-8">
          <div class="border-0 question-card card" style="position:relative;">
            <!-- Timer on top right of question card -->
            <div class="quiz-timer-card" v-if="!quizCompleted">
              <div class="timer-content">
                <i class="me-2 fas fa-clock"></i>
                <span class="timer-text">{{ formatTime(timeRemaining) }}</span>
              </div>
            </div>
            <div class="p-5 card-body">
              <div class="question-content">
                <div class="mb-3 question-number">
                  <span class="bg-primary px-3 py-2 badge fs-6">
                    Question {{ currentQuestion }}
                  </span>
                </div>
                
                <h4 class="mb-4 question-text">
                  {{ getCurrentQuestion().statement }}
                </h4>
                <div class="options-list">
                  <template v-if="getCurrentQuestion().question_type === 'mcq'">
                    <div 
                      v-for="(option, index) in getCurrentQuestion().options" 
                      :key="index"
                      class="mb-3 option-item"
                    >
                      <div 
                        class="form-check option-clickable"
                        :class="{ 'selected': selectedAnswers[currentQuestion - 1] === index }"
                        @click="selectedAnswers[currentQuestion - 1] = index"
                      >
                        <input 
                          class="form-check-input" 
                          type="radio" 
                          :name="`question-${currentQuestion}`"
                          :id="`option-${index}`"
                          :value="index"
                          v-model="selectedAnswers[currentQuestion - 1]"
                          style="pointer-events:none;"
                        >
                        <label class="w-100 form-check-label" :for="`option-${index}`">
                          <div class="option-content">
                            <span class="option-letter">{{ String.fromCharCode(65 + index) }}.</span>
                            <span class="option-text">{{ option }}</span>
                          </div>
                        </label>
                      </div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="mb-3 option-item">
                      <input
                        type="text"
                        class="form-control"
                        v-model="selectedAnswers[currentQuestion - 1]"
                        :placeholder="'Type your answer here...'"
                      />
                    </div>
                  </template>
                </div>

                <div class="mt-5 question-actions">
                  <div class="row">
                    <div class="col-6">
                      <button 
                        class="btn-outline-secondary w-100 btn"
                        @click="previousQuestion"
                        :disabled="currentQuestion === 1"
                      >
                        <i class="fa-chevron-left me-2 fas"></i>
                        Previous
                      </button>
                    </div>
                    <div class="col-6">
                      <button 
                        v-if="currentQuestion < quiz.questions.length"
                        class="w-100 btn btn-primary"
                        @click="nextQuestion"
                      >
                        Next
                        <i class="fa-chevron-right ms-2 fas"></i>
                      </button>
                      <button 
                        v-else
                        class="w-100 btn btn-success"
                        @click="submitQuiz"
                      >
                        <i class="me-2 fas fa-check"></i>
                        Submit Quiz
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Question Navigation Sidebar -->
        <div class="col-lg-3 offset-lg-1">
          <div class="sticky-top border-0 question-nav card">
            <div class="bg-white border-0 card-header">
              <h6 class="mb-0 fw-bold">Question Navigation</h6>
            </div>
            <div class="card-body">
              <div class="question-grid">
                <button
                  v-for="(question, index) in quiz.questions"
                  :key="index"
                  class="question-nav-btn btn"
                  :class="getQuestionNavClass(index + 1)"
                  @click="goToQuestion(index + 1)"
                >
                  {{ index + 1 }}
                </button>
              </div>
              
              <div class="mt-3 nav-legend">
                <div class="d-flex align-items-center mb-2 legend-item">
                  <div class="bg-primary legend-color"></div>
                  <small class="text-muted">Current</small>
                </div>
                <div class="d-flex align-items-center mb-2 legend-item">
                  <div class="bg-success legend-color"></div>
                  <small class="text-muted">Answered</small>
                </div>
                <div class="d-flex align-items-center legend-item">
                  <div class="bg-light border legend-color"></div>
                  <small class="text-muted">Not Answered</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz Completion -->
      <div class="row" v-if="quizCompleted">
        <div class="mx-auto col-lg-8">
          <div class="border-0 text-center completion-card card">
            <div class="p-5 card-body">
              <div class="mb-4 completion-icon">
                <i class="text-success fas fa-check-circle fa-5x"></i>
              </div>
              <h2 class="mb-3 fw-bold">Quiz Completed!</h2>
              <p class="mb-4 text-muted lead">
                Great job! You've successfully completed the quiz. 
                Your responses have been submitted for evaluation.
              </p>
              <div class="mb-4 text-center completion-stats row">
                <div class="col-md-4">
                  <h4 class="text-primary fw-bold">{{ quiz.questions.length }}</h4>
                  <small class="text-muted">Total Questions</small>
                </div>
                <div class="col-md-4">
                  <h4 class="text-success fw-bold">{{ getAnsweredCount() }}</h4>
                  <small class="text-muted">Answered</small>
                </div>
                <div class="col-md-4">
                  <h4 class="text-info fw-bold">{{ formatTime(quiz.duration * 60 - timeRemaining) }}</h4>
                  <small class="text-muted">Time Taken</small>
                </div>
              </div>
              <div class="completion-actions">
                <button class="me-3 btn btn-primary btn-lg" @click="viewResults">
                  <i class="me-2 fas fa-chart-bar"></i>
                  View Results
                </button>
                <router-link to="/user/dashboard" class="btn-outline-secondary btn btn-lg">
                  <i class="me-2 fas fa-home"></i>
                  Back to Dashboard
                </router-link>
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
  name: 'QuizInterface',
  data() {
    return {
      currentQuestion: 1,
      selectedAnswers: [],
      timeRemaining: 0,
      quizCompleted: false,
      timer: null,
      scoreId: null,
      quiz: {
        id: null,
        name: '',
        subjectName: '',
        chapterName: '',
        duration: 0,
        questions: []
      },
      token: localStorage.getItem("token") || ""
    }
  },
  async mounted() {
    await this.fetchQuizData();
    this.initializeQuiz();
  },
  beforeUnmount() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  methods: {
    async fetchQuizData() {
      const quizId = this.$route.params.quizId;
      try {
        // Use new details endpoint
        const res = await axios.get(`http://127.0.0.1:5000/api/quizzes/${quizId}/details`, {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        const quiz = res.data;
        this.quiz.id = quiz.id;
        this.quiz.name = quiz.name || "Untitled Quiz";
        this.quiz.duration = parseInt(quiz.time_duration) || 30;
        this.quiz.chapterName = quiz.chapter_name || "";
        this.quiz.subjectName = quiz.subject_name || "";
        this.quiz.questions = quiz.questions.map(q => ({
          id: q.id,
          statement: q.question_statement,
          options: q.question_type === "mcq"
            ? [q.option1, q.option2, q.option3, q.option4].filter(opt => opt !== null && opt !== undefined && opt !== "")
            : [],
          question_type: q.question_type,
          correctAnswer: q.correct_option
        }));
      } catch (err) {
        this.quiz = { id: null, name: "Quiz Not Found", duration: 0, questions: [] };
      }
    },

    initializeQuiz() {
      // Initialize selected answers array
      this.selectedAnswers = new Array(this.quiz.questions.length).fill(null);
      // Set timer
      this.timeRemaining = this.quiz.duration * 60; // Convert to seconds
      this.startTimer();
    },

    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeRemaining > 0) {
          this.timeRemaining--;
        } else {
          this.submitQuiz();
        }
      }, 1000);
    },

    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    },

    getCurrentQuestion() {
      // Defensive: always return a question object with required fields
      const q = this.quiz.questions[this.currentQuestion - 1];
      if (!q) return { statement: '', options: [], question_type: 'mcq' };
      // Ensure options array for MCQ
      if (q.question_type === "mcq") {
        return {
          ...q,
          options: Array.isArray(q.options)
            ? q.options.filter(opt => opt !== null && opt !== undefined && opt !== "")
            : []
        };
      }
      return q;
    },

    nextQuestion() {
      if (this.currentQuestion < this.quiz.questions.length) {
        this.currentQuestion++;
      }
    },

    previousQuestion() {
      if (this.currentQuestion > 1) {
        this.currentQuestion--;
      }
    },

    goToQuestion(questionNumber) {
      this.currentQuestion = questionNumber;
    },

    getQuestionNavClass(questionNumber) {
      if (questionNumber === this.currentQuestion) {
        return 'btn-primary';
      } else if (this.selectedAnswers[questionNumber - 1] !== null) {
        return 'btn-success';
      } else {
        return 'btn-outline-secondary';
      }
    },

    getAnsweredCount() {
      return this.selectedAnswers.filter(answer => answer !== null).length;
    },

    async submitQuiz() {
      if (this.timer) {
        clearInterval(this.timer);
      }
      this.quizCompleted = true;

      // Prepare answers for backend
      const answers = {};
      this.quiz.questions.forEach((q, idx) => {
        if (q.question_type === "mcq") {
          answers[q.id] = this.selectedAnswers[idx] !== null ? (parseInt(this.selectedAnswers[idx]) + 1) : null;
        } else {
          answers[q.id] = this.selectedAnswers[idx];
        }
      });

      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/api/quizzes/${this.quiz.id}/attempt`,
          { answers },
          { headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.token}` } }
        );
        
        // Store score ID for later use
        this.scoreId = response.data.score_id;
        
      } catch (err) {
        // handle error if needed
      }
    },

    viewResults() {
      // Redirect to specific score route with auto-open modal
      this.$router.push({
        path: `/user/results/${this.scoreId}`,
        query: { 
          autoOpen: 'true',
          justCompleted: 'true'
        }
      });
    }
  }
};
</script>

<style scoped>
.quiz-timer-card {
  position: absolute;
  top: 18px;
  right: 24px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 0.75rem;
  font-weight: bold;
  z-index: 10;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
  animation: pulse 2s infinite;
  display: flex;
  align-items: center;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.timer-content {
  display: flex;
  align-items: center;
}

.timer-text {
  font-size: 1.1rem;
  font-family: 'Courier New', monospace;
}

.quiz-header {
  border-radius: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.question-card {
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  min-height: 500px;
}

.question-number .badge {
  border-radius: 2rem;
}

.question-text {
  line-height: 1.6;
  color: #1e293b;
}

.option-item {
  transition: all 0.2s ease;
}

.option-item:hover {
  transform: translateX(5px);
}

.form-check {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1rem;
  transition: all 0.2s ease;
}

.form-check:hover {
  border-color: #3b82f6;
  background: #eff6ff;
}

.form-check-input:checked ~ .form-check-label .form-check {
  border-color: #3b82f6;
  background: #eff6ff;
}

.option-content {
  display: flex;
  align-items: center;
  width: 100%;
}

.option-letter {
  font-weight: bold;
  color: #3b82f6;
  margin-right: 1rem;
  min-width: 30px;
}

.option-text {
  flex: 1;
}

.question-nav {
  border-radius: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.question-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.question-nav-btn {
  aspect-ratio: 1;
  border-radius: 0.5rem;
  font-weight: bold;
  transition: all 0.2s ease;
}

.question-nav-btn:hover {
  transform: scale(1.1);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 0.25rem;
  margin-right: 0.5rem;
}

.completion-card {
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.completion-icon {
  animation: bounceIn 1s ease-out;
}

@keyframes bounceIn {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.completion-stats {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 2rem;
}

.option-clickable {
  cursor: pointer;
}
.option-clickable.selected {
  background: #f1f7ff;
  border: 2px solid #2563eb;
}

@media (max-width: 768px) {
  .quiz-timer {
    position: relative;
    top: auto;
    right: auto;
    margin-bottom: 1rem;
    text-align: center;
  }
  
  .question-grid {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .question-actions .btn {
    margin-bottom: 0.5rem;
  }
  
  .completion-actions .btn {
    display: block;
    width: 100%;
    margin-bottom: 0.5rem;
  }
}
</style>

<!-- This file implements the quiz interface for users.
It loads quiz details, chapter, subject, and questions from the backend APIs.
It supports MCQ and text questions, shows a timer, navigation, and submits answers to the backend.
If MCQ options are missing, check your backend data for option1/option2/option3/option4 fields. -->

<!-- This file implements the quiz interface for users.
It loads quiz details, chapter, subject, and questions from the backend APIs.
It supports MCQ and text questions, shows a timer, navigation, and submits answers to the backend.
If MCQ options are missing, check your backend data for option1/option2/option3/option4 fields. -->
<!-- This file implements the quiz interface for users.
It loads quiz details, chapter, subject, and questions from the backend APIs.
It supports MCQ and text questions, shows a timer, navigation, and submits answers to the backend.
If MCQ options are missing, check your backend data for option1/option2/option3/option4 fields. -->

