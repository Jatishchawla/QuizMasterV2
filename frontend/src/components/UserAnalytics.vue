<template>
  <div class="user-analytics">
    <div class="py-4 container-fluid">
      <!-- Analytics Header -->
      <div class="mb-4 row">
        <div class="col-12">
          <div class="analytics-header">
            <h2 class="mb-2 fw-bold">
              <i class="me-3 text-primary fas fa-chart-line"></i>
              Performance Analytics
            </h2>
            <p class="text-muted">Detailed insights into your learning progress and performance trends</p>
          </div>
        </div>
      </div>

      <!-- Key Metrics -->
      <div class="mb-4 row">
        <div class="mb-3 col-lg-3 col-md-6">
          <div class="border-0 h-100 metric-card card">
            <div class="text-center card-body">
              <div class="mb-3 metric-icon">
                <div class="bg-primary icon-circle">
                  <i class="text-white fas fa-graduation-cap fa-2x"></i>
                </div>
              </div>
              <h3 class="text-primary fw-bold">{{ analytics.totalQuizzes }}</h3>
              <p class="mb-2 text-muted">Total Quizzes</p>
              <small class="text-success">
                <i class="me-1 fas fa-arrow-up"></i>
                +{{ analytics.quizzesThisMonth }} this month
              </small>
            </div>
          </div>
        </div>


        <div class="mb-3 col-lg-3 col-md-6">
          <div class="border-0 h-100 metric-card card">
            <div class="text-center card-body">
              <div class="mb-3 metric-icon">
                <div class="bg-info icon-circle">
                  <i class="text-white fas fa-clock fa-2x"></i>
                </div>
              </div>
              <h3 class="text-info fw-bold">{{ analytics.totalStudyTime }}</h3>
              <p class="mb-2 text-muted">Study Time</p>
              <small class="text-info">
                <i class="me-1 fas fa-clock"></i>
                {{ analytics.avgSessionTime }} avg/session
              </small>
            </div>
          </div>
        </div>

        <div class="mb-3 col-lg-3 col-md-6">
          <div class="border-0 h-100 metric-card card">
            <div class="text-center card-body">
              <div class="mb-3 metric-icon">
                <div class="bg-warning icon-circle">
                  <i class="text-white fas fa-medal fa-2x"></i>
                </div>
              </div>
              <h3 class="text-warning fw-bold">#{{ analytics.globalRank }}</h3>
              <p class="mb-2 text-muted">Global Rank</p>
              <small class="text-success">
                <i class="me-1 fas fa-arrow-up"></i>
                Top {{ analytics.percentile }}%
              </small>
            </div>
          </div>
        </div>
      </div>

      <!-- Achievements & Goals -->
      <div class="row">
        <div class="mb-4 col-lg-6">
          <div class="border-0 card">
            <div class="bg-white pb-0 border-0 card-header">
              <h5 class="mb-0 fw-bold">Recent Achievements</h5>
            </div>
            <div class="card-body">
              <div class="achievements-list">
                <div 
                  v-for="achievement in achievements" 
                  :key="achievement.id"
                  class="d-flex align-items-center mb-3 achievement-item"
                >
                  <div class="me-3 achievement-icon">
                    <div class="icon-badge" :style="`background: ${achievement.color}`">
                      <i :class="achievement.icon" class="text-white"></i>
                    </div>
                  </div>
                  <div class="flex-grow-1 achievement-info">
                    <h6 class="mb-1">{{ achievement.title }}</h6>
                    <small class="text-muted">{{ achievement.description }}</small>
                  </div>
                  <div class="achievement-date">
                    <small class="text-muted">{{ achievement.date }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mb-4 col-lg-6">
          <div class="border-0 card">
            <div class="bg-white pb-0 border-0 card-header">
              <h5 class="mb-0 fw-bold">Learning Goals</h5>
            </div>
            <div class="card-body">
              <div class="goals-list">
                <div 
                  v-for="goal in learningGoals" 
                  :key="goal.id"
                  class="mb-4 goal-item"
                >
                  <div class="d-flex align-items-center justify-content-between mb-2">
                    <h6 class="mb-0">{{ goal.title }}</h6>
                    <span class="bg-light text-dark badge">{{ goal.progress }}%</span>
                  </div>
                  <div class="mb-2 progress" style="height: 8px;">
                    <div 
                      class="bg-primary progress-bar" 
                      :style="`width: ${goal.progress}%`"
                    ></div>
                  </div>
                  <div class="d-flex justify-content-between">
                    <small class="text-muted">{{ goal.description }}</small>
                    <small class="text-muted">{{ goal.deadline }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- Performance Trends -->
        <div class="mb-4 col-lg-8">
          <div class="border-0 card">
            <div class="bg-white pb-0 border-0 card-header">
              <div class="d-flex align-items-center justify-content-between">
                <h5 class="mb-0 fw-bold">Performance Trends</h5>
              </div>
            </div>
            <div class="card-body">
              <div class="row">
                <!-- Subjectwise Number of Quizzes Done -->
                <div class="mb-4 col-md-6">
                  <h6 class="mb-3 fw-bold">Quizzes Attempted per Subject</h6>
                  <canvas id="subjectQuizzesChart" height="220"></canvas>
                </div>
                <!-- Monthwise Number of Quizzes Attempted -->
                <div class="mb-4 col-md-6">
                  <h6 class="mb-3 fw-bold">Quizzes Attempted per Month</h6>
                  <canvas id="monthQuizzesChart" height="220"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </div>
      


      <div class="row">
        <!-- Difficulty Analysis -->
        <div class="mb-4 col-lg-6">
          <div class="border-0 card">
            <div class="bg-white pb-0 border-0 card-header">
              <h5 class="mb-0 fw-bold">Performance by Difficulty</h5>
            </div>
            <div class="card-body">
              <div class="difficulty-chart">
                <canvas id="difficultyChart" width="400" height="300"></canvas>
              </div>
              <div class="mt-3 difficulty-stats">
                <div class="text-center row">
                  <div class="col-4">
                    <div class="difficulty-stat">
                      <h5 class="text-success fw-bold">{{ difficultyStats.easy.score }}%</h5>
                      <small class="text-muted">Easy Questions</small>
                      <div class="text-success small">{{ difficultyStats.easy.count }} attempted</div>
                    </div>
                  </div>
                  <div class="col-4">
                    <div class="difficulty-stat">
                      <h5 class="text-warning fw-bold">{{ difficultyStats.medium.score }}%</h5>
                      <small class="text-muted">Medium Questions</small>
                      <div class="text-warning small">{{ difficultyStats.medium.count }} attempted</div>
                    </div>
                  </div>
                  <div class="col-4">
                    <div class="difficulty-stat">
                      <h5 class="text-danger fw-bold">{{ difficultyStats.hard.score }}%</h5>
                      <small class="text-muted">Hard Questions</small>
                      <div class="text-danger small">{{ difficultyStats.hard.count }} attempted</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Time Analysis -->
        
      </div>

      
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from 'chart.js/auto';

export default {
  name: 'UserAnalytics',
  data() {
    return {
      analytics: {
        totalQuizzes: 0,
        quizzesThisMonth: 0,
        totalStudyTime: '0h',
        avgSessionTime: '0m',
        globalRank: '--',
        percentile: 0
      },
      difficultyStats: {
        easy: { score: 0, count: 0 },
        medium: { score: 0, count: 0 },
        hard: { score: 0, count: 0 }
      },
      achievements: [],
      learningGoals: [],
      subjectQuizCounts: [],
      subjectLabels: [],
      subjectCounts: [],
      subjectChart: null,
      monthLabels: [],
      monthCounts: [],
      monthChart: null
    }
  },
  async mounted() {
    await this.fetchAnalyticsData();
    this.initCharts();
    this.initSubjectQuizzesChart();
  },
  methods: {
    async fetchAnalyticsData() {
      const token = localStorage.getItem("token") || "";
      let scores = [];
      let quizzes = [];
      try {
        const scoresRes = await axios.get("http://127.0.0.1:5000/api/scores", {
          headers: { Authorization: `Bearer ${token}` }
        });
        scores = Array.isArray(scoresRes.data) ? scoresRes.data : [];
        const quizzesRes = await axios.get("http://127.0.0.1:5000/api/quizzes", {
          headers: { Authorization: `Bearer ${token}` }
        });
        quizzes = Array.isArray(quizzesRes.data) ? quizzesRes.data : [];
      } catch (err) {}
      // Total quizzes attempted
      this.analytics.totalQuizzes = scores.length;
      // Quizzes this month
      const now = new Date();
      this.analytics.quizzesThisMonth = scores.filter(s => {
        const d = new Date(s.time_stamp_of_attempt);
        return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
      }).length;
      // Study time (dummy: count quizzes * 20min)
      this.analytics.totalStudyTime = `${scores.length * 20}m`;
      this.analytics.avgSessionTime = '20m';
      // Global rank/percentile (dummy, backend should provide)
      this.analytics.globalRank = '--';
      this.analytics.percentile = 0;
      // --- Difficulty Stats ---
      let easyScores = [], mediumScores = [], hardScores = [];
      scores.forEach(s => {
        const quiz = quizzes.find(q => q.id === s.quiz_id);
        if (!quiz) return;
        let difficulty = "Medium";
        if (quiz.time_duration) {
          const dur = parseInt(quiz.time_duration);
          if (dur <= 20) difficulty = "Easy";
          else if (dur <= 35) difficulty = "Medium";
          else difficulty = "Hard";
        }
        if (difficulty === "Easy") easyScores.push(s.total_scored || 0);
        else if (difficulty === "Medium") mediumScores.push(s.total_scored || 0);
        else hardScores.push(s.total_scored || 0);
      });
      this.difficultyStats.easy = { score: easyScores.length ? Math.round(easyScores.reduce((a, b) => a + b, 0) / easyScores.length) : 0, count: easyScores.length };
      this.difficultyStats.medium = { score: mediumScores.length ? Math.round(mediumScores.reduce((a, b) => a + b, 0) / mediumScores.length) : 0, count: mediumScores.length };
      this.difficultyStats.hard = { score: hardScores.length ? Math.round(hardScores.reduce((a, b) => a + b, 0) / hardScores.length) : 0, count: hardScores.length };
      // --- Time Insights ---
      let dates = scores.map(s => new Date(s.time_stamp_of_attempt));
      dates.sort((a, b) => a - b);
      let streak = 0, maxStreak = 0, prevDate = null;
      dates.forEach(d => {
        if (prevDate && (d - prevDate) / (1000 * 60 * 60 * 24) === 1) streak++;
        else streak = 1;
        if (streak > maxStreak) maxStreak = streak;
        prevDate = d;
      });
      // --- Achievements & Goals ---
      this.achievements = [
        {
          id: 1,
          title: 'Quiz Master',
          description: `Completed ${scores.length} quizzes`,
          icon: 'fas fa-trophy',
          color: '#f59e0b',
          date: dates.length ? this.formatRelativeDate(dates[dates.length - 1]) : ''
        }
      ];
      this.learningGoals = [
        {
          id: 1,
          title: 'Complete 20 Quizzes',
          description: 'Master fundamentals',
          progress: Math.min(100, Math.round((scores.length / 20) * 100)),
          deadline: 'Dec 31, 2024'
        }
      ];
      // --- Subject Quiz Counts for Chart.js ---
      let quizIdToSubject = {};
      quizzes.forEach(q => {
        quizIdToSubject[q.id] = q.subject_name || "Unknown";
      });
      let subjCount = {};
      scores.forEach(s => {
        const subj = quizIdToSubject[s.quiz_id] || "Unknown";
        subjCount[subj] = (subjCount[subj] || 0) + 1;
      });
      this.subjectQuizCounts = Object.entries(subjCount).map(([subject, count]) => ({ subject, count }));
      this.subjectLabels = this.subjectQuizCounts.map(x => x.subject);
      this.subjectCounts = this.subjectQuizCounts.map(x => x.count);

      // --- Monthwise Quiz Attempt Counts for Chart.js ---
      let monthCount = {};
      scores.forEach(s => {
        const d = new Date(s.time_stamp_of_attempt);
        if (!isNaN(d)) {
          const label = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
          monthCount[label] = (monthCount[label] || 0) + 1;
        }
      });
      // Sort months chronologically
      const sortedMonths = Object.keys(monthCount).sort();
      this.monthLabels = sortedMonths;
      this.monthCounts = sortedMonths.map(m => monthCount[m]);
    },
    getScoreClass(score) {
      if (score >= 90) return 'text-success'
      if (score >= 80) return 'text-primary'
      if (score >= 70) return 'text-warning'
      return 'text-danger'
    },
    getProgressClass(score) {
      if (score >= 90) return 'bg-success'
      if (score >= 80) return 'bg-primary'
      if (score >= 70) return 'bg-warning'
      return 'bg-danger'
    },
    formatRelativeDate(date) {
      const now = new Date();
      const diffMs = now - date;
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
      if (diffDays === 0) return "Today";
      if (diffDays === 1) return "Yesterday";
      if (diffDays < 7) return `${diffDays} days ago`;
      if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
      return `${Math.ceil(diffDays / 30)} months ago`;
    },
    initCharts() {
      this.initPerformanceTrendChart()
      this.initDifficultyChart()
      this.initTimeChart()
    },
    initPerformanceTrendChart() {
      const canvas = document.getElementById('performanceTrendChart')
      if (canvas) {
        const ctx = canvas.getContext('2d')
        
        // Sample data
        const data = [75, 78, 82, 79, 85, 88, 87, 90, 89, 92, 87, 89]
        const labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        const padding = 50
        const chartWidth = canvas.width - 2 * padding
        const chartHeight = canvas.height - 2 * padding
        
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        
        // Draw grid lines
        ctx.strokeStyle = '#f1f5f9'
        ctx.lineWidth = 1
        
        // Horizontal grid lines
        for (let i = 0; i <= 5; i++) {
          const y = padding + (i * chartHeight) / 5
          ctx.beginPath()
          ctx.moveTo(padding, y)
          ctx.lineTo(canvas.width - padding, y)
          ctx.stroke()
        }
        
        // Draw line chart
        ctx.strokeStyle = '#3b82f6'
        ctx.lineWidth = 3
        ctx.beginPath()
        
        data.forEach((point, index) => {
          const x = padding + (index * chartWidth) / (data.length - 1)
          const y = canvas.height - padding - ((point - 60) / 40) * chartHeight
          
          if (index === 0) {
            ctx.moveTo(x, y)
          } else {
            ctx.lineTo(x, y)
          }
        })
        
        ctx.stroke()
        
        // Draw points
        ctx.fillStyle = '#3b82f6'
        data.forEach((point, index) => {
          const x = padding + (index * chartWidth) / (data.length - 1)
          const y = canvas.height - padding - ((point - 60) / 40) * chartHeight
          
          ctx.beginPath()
          ctx.arc(x, y, 4, 0, 2 * Math.PI)
          ctx.fill()
        })
        
        // Draw labels
        ctx.fillStyle = '#64748b'
        ctx.font = '12px Arial'
        ctx.textAlign = 'center'
        
        labels.forEach((label, index) => {
          const x = padding + (index * chartWidth) / (labels.length - 1)
          ctx.fillText(label, x, canvas.height - 20)
        })
      }
    },
    
    initDifficultyChart() {
      const canvas = document.getElementById('difficultyChart')
      if (canvas) {
        const ctx = canvas.getContext('2d')
        const centerX = canvas.width / 2
        const centerY = canvas.height / 2
        const radius = 80
        
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        
        const data = [
          { label: 'Easy', value: this.difficultyStats.easy.score, color: '#10b981' },
          { label: 'Medium', value: this.difficultyStats.medium.score, color: '#f59e0b' },
          { label: 'Hard', value: this.difficultyStats.hard.score, color: '#ef4444' }
        ]
        
        const total = data.reduce((sum, item) => sum + item.value, 0)
        let currentAngle = -Math.PI / 2
        
        data.forEach(item => {
          const sliceAngle = (item.value / total) * 2 * Math.PI
          
          ctx.beginPath()
          ctx.moveTo(centerX, centerY)
          ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle)
          ctx.closePath()
          ctx.fillStyle = item.color
          ctx.fill()
          
          currentAngle += sliceAngle
        })
      }
    },
    
    initTimeChart() {
      const canvas = document.getElementById('timeChart')
      if (canvas) {
        const ctx = canvas.getContext('2d')
        
        // Sample hourly study data
        const hours = ['6AM', '9AM', '12PM', '3PM', '6PM', '9PM']
        const studyTime = [20, 45, 30, 60, 35, 25]
        
        const padding = 40
        const chartWidth = canvas.width - 2 * padding
        const chartHeight = canvas.height - 2 * padding
        const barWidth = chartWidth / hours.length * 0.6
        
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        
        const maxTime = Math.max(...studyTime)
        
        studyTime.forEach((time, index) => {
          const x = padding + (index * chartWidth) / hours.length + (chartWidth / hours.length - barWidth) / 2
          const barHeight = (time / maxTime) * chartHeight
          const y = canvas.height - padding - barHeight
          
          ctx.fillStyle = '#3b82f6'
          ctx.fillRect(x, y, barWidth, barHeight)
          
          // Draw labels
          ctx.fillStyle = '#64748b'
          ctx.font = '12px Arial'
          ctx.textAlign = 'center'
          ctx.fillText(hours[index], x + barWidth / 2, canvas.height - 10)
          
          // Draw values
          ctx.fillStyle = '#1f2937'
          ctx.fillText(`${time}m`, x + barWidth / 2, y - 5)
        })
      }
    },
    initSubjectQuizzesChart() {
      this.$nextTick(() => {
        if (this.subjectChart) {
          this.subjectChart.destroy();
        }
        const ctx = document.getElementById('subjectQuizzesChart');
        if (ctx && this.subjectLabels.length) {
          this.subjectChart = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: this.subjectLabels,
              datasets: [{
                label: 'Quizzes Attempted',
                data: this.subjectCounts,
                backgroundColor: '#2563eb',
                barThickness: 30,
                maxBarThickness: 35,
                minBarLength: 1
              }]
            },
            options: {
              responsive: true,
              plugins: {
                legend: { display: false },
                title: { display: false }
              },
              scales: {
                x: {
                  title: { display: true, text: 'Subject' },
                  categoryPercentage: 0.4,
                  barPercentage: 0.5
                },
                y: {
                  beginAtZero: true,
                  title: { display: true, text: 'Number of Quizzes' },
                  ticks: { stepSize: 1, maxTicksLimit: 5 },
                  max: Math.max(...this.subjectCounts, 1) + 1
                }
              }
            }
          });
        }
        // Also initialize month chart after subject chart
        this.initMonthQuizzesChart();
      });
    },
    initMonthQuizzesChart() {
      if (this.monthChart) {
        this.monthChart.destroy();
      }
      const ctx = document.getElementById('monthQuizzesChart');
      if (ctx && this.monthLabels.length) {
        this.monthChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: this.monthLabels,
            datasets: [{
              label: 'Quizzes Attempted',
              data: this.monthCounts,
              backgroundColor: '#f59e0b',
              barThickness: 30,
              maxBarThickness: 35,
              minBarLength: 1
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { display: false },
              title: { display: false }
            },
            scales: {
              x: {
                title: { display: true, text: 'Month' },
                categoryPercentage: 0.4,
                barPercentage: 0.5
              },
              y: {
                beginAtZero: true,
                title: { display: true, text: 'Number of Quizzes' },
                ticks: { stepSize: 1, maxTicksLimit: 5 },
                max: Math.max(...this.monthCounts, 1) + 1
              }
            }
          }
        });
      }
    }
  }
}
</script>

<style scoped>
.analytics-header {
  margin-bottom: 2rem;
}

.metric-card {
  transition: all 0.3s ease;
  border-radius: 1rem;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.chart-container {
  position: relative;
  height: 300px;
}

.subject-item {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border-left: 4px solid #3b82f6;
}

.difficulty-stat {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
}

.achievement-item {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  transition: all 0.2s ease;
}

.achievement-item:hover {
  background: #e2e8f0;
  transform: translateX(5px);
}

.icon-badge {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.goal-item {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border-left: 4px solid #10b981;
}

.insight-item {
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .chart-controls {
    margin-top: 1rem;
  }
  
  .metric-card {
    margin-bottom: 1rem;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .subject-item,
  .achievement-item,
  .goal-item {
    margin-bottom: 1rem;
  }
}
</style>