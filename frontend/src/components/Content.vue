<template>
  <div class="landing-page">
    <!-- Navigation -->
    <nav class="fixed-top bg-white shadow-sm navbar navbar-expand-lg navbar-light">
      <div class="container">
        <a class="d-flex align-items-center navbar-brand fw-bold" href="#">
          <i class="me-2 text-primary fas fa-graduation-cap"></i>
          <span class="logo-text">Quiz Master</span>
        </a>
            <RouterLink class="nav-link" to="/login">
                <button class="btn btn-warning btn-md">
                  <i class="me-2 fas fa-rocket"></i>Login Now
                </button>
              </RouterLink>
      </div>
    </nav>

    <!-- Hero & Register Section -->
    <section class="bg-primary text-white hero-section">
      <div class="container">
        <div class="align-items-center row min-vh-100">
          <!-- Left: Hero -->
          <div class="col-lg-6">
            <h1 class="mb-4 display-4 fw-bold">
              Master Your Knowledge with 
              <span class="text-warning">QuizMaster</span>
            </h1>
            <p class="mb-4 lead">
              The ultimate platform for creating, taking, and managing quizzes. 
              Boost your learning with interactive assessments and real-time feedback.
            </p>
            <!-- <div class="d-flex gap-3">
              <RouterLink class="nav-link" to="/login">
                <button class="btn btn-warning btn-lg">
                  <i class="me-2 fas fa-rocket"></i>Login Now
                </button>
              </RouterLink>
            </div> -->
            <div class="mt-4">
              <div class="text-center row">
                <div class="col-4">
                  <h3 class="fw-bold">10K+</h3>
                  <small>Active Users</small>
                </div>
                <div class="col-4">
                  <h3 class="fw-bold">50K+</h3>
                  <small>Quizzes Created</small>
                </div>
                <div class="col-4">
                  <h3 class="fw-bold">99%</h3>
                  <small>Satisfaction Rate</small>
                </div>
              </div>
            </div>
          </div>
          <!-- Right: Register Form -->
          <div class="d-flex align-items-center justify-content-center col-lg-6">
            <div class="shadow-lg p-4 register-form-container card">
              <h6 class="mb-3 text-primary text-center fw-bold">
                <i class="me-2 fas fa-user-plus"></i>Register Now
              </h6>
              <form @submit.prevent="registerUser">
                <div v-if="registerSuccess" class="text-center alert alert-success">{{ registerSuccess }}</div>
                <div v-if="registerError" class="text-center alert alert-danger">{{ registerError }}</div>
                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Full Name</label>
                      <input v-model="registerForm.full_name" class="form-control" placeholder="Enter your full name" />
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Email</label>
                      <input v-model="registerForm.email" type="email" class="form-control" placeholder="Enter your email" required />
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Username</label>
                      <input v-model="registerForm.username" class="form-control" placeholder="Choose a username" required />
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Password</label>
                      <input v-model="registerForm.password" type="password" class="form-control" placeholder="Create a password" required />
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Qualification</label>
                      <input v-model="registerForm.qualification" class="form-control" placeholder="Your qualification (optional)" />
                    </div>
                    <div class="mb-3">
                      <label class="form-label">Date of Birth</label>
                      <input v-model="registerForm.dob" type="date" class="form-control" />
                    </div>
                  </div>
                </div>
                <button class="w-100 btn btn-primary" type="submit" :disabled="registerLoading">
                  <span v-if="registerLoading" class="me-2 spinner-border spinner-border-sm"></span>
                  Register
                </button>
                <div class="mt-3 text-center">
                  <span class="text-muted">Already have an account?</span>
                  <RouterLink to="/login" class="ms-1 text-primary text-decoration-none fw-semibold">Login</RouterLink>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-5">
      <div class="container">
        <div class="mb-5 text-center">
          <h2 class="display-5 fw-bold">Powerful Features</h2>
          <p class="text-muted lead">Everything you need to create and manage quizzes effectively</p>
        </div>
        <div class="row">
          <div class="mb-4 col-md-4" v-for="feature in features" :key="feature.id">
            <div class="shadow-sm border-0 h-100 card">
              <div class="p-4 text-center card-body">
                <div class="mb-3 feature-icon">
                  <i :class="feature.icon" class="text-primary fa-3x"></i>
                </div>
                <h5 class="card-title">{{ feature.title }}</h5>
                <p class="text-muted card-text">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-dark py-5 text-white">
      <div class="container">
        <div class="row">
          <div class="mb-4 col-md-4">
            <h5 class="fw-bold">
              <i class="me-2 fas fa-graduation-cap"></i>QuizMaster
            </h5>
            <p class="text-muted">
              Empowering learners worldwide with interactive quizzes and assessments.
            </p>
            <div class="social-links">
              <a href="#" class="me-3 text-white"><i class="fab fa-facebook fa-lg"></i></a>
              <a href="#" class="me-3 text-white"><i class="fab fa-twitter fa-lg"></i></a>
              <a href="#" class="me-3 text-white"><i class="fab fa-linkedin fa-lg"></i></a>
              <a href="#" class="text-white"><i class="fab fa-instagram fa-lg"></i></a>
            </div>
          </div>
          
          <div class="mb-4 col-md-2">
            <h6 class="fw-bold">Product</h6>
            <ul class="list-unstyled">
              <li><a href="#" class="text-white text-decoration-none">Features</a></li>
              <li><a href="#" class="text-white text-decoration-none">Pricing</a></li>
              <li><a href="#" class="text-white text-decoration-none">API</a></li>
              <li><a href="#" class="text-white text-decoration-none">Integrations</a></li>
            </ul>
          </div>
          
          <div class="mb-4 col-md-2">
            <h6 class="fw-bold">Company</h6>
            <ul class="list-unstyled">
              <li><a href="#" class="text-white text-decoration-none">About</a></li>
              <li><a href="#" class="text-white text-decoration-none">Blog</a></li>
              <li><a href="#" class="text-white text-decoration-none">Careers</a></li>
              <li><a href="#" class="text-white text-decoration-none">Contact</a></li>
            </ul>
          </div>
          
          <div class="mb-4 col-md-2">
            <h6 class="fw-bold">Support</h6>
            <ul class="list-unstyled">
              <li><a href="#" class="text-white text-decoration-none">Help Center</a></li>
              <li><a href="#" class="text-white text-decoration-none">Documentation</a></li>
              <li><a href="#" class="text-white text-decoration-none">Status</a></li>
              <li><a href="#" class="text-white text-decoration-none">Community</a></li>
            </ul>
          </div>
          
          <div class="mb-4 col-md-2">
            <h6 class="fw-bold">Legal</h6>
            <ul class="list-unstyled">
              <li><a href="#" class="text-white text-decoration-none">Privacy</a></li>
              <li><a href="#" class="text-white text-decoration-none">Terms</a></li>
              <li><a href="#" class="text-white text-decoration-none">Security</a></li>
              <li><a href="#" class="text-white text-decoration-none">Cookies</a></li>
            </ul>
          </div>
        </div>
        
        <hr class="my-4">
        
        <div class="align-items-center row">
          <div class="col-md-6">
            <p class="mb-0 text-muted">&copy; 2024 QuizMaster. All rights reserved.</p>
          </div>
          <div class="text-end col-md-6">
            <p class="mb-0 text-muted">Made with ❤️ for learners everywhere</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const features = ref([
  {
    id: 1,
    icon: 'fas fa-bolt',
    title: 'Lightning Fast',
    description: 'Create and deploy quizzes in minutes with our intuitive interface'
  },
  {
    id: 2,
    icon: 'fas fa-chart-line',
    title: 'Advanced Analytics',
    description: 'Track performance with detailed insights and progress reports'
  },
  {
    id: 3,
    icon: 'fas fa-mobile-alt',
    title: 'Mobile Friendly',
    description: 'Take quizzes anywhere with our responsive mobile design'
  },
  {
    id: 4,
    icon: 'fas fa-users',
    title: 'Team Collaboration',
    description: 'Work together with your team to create better assessments'
  },
  {
    id: 5,
    icon: 'fas fa-shield-alt',
    title: 'Secure & Reliable',
    description: 'Enterprise-grade security to protect your data and privacy'
  },
  {
    id: 6,
    icon: 'fas fa-cogs',
    title: 'Customizable',
    description: 'Tailor quizzes to your needs with flexible question types'
  }
])

const registerForm = ref({
  full_name: '',
  email: '',
  username: '',
  password: '',
  qualification: '',
  dob: ''
})
const registerLoading = ref(false)
const registerError = ref('')
const registerSuccess = ref('')

const registerUser = async () => {
  registerError.value = ''
  registerSuccess.value = ''
  registerLoading.value = true
  try {
    const payload = {
      email: registerForm.value.email,
      username: registerForm.value.username,
      password: registerForm.value.password,
      full_name: registerForm.value.full_name,
      qualification: registerForm.value.qualification,
      dob: registerForm.value.dob
    }
    const res = await axios.post('http://127.0.0.1:5000/api/register', payload, {
      headers: { 'Content-Type': 'application/json' }
    })
    registerSuccess.value = res.data.message || 'Registration successful! Please login.'
    registerForm.value = {
      full_name: '',
      email: '',
      username: '',
      password: '',
      qualification: '',
      dob: ''
    }
  } catch (err) {
    registerError.value = err.response?.data?.message || 'Registration failed. Please try again.'
  }
  registerLoading.value = false
}
</script>

<style scoped>
/* Navbar logo */
.navbar {
  min-height: 64px;
}
.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #2563eb;
}
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-top: 80px;
  padding-bottom: 40px;
}
.register-form-container {
  background: #fff;
  border-radius: 1.25rem;
  box-shadow: 0 8px 32px rgba(79,140,255,0.13);
  min-width: 340px;
  max-width: 420px;
  width: 100%;
  margin: 0 auto;
}
.register-form-container h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #2563eb;
}
.form-label {
  font-weight: 600;
  color: #374151;
}
.btn-primary {
  background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
  border: none;
}
.btn-primary:disabled {
  background: #bcd0fa;
}
.card {
  border-radius: 1.25rem;
}
@media (max-width: 991px) {
  .hero-section .row {
    flex-direction: column;
  }
  .register-form-container {
    margin-top: 32px;
    margin-bottom: 32px;
  }
}
.feature-icon {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.card {
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: translateY(-5px);
}
.social-links a {
  transition: color 0.2s ease;
}
.social-links a:hover {
  color: #007bff !important;
}
.navbar-brand {
  font-size: 1.5rem;
}
.hero-image img {
  max-width: 100%;
  height: auto;
}
</style>