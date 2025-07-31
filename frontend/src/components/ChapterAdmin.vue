<!-- Chapter Administration -->
 <!-- admin can see all the chapters (using card) , and all quizzes for each chapter should be visible  and for each chapter he can create quizzes -->
<template>
  <div class="py-4 container">
    <h2 class="mb-4 fw-bold">Chapters Management</h2>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="loading" class="py-5 text-center">
      <div class="spinner-border text-primary"></div>
    </div>
    <div v-else>
      <div class="row g-4 chapter-row">
        <div v-for="chapter in chapters" :key="chapter.id" class="d-flex col-12 col-sm-6 col-md-4">
          <div class="d-flex flex-column flex-fill h-100 card chapter-card">
            <div class="d-flex flex-column card-body">
              <div class="d-flex align-items-center justify-content-between mb-2">
                <h5 class="mb-0 fw-bold" v-if="editChapterId !== chapter.id">{{ chapter.name }}</h5>
                <input v-else v-model="editChapterForm.name" class="form-control form-control-sm fw-bold" />
                <span class="bg-info badge">{{ getSubjectName(chapter.subject_id) }}</span>
              </div>
              <div v-if="editChapterId !== chapter.id">
                <p class="mb-2 text-muted">{{ chapter.description }}</p>
              </div>
              <div v-else>
                <input v-model="editChapterForm.description" class="mb-2 form-control form-control-sm" placeholder="Description" />
              </div>
              <div class="mb-2">
                <strong>Quizzes:</strong>
                <ul class="list-group list-group-flush mb-2">
                  <li v-for="quiz in quizzesForChapter(chapter.id)" :key="quiz.id" class="list-group-item d-flex align-items-center justify-content-between px-0">
                    <span>{{ quiz.name || 'Untitled Quiz' }}</span>
                    <span class="bg-secondary badge">{{ quiz.time_duration }} min</span>
                  </li>
                  <li v-if="quizzesForChapter(chapter.id).length === 0" class="list-group-item px-0 text-muted">
                    No quizzes yet.
                  </li>
                </ul>
              </div>
              <div class="d-flex gap-2 mt-auto">
                <button v-if="editChapterId !== chapter.id" class="btn-outline-primary btn btn-sm" @click="startEditChapter(chapter)">
                  <i class="bi bi-pencil"></i> Edit
                </button>
                <button v-if="editChapterId === chapter.id" class="btn btn-success btn-sm" @click="updateChapter(chapter.id)">
                  <i class="bi bi-check-lg"></i> Save
                </button>
                <button v-if="editChapterId === chapter.id" class="btn btn-secondary btn-sm" @click="cancelEditChapter">
                  <i class="bi bi-x-lg"></i> Cancel
                </button>
                <button class="btn-outline-danger btn btn-sm" @click="deleteChapter(chapter)">
                  <i class="bi bi-trash"></i> Delete
                </button>
                <button class="ms-auto btn btn-success btn-sm" @click="openAddQuizModal(chapter)">
                  <i class="bi bi-plus-circle"></i> Add Quiz
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Quiz Modal -->
    <div v-if="showAddQuizModal" class="modal fade show" style="display:block;" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Quiz to "{{ modalChapter?.name }}"</h5>
            <button type="button" class="btn-close" @click="closeAddQuizModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitAddQuiz">
              <div class="mb-3">
                <label class="form-label">Quiz Title</label>
                <input v-model="newQuiz.name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Date</label>
                <input v-model="newQuiz.date_of_quiz" class="form-control" type="date" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (minutes)</label>
                <input v-model="newQuiz.time_duration" class="form-control" type="number" min="1" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Remarks</label>
                <textarea v-model="newQuiz.remarks" class="form-control"></textarea>
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-success" type="submit">Add Quiz</button>
                <button class="btn btn-secondary" type="button" @click="closeAddQuizModal">Cancel</button>
              </div>
            </form>
            <div v-if="quizError" class="mt-3 alert alert-danger">{{ quizError }}</div>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal backdrop -->
    <div v-if="showAddQuizModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "ChapterAdmin",
  data() {
    return {
      chapters: [],
      quizzes: [],
      subjects: [],
      loading: true,
      error: "",
      showAddQuizModal: false,
      modalChapter: null,
      newQuiz: {
        name: "",
        date_of_quiz: "",
        time_duration: "",
        remarks: ""
      },
      quizError: "",
      token: localStorage.getItem("token") || "",
      editChapterId: null,
      editChapterForm: {
        name: "",
        description: ""
      }
    };
  },
  methods: {
    async fetchChapters() {
      this.loading = true;
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/chapters", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.chapters = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        this.error = err.response?.data?.message || "Error loading chapters";
      }
      this.loading = false;
    },
    async fetchQuizzes() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/quizzes", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.quizzes = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        this.error = err.response?.data?.message || "Error loading quizzes";
      }
    },
    async fetchSubjects() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/subjects", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.subjects = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        this.subjects = [];
      }
    },
    quizzesForChapter(chapterId) {
      return this.quizzes.filter(q => q.chapter_id === chapterId);
    },
    getSubjectName(subjectId) {
      const subj = this.subjects.find(s => s.id === subjectId);
      return subj ? subj.name : "N/A";
    },
    openAddQuizModal(chapter) {
      this.modalChapter = chapter;
      this.newQuiz = {
        name: "",
        date_of_quiz: "",
        time_duration: "",
        remarks: ""
      };
      this.quizError = "";
      this.showAddQuizModal = true;
    },
    closeAddQuizModal() {
      this.showAddQuizModal = false;
      this.modalChapter = null;
      this.newQuiz = {
        name: "",
        date_of_quiz: "",
        time_duration: "",
        remarks: ""
      };
      this.quizError = "";
    },
    async submitAddQuiz() {
      if (!this.modalChapter) return;
      try {
        await axios.post(
          "http://127.0.0.1:5000/api/quizzes",
          {
            name: this.newQuiz.name,
            chapter_id: this.modalChapter.id,
            date_of_quiz: this.newQuiz.date_of_quiz,
            time_duration: this.newQuiz.time_duration,
            remarks: this.newQuiz.remarks
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`
            }
          }
        );
        this.closeAddQuizModal();
        await this.fetchQuizzes();
      } catch (err) {
        this.quizError = err.response?.data?.message || "Error adding quiz";
      }
    },
    startEditChapter(chapter) {
      this.editChapterId = chapter.id;
      this.editChapterForm = {
        name: chapter.name,
        description: chapter.description || ""
      };
    },
    cancelEditChapter() {
      this.editChapterId = null;
      this.editChapterForm = { name: "", description: "" };
    },
    async updateChapter(chapterId) {
      try {
        await axios.put(
          `http://127.0.0.1:5000/api/chapters/${chapterId}`,
          {
            name: this.editChapterForm.name,
            description: this.editChapterForm.description
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`
            }
          }
        );
        await this.fetchChapters();
        this.cancelEditChapter();
      } catch (err) {
        this.error = err.response?.data?.message || "Error updating chapter";
      }
    },
    async deleteChapter(chapter) {
      if (!chapter || !chapter.id) return;
      if (!confirm(`Delete chapter "${chapter.name}"? This cannot be undone.`)) return;
      try {
        await axios.delete(`http://127.0.0.1:5000/api/chapters/${chapter.id}`, {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        await this.fetchChapters();
      } catch (err) {
        this.error = err.response?.data?.message || "Error deleting chapter";
      }
    }
  },
  async mounted() {
    await this.fetchSubjects();
    await this.fetchChapters();
    await this.fetchQuizzes();
  }
};
</script>

<style scoped>
.chapter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 24px 0;
}

.chapter-card {
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  min-height: 320px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
}

@media (max-width: 991px) {
  .chapter-row > .col-12,
  .chapter-row > .col-sm-6,
  .chapter-row > .col-md-4 {
    max-width: 100%;
    flex: 0 0 100%;
  }
}

@media (min-width: 992px) {
  .chapter-row > .col-md-4 {
    max-width: 33.3333%;
    flex: 0 0 33.3333%;
  }
}

.badge {
  font-size: 0.95rem;
  border-radius: 0.5rem;
}
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  z-index: 1050;
}
.chapter-card .d-flex.gap-2.mt-auto {
  margin-top: auto;
  gap: 8px;
  flex-wrap: wrap;
}
.chapter-card .btn-sm {
  font-size: 0.95rem;
  padding: 4px 10px;
}
.chapter-card .btn-outline-danger {
  margin-left: 0 !important;
}
.chapter-card .btn-success.btn-sm.ms-auto {
  margin-left: auto !important;
}
</style>