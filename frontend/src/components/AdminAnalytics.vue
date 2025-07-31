<template>
  <div class="py-4 container">
    <h2 class="mb-4 fw-bold">Admin Analytics</h2>
    <div v-if="loading" class="py-5 text-center">
      <div class="spinner-border text-primary"></div>
    </div>
    <div v-else>
      <!-- Top Scorers Table -->
      <div class="mt-4 row g-4">
        <div class="col-12">
          <div class="p-3 card">
            <h5 class="mb-3 fw-bold">Top Scorers for Each Quiz</h5>
            <table class="table table-bordered table-hover">
              <thead>
                <tr>
                  <th>Quiz</th>
                  <th>Subject</th>
                  <th>Top Scorer</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in quizTopScorers" :key="row.quizId">
                  <td>{{ row.quizName }}</td>
                  <td>{{ row.subjectName }}</td>
                  <td>{{ row.topScorer }}</td>
                  <td>{{ row.topScore }}</td>
                </tr>
                <tr v-if="quizTopScorers.length === 0">
                  <td colspan="4" class="text-muted text-center">No data available.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Top Scores Chart -->
      <div class="mt-4 row g-4">
        <div class="col-12">
          <div class="p-3 card">
            <h5 class="mb-3 fw-bold">Chart: Quiz Wise Top Scores</h5>
            <canvas id="quizTopScoresChart" height="100"></canvas>
          </div>
        </div>
      </div>

      <!-- All Attempts Table -->
      <div class="mt-4 row g-4">
        <div class="col-12">
          <div class="p-3 card">
            <h5 class="mb-3 fw-bold">All Quiz Attempts</h5>
            <table class="table table-bordered table-hover">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Quiz</th>
                  <th>Subject</th>
                  <th>Score</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="attempt in allAttempts" :key="attempt.id">
                  <td>{{ attempt.userName }}</td>
                  <td>{{ attempt.quizName }}</td>
                  <td>{{ attempt.subjectName }}</td>
                  <td>{{ attempt.score }}</td>
                  <td>{{ attempt.date }}</td>
                </tr>
                <tr v-if="allAttempts.length === 0">
                  <td colspan="5" class="text-muted text-center">No attempts found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Chart, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  name: "AdminAnalytics",
  data() {
    return {
      loading: true,
      subjects: [],
      chapters: [],
      quizzes: [],
      scores: [],
      users: [],
      quizTopScorers: [],
      allAttempts: [],
      token: localStorage.getItem("token") || "",
      chartInstance: null
    };
  },
  async mounted() {
    await this.fetchAllData();
    this.prepareTables();
    this.renderTopScoresChart();
    this.loading = false;
  },
  methods: {
    async fetchAllData() {
      const headers = { Authorization: `Bearer ${this.token}` };
      const [subjectsRes, chaptersRes, quizzesRes, scoresRes, usersRes] = await Promise.all([
        axios.get("http://127.0.0.1:5000/api/subjects", { headers }),
        axios.get("http://127.0.0.1:5000/api/chapters", { headers }),
        axios.get("http://127.0.0.1:5000/api/quizzes", { headers }),
        axios.get("http://127.0.0.1:5000/api/scores", { headers }),
        axios.get("http://127.0.0.1:5000/api/users", { headers })
      ]);
      this.subjects = subjectsRes.data || [];
      this.chapters = chaptersRes.data || [];
      this.quizzes = quizzesRes.data || [];
      this.scores = scoresRes.data || [];
      this.users = usersRes.data || [];
    },
    prepareTables() {
      this.quizTopScorers = this.quizzes.map(quiz => {
        const quizScores = this.scores.filter(s => s.quiz_id === quiz.id);
        let topScore = 0;
        let topUserId = null;
        quizScores.forEach(s => {
          if (s.total_scored > topScore) {
            topScore = s.total_scored;
            topUserId = s.user_id;
          }
        });
        const topUser = this.users.find(u => u.id === topUserId);
        let subj = this.subjects.find(s => s.id === quiz.subject_id);
        if (!subj && quiz.chapter_id) {
          const chapter = this.chapters.find(c => c.id === quiz.chapter_id);
          subj = chapter ? this.subjects.find(s => s.id === chapter.subject_id) : null;
        }
        return {
          quizId: quiz.id,
          quizName: quiz.name || "Quiz",
          subjectName: subj ? subj.name : "",
          topScorer: topUser ? (topUser.full_name || topUser.username || topUser.email) : "-",
          topScore: topScore
        };
      });

      this.allAttempts = this.scores.map(s => {
        const user = this.users.find(u => u.id === s.user_id);
        const quiz = this.quizzes.find(q => q.id === s.quiz_id);
        let subj = quiz ? this.subjects.find(sub => sub.id === quiz.subject_id) : null;
        if (!subj && quiz && quiz.chapter_id) {
          const chapter = this.chapters.find(c => c.id === quiz.chapter_id);
          subj = chapter ? this.subjects.find(su => su.id === chapter.subject_id) : null;
        }
        return {
          id: s.id,
          userName: user ? (user.full_name || user.username || user.email) : "-",
          quizName: quiz ? (quiz.name || "Quiz") : "-",
          subjectName: subj ? subj.name : "",
          score: s.total_scored,
          date: s.time_stamp_of_attempt ? new Date(s.time_stamp_of_attempt).toLocaleString() : ""
        };
      });
    },
    renderTopScoresChart() {
      const ctx = document.getElementById("quizTopScoresChart");
      if (!ctx) return;

      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      const labels = this.quizTopScorers.map(q => q.quizName);
      const data = this.quizTopScorers.map(q => q.topScore);

      this.chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "Top Score",
            data: data,
            backgroundColor: "rgba(54, 162, 235, 0.6)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Score"
              }
            },
            x: {
              title: {
                display: true,
                text: "Quiz"
              }
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.table th, .table td {
  vertical-align: middle;
}
</style>
