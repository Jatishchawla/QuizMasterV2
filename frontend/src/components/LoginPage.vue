<template>
  <div class="login-page">
    <div class="container-fluid">
      <div class="row min-vh-100">
        <!-- Left Side - Login Form -->
        <div class="d-flex align-items-center justify-content-center col-lg-6">
          <div class="login-form-container">
            <div class="mb-5 text-center">
              <router-link to="/" class="text-decoration-none">
                <h2 class="text-primary fw-bold">
                  <i class="me-2 fas fa-graduation-cap"></i>
                  Quiz Master
                </h2>
              </router-link>
              <p class="text-muted">Welcome back! Please sign in to your account.</p>
            </div>
            <form @submit.prevent="loginUser" class="login-form">
              <p class="text-danger text-center" v-if="error">{{ error }}</p>
              <div class="mb-4">
                <label for="email" class="form-label fw-semibold">Email Address</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="text-muted fas fa-envelope"></i>
                  </span>
                  <input 
                    type="email" 
                    class="form-control" 
                    id="email"
                    v-model="formData.email"
                    placeholder="Enter your email"
                    required
                  >
                </div>
              </div>
              <div class="mb-4">
                <label for="password" class="form-label fw-semibold">Password</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="text-muted fas fa-lock"></i>
                  </span>
                  <input 
                    :type="showPassword ? 'text' : 'password'" 
                    class="form-control" 
                    id="password"
                    v-model="formData.password"
                    placeholder="Enter your password"
                    required
                  >
                  <span class="input-group-text password-toggle" @click="showPassword = !showPassword" style="cursor:pointer;">
                    <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" style="font-size:1.2rem;"></i>
                  </span>
                </div>
              </div>
              <div class="d-flex align-items-center justify-content-between mb-4">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="remember" v-model="remember">
                  <label class="form-check-label" for="remember">
                    Remember me
                  </label>
                </div>
                <a href="#" class="text-primary text-decoration-none">Forgot Password?</a>
              </div>
              <button type="submit" class="mb-4 py-3 w-100 btn btn-primary" :disabled="isLoading">
                <span v-if="isLoading" class="me-2 spinner-border spinner-border-sm"></span>
                <i v-else class="me-2 fas fa-sign-in-alt"></i>
                {{ isLoading ? 'Signing In...' : 'Sign In' }}
              </button>
              <div class="text-center">
                <p class="text-muted">
                  Don't have an account? 
                  <router-link to="/register" class="text-primary text-decoration-none fw-semibold">
                    Sign up here
                  </router-link>
                </p>
              </div>
              <hr class="my-4">
              <div class="text-center">
                <router-link to="/admin/login" class="btn-outline-secondary w-100 btn">
                  <i class="me-2 fas fa-user-shield"></i>
                  Admin Login
                </router-link>
              </div>
            </form>
          </div>
        </div>
        <!-- Right Side - Image/Illustration -->
        <div class="d-lg-flex align-items-center justify-content-center bg-primary col-lg-6 d-none">
          <div class="p-5 text-white text-center">
            <img 
              
              alt="Online Learning" 
              class="mb-4 rounded-3 img-fluid"
            >
            <h3 class="mb-3 fw-bold">Start Your Learning Journey</h3>
            <p class="lead">
              Access thousands of quizzes across multiple subjects and track your progress 
              with detailed analytics.
            </p>
            <div class="mt-4">
              <div class="text-center row">
                <div class="col-4">
                  <h4 class="fw-bold">50+</h4>
                  <small>Subjects</small>
                </div>
                <div class="col-4">
                  <h4 class="fw-bold">500+</h4>
                  <small>Quizzes</small>
                </div>
                <div class="col-4">
                  <h4 class="fw-bold">1000+</h4>
                  <small>Students</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'LoginPage',
  data() {
    return {
      formData: {
        email: '',
        password: ''
      },
      token: '',
      error: '',
      showPassword: false,
      isLoading: false,
      remember: false
    };
  },
  methods: {
    async loginUser() {
      this.isLoading = true;
      try {
        const response = await axios.post(
          'http://127.0.0.1:5000/api/login',
          this.formData,
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        this.isLoading = false;
        if(response.data.role=="admin"){
          this.$router.push('/admin/dashboard');
        }
        else{
          this.$router.push('/user/dashboard');
        }
      } catch (err) {
        this.isLoading = false;
        this.error = err.response?.data?.message || 'Login failed.';
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  background-color: #f8fafc;
}
.login-form-container {
  width: 100%;
  max-width: 450px;
  padding: 2rem;
}
.login-form {
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.input-group-text {
  background-color: #f8fafc;
  border-color: #d1d5db;
}
.password-toggle {
  background: #f8fafc;
  border-left: none;
}
.form-control {
  border-left: none;
}
.form-control:focus {
  box-shadow: none;
  border-color: #2563eb;
}
.input-group:focus-within .input-group-text {
  border-color: #2563eb;
  background-color: #eff6ff;
}
.password-toggle i {
  font-size: 1.2rem;
  color: #2563eb;
  vertical-align: middle;
  display: inline-block;
}
.input-group-text.password-toggle {
  background: #f8fafc;
  border-left: none;
  color: #2563eb;
}
.input-group-text i {
  color: #2563eb;
}
@media (max-width: 768px) {
  .login-form-container {
    padding: 1rem;
  }
  .login-form {
    padding: 2rem;
  }
}
</style>
