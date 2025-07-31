<template>
  <div class="py-4 subjects-admin container">
    <div class="d-flex align-items-center justify-content-between mb-4">
      <h2 class="mb-0 fw-bold">Subjects</h2>
      <div class="d-flex align-items-center gap-2">
        <!-- Search input -->
        <input
          v-model="searchQuery"
          class="form-control form-control-sm"
          placeholder="Search subjects..."
          style="max-width: 220px;"
        />
        <button class="btn btn-success" @click="showAdd = !showAdd">
          <i class="bi bi-plus-circle"></i> Add Subject
        </button>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="loading" class="py-5 text-center">
      <div class="spinner-border text-primary"></div>
    </div>
    <div v-else>
      <transition name="fade">
        <div v-if="showAdd" class="shadow-sm mb-4 card glass-card">
          <div class="card-body">
            <h5 class="mb-3 fw-bold">Add New Subject</h5>
            <form @submit.prevent="addSubject" class="align-items-end row g-2">
              <div class="col-md-5">
                <input v-model="newSubject.name" class="form-control" placeholder="Name" required />
              </div>
              <div class="col-md-5">
                <input v-model="newSubject.description" class="form-control" placeholder="Description" required />
              </div>
              <div class="col-md-2">
                <button class="w-100 btn btn-success" type="submit">Add</button>
              </div>
            </form>
          </div>
        </div>
      </transition>
      <div class="d-flex flex-wrap gap-4 subjects-list">
        <div
          v-for="(subject, idx) in filteredSubjects"
          :key="subject.id"
          class="shadow-sm subject-card"
        >
          <div class="d-flex flex-column card-body">
            <div class="card-header-actions">
              <template v-if="editId === subject.id">
                <input v-model="editForm.name" class="mb-2 form-control" placeholder="Name" />
                <input v-model="editForm.description" class="mb-2 form-control" placeholder="Description" />
                <button class="btn btn-success btn-sm" @click="updateSubject(subject.id)">
                  <i class="bi bi-check-lg"></i>
                </button>
                <button class="btn btn-secondary btn-sm" @click="cancelEdit">
                  <i class="bi bi-x-lg"></i>
                </button>
              </template>
              <template v-else>
                <button class="btn-outline-primary btn btn-sm" @click="startEdit(subject)">
                  <i class="bi bi-pencil"></i>
                </button>
                <button class="btn-outline-danger btn btn-sm" @click="deleteSubject(subject.id)">
                  <i class="bi bi-trash"></i>
                </button>
              </template>
            </div>
            <div class="d-flex align-items-center mb-2 pt-5">
              <div class="me-3 text-white subject-avatar gradient-bg">
                {{ subject.name.charAt(0).toUpperCase() }}
              </div>
              <h5 class="mb-0 card-title">{{ subject.name }}</h5>
            </div>
            <p class="mb-3 text-muted card-text">{{ subject.description }}</p>
              <table class="chapter-table table table-bordered table-sm">
                <thead>
                  <tr>
                    <th>Chapter Name</th>
                    <th>Description</th>
                    <th>Questions</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="chapter in chaptersForSubject(subject.id)" :key="chapter.id">
                    <template v-if="editChapterId === chapter.id">
                      <td>
                        <input v-model="editChapterForm.name" class="form-control" placeholder="Chapter Name" />
                      </td>
                      <td>
                        <input v-model="editChapterForm.description" class="form-control" placeholder="Description" />
                      </td>
                      <td>
                        <input v-model="editChapterForm.questions_count" class="form-control" placeholder="Questions" type="number" min="0" />
                      </td>
                      <td>
                        <button class="me-1 btn btn-success btn-sm" @click="updateChapter(chapter.id)">
                          <i class="bi bi-check-lg"></i>
                        </button>
                        <button class="btn btn-secondary btn-sm" @click="cancelEditChapter">
                          <i class="bi bi-x-lg"></i>
                        </button>
                      </td>
                    </template>
                    <template v-else>
                      <td class="chapter-name">{{ chapter.name }}</td>
                      <td class="chapter-description">{{ chapter.description }}</td>
                      <td>{{ chapter.questions_count || 'N/A' }}</td>
                      <td>
                        <button class="me-1 btn-outline-primary btn btn-sm" @click="startEditChapter(chapter)">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn-outline-danger btn btn-sm" @click="deleteChapter(chapter)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </td>
                    </template>
                  </tr>
                  <tr v-if="chaptersForSubject(subject.id).length === 0">
                    <td colspan="4" class="text-muted text-center">No chapters</td>
                  </tr>
                </tbody>
              </table>
          </div>
          <div class="px-3 py-2 text-start card-footer">
            <span class="badge badge-index">
              {{ idx + 1 }}
            </span>
          </div>
          <!-- Add Chapter Button at bottom center of card -->
          <button
            class="add-chapter-btn"
            @click="openAddChapterModal(subject)"
            title="Add Chapter"
          >
            <i class="bi bi-plus-lg"></i>
          </button>
        </div>
      </div>
      <div v-if="subjects.length === 0" class="py-4 text-muted text-center">
        <i class="bi bi-folder-x fs-2"></i>
        <div>No subjects found.</div>
      </div>
    </div>

    <!-- Add Chapter Modal -->
    <transition name="fade">
      <div v-if="showAddChapterModal" class="add-chapter-modal">
        <div class="p-4 card glass-card">
          <h5 class="mb-3 fw-bold">Add Chapter to "{{ modalSubject?.name }}"</h5>
          <form @submit.prevent="submitAddChapter" class="row g-2">
            <div class="mb-2 col-12">
              <input v-model="newChapter.name" class="form-control" placeholder="Chapter Name" required />
            </div>
            <div class="mb-2 col-12">
              <input v-model="newChapter.description" class="form-control" placeholder="Description" required />
            </div>
            <div class="col-12">
              <button class="w-100 btn btn-success" type="submit">Add Chapter</button>
              <button class="mt-2 w-100 btn btn-secondary" type="button" @click="closeAddChapterModal">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "SubjectsAdmin",
  data() {
    return {
      subjects: [],
      chapters: [],
      loading: true,
      error: "",
      editId: null,
      editForm: { name: "", description: "" },
      newSubject: { name: "", description: "" },
      showAdd: false,
      showAddChapterModal: false,
      modalSubject: null,
      newChapter: { name: "", description: "" },
      token: localStorage.getItem("token") || "",
      editChapterId: null,
      editChapterForm: { name: "", description: "", questions_count: "" },
      searchQuery: ""
    };
  },
  computed: {
    filteredSubjects() {
      if (!this.searchQuery.trim()) return this.subjects;
      const q = this.searchQuery.trim().toLowerCase();
      return this.subjects.filter(
        s =>
          (s.name && s.name.toLowerCase().includes(q)) ||
          (s.description && s.description.toLowerCase().includes(q))
      );
    }
  },
  mounted() {
    this.fetchSubjects();
    this.fetchChapters();
  },
  methods: {
    fetchSubjects() {
      this.loading = true;
      axios
        .get("http://127.0.0.1:5000/api/subjects", {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(res => {
          this.subjects = res.data;
          this.loading = false;
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error loading subjects";
          this.loading = false;
        });
    },
    fetchChapters() {
      axios
        .get("http://127.0.0.1:5000/api/chapters", {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(res => {
          this.chapters = res.data;
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error loading chapters";
        });
    },
    chaptersForSubject(subjectId) {
      return this.chapters.filter(ch => ch.subject_id === subjectId);
    },
    startEdit(subject) {
      this.editId = subject.id;
      this.editForm = { name: subject.name, description: subject.description };
    },
    cancelEdit() {
      this.editId = null;
      this.editForm = { name: "", description: "" };
    },
    updateSubject(id) {
      axios
        .put(`http://127.0.0.1:5000/api/subjects/${id}`, 
          { name: this.editForm.name, description: this.editForm.description }, // send only relevant fields
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`
            }
          }
        )
        .then(() => {
          this.fetchSubjects();
          this.cancelEdit();
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error updating subject";
        });
    },
    deleteSubject(id) {
      if (!confirm("Are you sure you want to delete this subject?")) return;
      axios
        .delete(`http://127.0.0.1:5000/api/subjects/${id}`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(() => {
          this.fetchSubjects();
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error deleting subject";
        });
    },
    addSubject() {
      axios
        .post("http://127.0.0.1:5000/api/subjects", this.newSubject, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`
          }
        })
        .then(() => {
          this.newSubject = { name: "", description: "" };
          this.fetchSubjects();
          this.showAdd = false;
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error adding subject";
        });
    },
    openAddChapterModal(subject) {
      this.modalSubject = subject;
      this.newChapter = { name: "", description: "" };
      this.showAddChapterModal = true;
    },
    closeAddChapterModal() {
      this.showAddChapterModal = false;
      this.modalSubject = null;
      this.newChapter = { name: "", description: "" };
    },
    submitAddChapter() {
      if (!this.modalSubject) return;
      axios
        .post("http://127.0.0.1:5000/api/chapters", {
          name: this.newChapter.name,
          description: this.newChapter.description,
          subject_id: this.modalSubject.id
        }, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`
          }
        })
        .then(() => {
          this.fetchChapters();
          this.closeAddChapterModal();
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error adding chapter";
        });
    },
    startEditChapter(chapter) {
      this.editChapterId = chapter.id;
      this.editChapterForm = {
        name: chapter.name,
        description: chapter.description || "",
        questions_count: chapter.questions_count || ""
      };
    },
    cancelEditChapter() {
      this.editChapterId = null;
      this.editChapterForm = { name: "", description: "", questions_count: "" };
    },
    updateChapter(chapterId) {
      axios
        .put(`http://127.0.0.1:5000/api/chapters/${chapterId}`, {
          name: this.editChapterForm.name,
          description : this.editChapterForm.description,
          questions_count: this.editChapterForm.questions_count
        }, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`
          }
        })
        .then(() => {
          this.fetchChapters();
          this.cancelEditChapter();
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error updating chapter";
        });
    },
    deleteChapter(chapter) {
      if (!chapter || !chapter.id) return;
      if (!confirm(`Delete chapter ${chapter.name}?`)) return;
      axios
        .delete(`http://127.0.0.1:5000/api/chapters/${chapter.id}`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(() => {
          this.fetchChapters();
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error deleting chapter";
        });
    }
  }
};
</script>

<style scoped>
.subjects-admin {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 24px rgba(0,0,0,0.10);
  padding: 32px 24px;
  margin-top: 12px;
}
.subjects-list {
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
  justify-content: flex-start;
  align-items: stretch;
}
.subject-card {
  flex: 1 1 340px;
  max-width: 370px;
  min-width: 320px;
  border-radius: 18px;
  border: none;
  background: linear-gradient(135deg, #f8fbff 0%, #ffe0e0 40%, #eaf4ff 100%);
  box-shadow: 0 4px 24px rgba(79,140,255,0.12);
  transition: box-shadow 0.2s, transform 0.2s;
  backdrop-filter: blur(2px);
  overflow: hidden;
  position: relative;
}
.subject-card:nth-child(2n) {
  background: linear-gradient(135deg, #e0ffe0 0%, #eaf4ff 100%);
}
.subject-card:nth-child(3n) {
  background: linear-gradient(135deg, #e0eaff 0%, #ffe0f0 100%);
}
.subject-card:hover {
  box-shadow: 0 8px 32px rgba(79,140,255,0.18);
  transform: translateY(-2px) scale(1.02);
}
.add-chapter-btn {
  position: absolute;
  left: 50%;
  bottom: 12px;
  transform: translateX(-50%);
  background: #fff;
  border: 2px solid #4f8cff;
  color: #4f8cff;
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  box-shadow: 0 2px 8px rgba(79,140,255,0.10);
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  z-index: 3;
}
.add-chapter-btn:hover {
  background: #4f8cff;
  color: #fff;
  border-color: #4f8cff;
}
.add-chapter-modal {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 2000;
  width: 340px;
  max-width: 90vw;
}
.chapter-table-wrap {
  background: rgba(255,255,255,0.7);
  border-radius: 10px;
  box-shadow: 0 1px 8px rgba(79,140,255,0.07);
  padding: 8px;
  margin-bottom: 8px;
}
.chapter-table {
  margin-bottom: 0;
  border-radius: 6px;
  border-collapse: collapse;
}
.chapter-table th, .chapter-table td {
  vertical-align: middle;
  text-align: center;
  font-size: 0.89rem;
  padding: 2px 6px;
  border: 1px solid #e3e6f0;
}
.chapter-table th {
  background: #eaf4ff;
  font-weight: 600;
  border-top: none;
  padding: 4px 6px;
}
.chapter-table td {
  background: #fff;
  border-top: none;
  padding: 2px 6px;
}
.chapter-name {
  text-align: left;
  font-weight: 500;
  color: #2d3a4a;
}
.chapter-description {
  margin: 0;
  padding: 0;
  font-size: 0.80rem;
  color: #6c757d;
}
.card-body {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  padding: 22px 18px 10px 18px;
  flex: 1 1 auto;
  position: relative;
}
.card-header-actions {
  position: absolute;
  top: 18px;
  right: 18px;
  display: flex;
  gap: 8px;
  z-index: 2;
}
.d-flex.align-items-center.mb-2 {
  margin-bottom: 16px !important;
  align-items: center;
  gap: 10px;
}
.subject-avatar {
  width: 44px;
  height: 44px;
  font-size: 1.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #4f8cff 0%, #6dd5ed 100%);
  box-shadow: 0 2px 8px rgba(79,140,255,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
}
.gradient-bg {
  background: linear-gradient(135deg, #4f8cff 0%, #6dd5ed 100%);
}
.card-title {
  font-size: 1.13rem;
  font-weight: 600;
  margin-bottom: 0;
  line-height: 1.2;
  flex: 1 1 auto;
  text-align: left;
  padding-right: 70px; /* space for buttons */
}
.card-text {
  font-size: 0.97rem;
  margin-bottom: 0.5rem;
  text-align: left;
  min-height: 36px;
  flex: 1 1 auto;
}
.d-flex.gap-2.mt-2 {
  margin-top: 10px !important;
  gap: 8px;
  justify-content: flex-end;
}
.card-footer {
  background: none;
  border: none;
  text-align: right;
  padding: 8px 18px 8px 18px;
}



.badge.bg-gradient {
  background: linear-gradient(90deg, #4f8cff 0%, #6dd5ed 100%);
  font-size: 0.93rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(79,140,255,0.08);
}
.badge-index {
  background: linear-gradient(90deg, #ff7e5f 0%, #feb47b 100%);
  color: #222;
  font-size: 1.05rem;
  font-weight: 600;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(255,126,95,0.12);
  padding: 6px 18px;
  letter-spacing: 1px;
  border: 1px solid #feb47b;
  display: inline-block;
}
.btn {
  font-size: 0.89rem;
  padding: 2px 8px;
}
.btn i {
  margin-right: 2px;
}
.glass-card {
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(8px);
  border: none;
  box-shadow: 0 2px 16px rgba(0,0,0,0.10);
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

</style>
