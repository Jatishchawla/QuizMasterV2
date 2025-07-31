<script>
import axios from 'axios'
export default {
  name: "AdminDashboard",
  data() {
    return {
      role: "",
      token: "",
      dashboard: null,
      error: ""
    };
  },
  mounted() {
    this.loadToken();
    this.loadUser();
  },
  methods: {
    loadToken() {
      const token = localStorage.getItem("token");
      if (token) {
        this.token = token;
      }
    },
    loadUser() {
      axios
        .get("http://127.0.0.1:5000/api/dashboard", {
          headers: {
            "content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: `Bearer ${this.token}`,
          },
        })
        .then((res) => {
          this.dashboard = res.data;
          this.role = res.data.role;
        })
        .catch((err) => {
          this.error = err.response?.data?.message || "Error loading dashboard";
        });
    }
  }
};
</script>

<template>
  <div v-if="token">
    <div v-if="role === 'admin'">
      <div class="py-4 container-fluid">
        <h2 class="mb-4 fw-bold">Welcome, Admin!</h2>
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <div v-if="dashboard" class="row g-4">
          <div class="col-md-3">
            <div class="shadow-sm card stat-card">
              <div class="text-center card-body">
                <i class="text-primary bi bi-book fs-1"></i>
                <h5 class="mt-2 card-title">Subjects</h5>
                <p class="card-text fs-4">{{ dashboard.total_subjects || 0 }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="shadow-sm card stat-card">
              <div class="text-center card-body">
                <i class="text-success bi bi-journal fs-1"></i>
                <h5 class="mt-2 card-title">Chapters</h5>
                <p class="card-text fs-4">{{ dashboard.total_chapters || 0 }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="shadow-sm card stat-card">
              <div class="text-center card-body">
                <i class="text-warning bi bi-question-circle fs-1"></i>
                <h5 class="mt-2 card-title">Quizzes</h5>
                <p class="card-text fs-4">{{ dashboard.total_quizzes || 0 }}</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="shadow-sm card stat-card">
              <div class="text-center card-body">
                <i class="text-info bi bi-bar-chart fs-1"></i>
                <h5 class="mt-2 card-title">Quiz Attempts</h5>
                <p class="card-text fs-4">{{ dashboard.total_scores || 0 }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-5">
          <h4 class="mb-3 fw-bold">Quick Actions</h4>
          <div class="row g-3">
            <div class="col-md-4">
              <a href="/admin/subjects" class="btn-outline-primary w-100 btn">Manage Subjects</a>
            </div>
            <div class="col-md-4">
              <a href="/admin/quiz" class="btn-outline-success w-100 btn">Create Quiz</a>
            </div>
            <div class="col-md-4">
              <a href="/admin/analytics" class="btn-outline-info w-100 btn">View Analytics</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="mt-5 text-center container">
      <h2 class="text-danger">Access Denied</h2>
      <p class="text-muted">You must be logged in as an admin to view this page.</p>
      <a href="/login" class="btn btn-primary">Login</a>
    </div>
  </div>
  <div v-else class="mt-5 text-center container">
    <h2 class="text-danger">Access Denied</h2>
    <p class="text-muted">You must be logged in as an admin to view this page.</p>
    <a href="/login" class="btn btn-primary">Login</a>
  </div>
</template>

<style scoped>
.admin-dashboard {
  display: flex;
  min-height: 100vh;
  background: #f4f6fb;
  margin-top: 56px;
  transition: all 0.3s;
}
.main-content {
  flex: 1;
  padding-left: 260px;
  transition: padding-left 0.3s;
}
.admin-dashboard.sidebar-collapsed .main-content {
  padding-left: 70px;
}
</style>


