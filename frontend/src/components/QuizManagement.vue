<template>
  <div class="quiz-management-page">
    <h2 class="mb-4 fw-bold">Quiz Management</h2>
    <div class="d-flex align-items-center justify-content-between mb-3">
      <button class="btn btn-success add-quiz-btn" @click="openModal()">
        <i class="bi bi-plus-circle"></i> Add Quiz
      </button>
      <!-- Search input -->
      <input
        v-model="searchQuery"
        class="form-control form-control-sm"
        placeholder="Search quizzes..."
        style="max-width: 260px;"
      />
    </div>
    <!-- Wrap cards in a responsive grid row -->
    <div class="quiz-card-list row g-4">
      <transition-group name="fade-slide" tag="div" class="row g-4">
        <div
          v-for="quiz in filteredQuizzes"
          :key="quiz.id"
          class="d-flex col-12 col-sm-6 col-md-4"
        >
          <div
            class="flex-fill quiz-card"
            @mouseover="hovered = quiz.id"
            @mouseleave="hovered = null"
          >
            <div class="divider"></div>
            <div class="quiz-card-header">
              <div class="quiz-title">{{ quiz.name || 'Untitled Quiz' }}</div>
              <span class="quiz-status" :class="quizStatusClass(quiz)">
                <i v-if="quizStatus(quiz) === 'Active'" class="bi bi-check-circle-fill status-icon"></i>
                <i v-else class="bi bi-clock-fill status-icon"></i>
                {{ quizStatus(quiz) }}
              </span>
            </div>
            <div class="divider"></div>
            <div class="quiz-card-body">
              <div class="quiz-detail">
                <span class="detail-label"><i class="bi bi-journal-bookmark"></i> Chapter:</span>
                <span class="detail-value">{{ chapterName(quiz.chapter_id) }}</span>
              </div>
              <div class="quiz-detail">
                <span class="detail-label"><i class="bi bi-calendar-event"></i> End Date:</span>
                <span class="detail-value">{{ formatDate(quiz.date_of_quiz) }}</span>
              </div>
              <div class="quiz-detail">
                <span class="detail-label"><i class="bi bi-clock"></i> Duration:</span>
                <span class="detail-value">{{ quiz.time_duration }} mins</span>
              </div>
              <div class="quiz-detail">
                <span class="detail-label"><i class="bi-chat-left-text bi"></i> Remarks:</span>
                <span class="detail-value" v-tooltip="quiz.remarks">{{ truncateRemarks(quiz.remarks) }}</span>
              </div>
            </div>
            <div class="quiz-card-footer">
          
            </div>
            <div class="quiz-card-actions">
              <button class="btn-outline-primary btn-action" @click="openModal(quiz)" title="Edit">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn-outline-danger btn-action" @click="deleteQuiz(quiz.id)" title="Delete">
                <i class="bi bi-trash"></i>
              </button>
              <button class="btn-outline-info btn-action" @click="viewQuestions(quiz.id)" title="Questions">
                <i class="bi bi-eye"></i>
                <span>View Questions</span>
              </button>
            </div>
          </div>
        </div>
      </transition-group>
      <div v-if="filteredQuizzes.length === 0" class="empty-state">
        <i class="bi bi-clipboard-x empty-icon"></i>
        <div>No quizzes found</div>
      </div>
    </div>

    <!-- Add/Edit Quiz Modal -->
    <transition name="fade">
      <div class="modal" v-if="isModalOpen">
        <div class="modal-content">
          <span class="close" @click="closeModal">&times;</span>
          <div class="modal-header">
            <i class="bi-ui-check-grid bi modal-header-icon"></i>
            <h4 class="mb-3">{{ isEditMode ? 'Edit Quiz' : 'Add Quiz' }}</h4>
          </div>
          <form @submit.prevent="submitQuizForm">
            <div class="mb-2">
              <label for="name">Title:</label>
              <input v-model="quizForm.name" class="form-control" required />
            </div>
            <div class="mb-2">
              <label for="chapter">Chapter:</label>
              <select v-model="quizForm.chapter_id" class="form-control" required>
                <option v-for="chapter in chapters" :value="chapter.id" :key="chapter.id">
                  {{ chapter.name }}
                </option>
              </select>
            </div>
            <div class="mb-2">
              <label for="date">Date:</label>
              <input type="date" v-model="quizForm.date_of_quiz" class="form-control" required />
            </div>
            <div class="mb-2">
              <label for="duration">Duration (mins):</label>
              <input type="number" v-model="quizForm.time_duration" class="form-control" required />
            </div>
            <div class="mb-2">
              <label for="remarks">Remarks:</label>
              <textarea v-model="quizForm.remarks" class="form-control"></textarea>
            </div>
            <button class="w-100 btn btn-success" type="submit">{{ isEditMode ? 'Update' : 'Create' }} Quiz</button>
          </form>
        </div>
      </div>
    </transition>

    <!-- Question Management Modal -->
    <transition name="fade">
      <div class="modal" v-if="showQuestionsModal">
        <div class="modal-content question-modal-content">
          <span class="close enhanced-close" @click="closeQuestionsModal">&times;</span>
          <div class="question-modal-header">
            <div class="header-content">
              <div class="header-icon">
                <i class="bi bi-question-circle"></i>
              </div>
              <div class="header-text">
                <h4 class="modal-title">Question Management</h4>
                <p class="modal-subtitle">Create and manage quiz questions</p>
              </div>
            </div>
            <!-- Add margin-left to push the button away from the close icon -->
            <button class="ms-5 add-question-btn" style="margin-right: 40px ;"  @click="addQuestion" title="Add New Question">
              <i class="bi bi-plus-lg"></i>
              <span>Add Question</span>
            </button>
          </div>
          
          <div class="question-list-container">
            <transition-group name="fade-slide" tag="div" class="question-list">
              <div v-for="(question, idx) in questions" :key="question.id || idx" class="question-card">
                <div class="question-card-header">
                  <div class="question-number">
                    <span>{{ idx + 1 }}</span>
                  </div>
                  <div class="question-input-container">
                    <input
                      v-model="question.question_statement"
                      class="question-input"
                      :placeholder="'Enter question ' + (idx + 1)"
                    />
                  </div>
                  <div class="question-type-selector">
                    <select v-model="question.question_type" class="question-type-select">
                      <option value="mcq">Multiple Choice</option>
                      <option value="text">Text Answer</option>
                    </select>
                    <div class="type-indicator">
                      <i v-if="question.question_type === 'mcq'" class="bi bi-ui-radios"></i>
                      <i v-else class="bi bi-textarea-t"></i>
                    </div>
                  </div>
                </div>
                
                <div class="question-content">
                  <div v-if="question.question_type === 'mcq'" class="mcq-options">
                    <div class="options-header">
                      <span>Answer Options</span>
                      <small>Select the correct answer</small>
                    </div>
                    <div v-for="opt in [1,2,3,4]" :key="opt" class="option-item">
                      <div class="option-selector">
                        <input
                          type="radio"
                          :name="'correct_option_' + (question.id || idx)"
                          :value="opt"
                          v-model="question.correct_option"
                          class="option-radio"
                        />
                        <label class="option-label">{{ String.fromCharCode(64 + opt) }}</label>
                      </div>
                      <input
                        v-model="question['option'+opt]"
                        class="option-input"
                        :placeholder="'Option ' + String.fromCharCode(64 + opt)"
                      />
                    </div>
                  </div>
                  
                  <div v-else class="text-answer">
                    <div class="text-answer-header">
                      <span>Correct Answer</span>
                      <small>Enter the expected answer</small>
                    </div>
                    <input
                      v-model="question.correct_option"
                      class="text-answer-input"
                      placeholder="Enter the correct answer"
                    />
                  </div>
                </div>
              </div>
            </transition-group>
            
            <div v-if="questions.length === 0" class="empty-questions-state">
              <div class="empty-icon">
                <i class="bi bi-question-circle"></i>
              </div>
              <h5>No Questions Added</h5>
              <p>Start building your quiz by adding your first question</p>
              <button class="btn btn-primary" @click="addQuestion">
                <i class="me-2 bi bi-plus-circle"></i>Add First Question
              </button>
            </div>
          </div>
          
          <div class="question-modal-footer">
            <div class="questions-count">
              <span>{{ questions.length }} question{{ questions.length !== 1 ? 's' : '' }} added</span>
            </div>
            <button class="save-all-btn" @click="saveAllQuestions" :disabled="questions.length === 0">
              <i class="me-2 bi bi-check-circle"></i>
              Save All Questions
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <!-- Add/Edit Question Modal -->
    <transition name="fade">
      <div class="modal" v-if="showQuestionFormModal">
        <div class="modal-content">
          <span class="close" @click="closeQuestionFormModal">&times;</span>
          <div class="modal-header">
            <i class="bi bi-pencil-square modal-header-icon"></i>
            <h4 class="mb-3">{{ isEditQuestionMode ? 'Edit Question' : 'Add Question' }}</h4>
          </div>
          <form @submit.prevent="submitQuestionForm">
            <div class="mb-2">
              <label>Statement:</label>
              <input v-model="questionForm.question_statement" class="form-control" required />
            </div>
            <div class="mb-2">
              <label>Type:</label>
              <select v-model="questionForm.question_type" class="form-control">
                <option value="mcq">MCQ</option>
                <option value="text">Text</option>
              </select>
            </div>
            <div v-if="questionForm.question_type === 'mcq'">
              <div class="mb-2" v-for="opt in [1,2,3,4]" :key="opt">
                <label>Option {{ opt }}:</label>
                <input v-model="questionForm['option'+opt]" class="form-control" required />
              </div>
              <div class="mb-2">
                <label>Correct Option:</label>
                <select v-model="questionForm.correct_option" class="form-control" required>
                  <option v-for="opt in [1,2,3,4]" :value="opt">{{ opt }}</option>
                </select>
              </div>
            </div>
            <button class="w-100 btn btn-success" type="submit">{{ isEditQuestionMode ? 'Update' : 'Add' }} Question</button>
          </form>
        </div>
      </div>
    </transition>
    <!-- Floating Add Quiz Button -->
    <button class="floating-add-btn btn btn-success" @click="openModal()" title="Add Quiz">
      <i class="bi bi-plus-lg"></i>
    </button>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "QuizManagement",
  data() {
    return {
      quizzes: [],
      chapters: [],
      isModalOpen: false,
      isEditMode: false,
      quizForm: {
        name: "",
        chapter_id: "",
        date_of_quiz: "",
        time_duration: "",
        remarks: ""
      },
      showQuestionsModal: false,
      selectedQuizId: null,
      questions: [],
      showQuestionFormModal: false,
      isEditQuestionMode: false,
      questionForm: {
        question_statement: "",
        question_type: "mcq",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: 1
      },
      editQuestionId: null,
      token: localStorage.getItem("token") || "",
      hovered: null,
      searchQuery: ""
    };
  },
  computed: {
    filteredQuizzes() {
      if (!this.searchQuery.trim()) return this.quizzes;
      const q = this.searchQuery.trim().toLowerCase();
      return this.quizzes.filter(
        quiz =>
          (quiz.name && quiz.name.toLowerCase().includes(q)) ||
          (quiz.remarks && quiz.remarks.toLowerCase().includes(q)) ||
          (this.chapterName(quiz.chapter_id) && this.chapterName(quiz.chapter_id).toLowerCase().includes(q))
      );
    }
  },
  methods: {
    fetchQuizzes() {
      axios
        .get("http://127.0.0.1:5000/api/quizzes", {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(res => {
          this.quizzes = res.data;
        });
    },
    fetchChapters() {
      axios
        .get("http://127.0.0.1:5000/api/chapters", {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(res => {
          this.chapters = res.data;
        });
    },
    chapterName(chapterId) {
      const chapter = this.chapters.find(c => c.id === chapterId);
      return chapter ? chapter.name : "N/A";
    },
    quizStatus(quiz) {
      const today = new Date().toISOString().slice(0, 10);
      return quiz.date_of_quiz >= today ? "Active" : "Expired";
    },
    quizStatusClass(quiz) {
      return quiz.date_of_quiz >= new Date().toISOString().slice(0, 10)
        ? "badge bg-success"
        : "badge bg-secondary";
    },
    openModal(quiz = null) {
      this.isEditMode = !!quiz;
      if (quiz) {
        this.quizForm = {
          name: quiz.name || "",
          chapter_id: quiz.chapter_id,
          date_of_quiz: quiz.date_of_quiz,
          time_duration: quiz.time_duration,
          remarks: quiz.remarks,
          id: quiz.id
        };
      } else {
        this.quizForm = {
          name: "",
          chapter_id: "",
          date_of_quiz: "",
          time_duration: "",
          remarks: ""
        };
      }
      this.isModalOpen = true;
    },
    closeModal() {
      this.isModalOpen = false;
    },
    submitQuizForm() {
      if (this.isEditMode) {
        axios
          .put(`http://127.0.0.1:5000/api/quizzes/${this.quizForm.id}`, this.quizForm, {
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.token}` }
          })
          .then(() => {
            this.fetchQuizzes();
            this.closeModal();
          });
      } else {
        axios
          .post("http://127.0.0.1:5000/api/quizzes", this.quizForm, {
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.token}` }
          })
          .then(() => {
            this.fetchQuizzes();
            this.closeModal();
          });
      }
    },
    deleteQuiz(quizId) {
      if (!confirm("Delete this quiz?")) return;
      axios
        .delete(`http://127.0.0.1:5000/api/quizzes/${quizId}`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(() => {
          this.fetchQuizzes();
        });
    },
    viewQuestions(quizId) {
      this.selectedQuizId = quizId;
      axios
        .get(`http://127.0.0.1:5000/api/questions`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(res => {
          // Fix: Ensure correct type and value for question_type
          this.questions = res.data
            .filter(q => q.quiz_id === quizId)
            .map(q => {
              // Accept only "mcq" or "text" (case-insensitive), fallback to "mcq"
              let qt = (q.question_type || "").toString().trim().toLowerCase();
              qt = qt === "text" ? "text" : "mcq";
              return {
                ...q,
                question_type: qt,
                option1: q.option1 || "",
                option2: q.option2 || "",
                option3: q.option3 || "",
                option4: q.option4 || "",
                correct_option: q.correct_option || (qt === "mcq" ? 1 : "")
              };
            });
          this.showQuestionsModal = true;
        });
    },
    closeQuestionsModal() {
      this.showQuestionsModal = false;
      this.selectedQuizId = null;
      this.questions = [];
    },
    addQuestion() {
      this.questions.push({
        question_statement: "",
        question_type: "mcq",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        correct_option: 1,
        quiz_id: this.selectedQuizId
      });
    },
    deleteQuestion(questionId, idx) {
      if (!confirm("Delete this question?")) return;
      if (questionId) {
        axios
          .delete(`http://127.0.0.1:5000/api/questions/${questionId}`, {
            headers: { Authorization: `Bearer ${this.token}` }
          })
          .then(() => {
            this.questions = this.questions.filter(q => q.id !== questionId);
          });
      } else {
        // Remove unsaved question by index
        this.questions.splice(idx, 1);
      }
    },
    saveAllQuestions() {
      // Save all questions (new and edited)
      const requests = this.questions.map(q => {
        const payload = {
          question_statement: q.question_statement,
          question_type: q.question_type,
          option1: q.option1,
          option2: q.option2,
          option3: q.option3,
          option4: q.option4,
          correct_option: q.correct_option,
          quiz_id: q.quiz_id || this.selectedQuizId
        };
        if (q.id) {
          // Update existing question
          return axios.put(`http://127.0.0.1:5000/api/questions/${q.id}`, payload, {
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.token}` }
          });
        } else {
          // Create new question
          return axios.post("http://127.0.0.1:5000/api/questions", payload, {
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${this.token}` }
          });
        }
      });
      Promise.all(requests).then(() => {
        this.viewQuestions(this.selectedQuizId);
        alert("All questions saved!");
      });
    },
    formatDate(dateString) {
      if (!dateString) return "N/A";
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return "N/A";
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return date.toLocaleDateString(undefined, options);
    },
    truncateRemarks(remarks) {
      return remarks.length > 50 ? remarks.slice(0, 50) + '...' : remarks;
    }
  },
  mounted() {
    this.fetchQuizzes();
    this.fetchChapters();
  }
};
</script>

<style scoped>
.quiz-management-page {
  padding: 20px;
  background: #f6f8fb;
  min-height: 100vh;
  position: relative;
}

/* Use Bootstrap grid for cards */
.quiz-card-list {
  margin-left: 0;
  margin-right: 0;
}

.quiz-card {
  background: linear-gradient(135deg, #f8fbff 0%, #eaf4ff 100%);
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(79,140,255,0.10);
  max-width: 370px;
  min-width: 320px;
  flex: 1 1 340px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
  transition: box-shadow 0.2s, transform 0.2s;
  position: relative;
  width: 100%;
}

@media (max-width: 991px) {
  .quiz-card-list .col-12,
  .quiz-card-list .col-sm-6,
  .quiz-card-list .col-md-4 {
    max-width: 100%;
    flex: 0 0 100%;
  }
}

@media (min-width: 992px) {
  .quiz-card-list .col-md-4 {
    max-width: 33.3333%;
    flex: 0 0 33.3333%;
  }
}

.quiz-card:hover {
  box-shadow: 0 8px 32px rgba(79,140,255,0.18);
}

.quiz-card-header {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  padding: 24px 18px 10px 18px;
}

.quiz-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #3094f1;
  text-align: center;
  margin-bottom: 8px;
  letter-spacing: 1px;
  word-break: break-word;
  background: linear-gradient(90deg, #fce7e7 0%, #ffe0e0 100%);
  border-radius: 10px;
  padding: 8px 0;
  box-shadow: 0 1px 8px rgba(79,140,255,0.07);
}

.quiz-status {
  top: 18px;
  right: 18px;
  background: #e6ffe6;
  color: #218838;
  font-size: 0.93rem;
  font-weight: 600;
  border-radius: 12px;
  padding: 3px 10px 3px 8px;
  box-shadow: 0 1px 4px rgba(33,136,56,0.07);
  border: none;
  display: flex;
  align-items: center;
  gap: 4px;
  min-width: 70px;
  justify-content: flex-start;
}

.status-icon {
  font-size: 1rem;
  vertical-align: middle;
  margin-right: 3px;
}

.bg-success {
  background: #e6ffe6 !important;
  color: #218838 !important;
}

.bg-secondary {
  background: #f0f0f0 !important;
  color: #383d41 !important;
}

.divider {
  width: 80%;
  height: 2px;
  background: linear-gradient(90deg, #3094f1 0%, #ffe0e0 100%);
  margin: 0 auto 16px auto;
  border-radius: 2px;
}

.quiz-card-body {
  width: 100%;
  padding: 0 24px 0 24px;
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  background: #f6f8fb;
  border-radius: 10px;
}

.quiz-detail {
  display: flex;
  gap: 8px;
  font-size: 1.07rem;
  align-items: center;
}

.detail-label {
  font-weight: 600;
  color: #2d3a4a;
  min-width: 110px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.detail-value {
  color: #444;
  font-weight: 400;
  word-break: break-word;
}

.quiz-card-actions {
  width: 100%;
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 8px;
}

.btn-action {
  font-size: 1.1rem;
  padding: 8px 14px;
  border-radius: 50px;
  font-weight: 500;
  box-shadow: 0 1px 4px rgba(79,140,255,0.07);
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-outline-primary {
  border: 2px solid #3094f1;
  color: #3094f1;
  background: #fff;
}

.btn-outline-primary:hover {
  background: #3094f1;
  color: #fff;
}

.btn-outline-danger {
  border: 2px solid #ff7e5f;
  color: #ff7e5f;
  background: #fff;
}

.btn-outline-danger:hover {
  background: #ff7e5f;
  color: #fff;
}

.btn-outline-info {
  border: 2px solid #17a2b8;
  color: #17a2b8;
  background: #fff;
}

.btn-outline-info:hover {
  background: #17a2b8;
  color: #fff;
}

.add-quiz-btn {
  position: relative;
  z-index: 2;
}

.floating-add-btn {
  position: fixed;
  right: 32px;
  bottom: 32px;
  z-index: 3000;
  border-radius: 50%;
  width: 56px;
  height: 56px;
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(79,140,255,0.18);
}

.floating-add-btn i {
  margin: 0;
}

.empty-state {
  width: 100%;
  text-align: center;
  color: #b0b4bb;
  font-size: 1.2rem;
  margin-top: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.empty-icon {
  font-size: 2.8rem;
  color: #eaf4ff;
}

.modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: #fff;
  padding: 32px 24px 24px 24px;
  border-radius: 16px;
  min-width: 340px;
  max-width: 95vw;
  position: relative;
  box-shadow: 0 2px 16px rgba(0,0,0,0.10);
  animation: fadeInModal 0.3s;
}

.close {
  cursor: pointer;
  position: absolute;
  top: 18px;
  right: 24px;
  font-size: 1.7rem;
  color: #888;
  z-index: 2;
  /* ...existing code... */
}

/* Add enhanced style for modal close button */
.enhanced-close {
  background: #f1f5f9;
  border-radius: 50%;
  padding: 6px 14px 8px 14px;
  box-shadow: 0 2px 8px rgba(79,140,255,0.10);
  border: 1px solid #e2e8f0;
  transition: background 0.2s, color 0.2s;
}
.enhanced-close:hover {
  background: #e0e7ef;
  color: #222;
}

/* Add margin to the Add Question button to move it away from close */
.ms-5 {
  margin-left: 2.5rem !important;
}

.fade-enter-active, .fade-leave-active, .fade-slide-enter-active, .fade-slide-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter, .fade-leave-to, .fade-slide-enter, .fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* NEW QUESTION MODAL STYLES */
.question-modal-content {
  max-width: 900px;
  min-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 0;
}

.question-modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 24px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 16px 16px 0 0;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.header-text h4 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.modal-subtitle {
  margin: 4px 0 0 0;
  opacity: 0.9;
  font-size: 0.95rem;
}

.add-question-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 12px 20px;
  border-radius: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.add-question-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.question-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
  background: #f8fafc;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.question-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  overflow: hidden;
  transition: all 0.3s ease;
}

.question-card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.question-card-header {
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  padding: 20px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.question-number {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  flex-shrink: 0;
}

.question-input-container {
  flex: 1;
}

.question-input {
  width: 100%;
  border: none;
  background: transparent;
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  padding: 8px 0;
  outline: none;
}

.question-input::placeholder {
  color: #94a3b8;
  font-weight: 500;
}

.question-type-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.question-type-select {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #475569;
  outline: none;
  transition: border-color 0.3s ease;
}

.question-type-select:focus {
  border-color: #3b82f6;
}

.type-indicator {
  width: 32px;
  height: 32px;
  background: #f1f5f9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  font-size: 1.1rem;
}

.question-content {
  padding: 24px;
}

.mcq-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.9rem;
  font-weight: 500;
  color: #475569;
  outline: none;
  transition: border-color 0.3s ease;
}

.question-type-select:focus {
  border-color: #3b82f6;
}

.type-indicator {
  width: 32px;
  height: 32px;
  background: #f1f5f9;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  font-size: 1.1rem;
}

.question-content {
  padding: 24px;
}

.mcq-options {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.options-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.options-header span {
  font-weight: 600;
  color: #374151;
  font-size: 1rem;
}

.options-header small {
  color: #6b7280;
  font-size: 0.85rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 12px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.option-item:hover {
  background: #f1f5f9;
  border-color: #e2e8f0;
}

.option-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.option-radio {
  width: 20px;
  height: 20px;
  accent-color: #3b82f6;
}

.option-label {
  width: 24px;
  height: 24px;
  background: #e2e8f0;
  color: #64748b;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  margin: 0;
}

.option-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 1rem;
  color: #374151;
  padding: 8px 0;
  outline: none;
}

.option-input::placeholder {
  color: #9ca3af;
}

.text-answer {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.text-answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text-answer-header span {
  font-weight: 600;
  color: #374151;
  font-size: 1rem;
}

.text-answer-header small {
  color: #6b7280;
  font-size: 0.85rem;
}

.text-answer-input {
  width: 100%;
  padding: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  color: #374151;
  background: #f8fafc;
  outline: none;
  transition: all 0.3s ease;
}

.text-answer-input:focus {
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.text-answer-input::placeholder {
  color: #9ca3af;
}

.empty-questions-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}

.empty-questions-state .empty-icon {
  font-size: 4rem;
  color: #cbd5e1;
  margin-bottom: 16px;
}

.empty-questions-state h5 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

.empty-questions-state p {
  font-size: 1rem;
  margin-bottom: 24px;
}

.question-modal-footer {
  background: white;
  padding: 20px 32px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 0 0 16px 16px;
}

.questions-count {
  color: #64748b;
  font-size: 0.95rem;
  font-weight: 500;
}

.save-all-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  cursor: pointer;
}

.save-all-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
}

.save-all-btn:disabled {
  background: #d1d5db;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .question-modal-content {
    min-width: 95vw;
    max-height: 95vh;
  }
  
  .question-modal-header {
    padding: 20px;
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .question-list-container {
    padding: 16px;
  }
  
  .question-card-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .question-type-selector {
    justify-content: space-between;
  }
  
  .option-item {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .option-selector {
    justify-content: flex-start;
  }
}
</style>