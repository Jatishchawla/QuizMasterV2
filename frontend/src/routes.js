import { createWebHistory , createRouter } from "vue-router";
import AdminDashboard from "./components/AdminDashboard.vue";
import LoginPage from "./components/LoginPage.vue";
import Content from "./components/Content.vue"
import SubjectsAdmin from "./components/SubjectsAdmin.vue";
import AdminLayout from "./components/AdminLayout.vue";
import QuizManagement from "./components/QuizManagement.vue";
// import RegisterPage from "./components/RegisterPage.vue";
import UserDashboard from "./components/UserDashboard.vue";
import UserLayout from "./components/UserLayout.vue";
import QuizInterface from "./components/QuizInterface.vue";
import QuizHistory from "./components/QuizHistory.vue";
import UserAnalytics from "./components/UserAnalytics.vue";
import UserProfile from "./components/UserProfile.vue";
import ChapterAdmin from "./components/ChapterAdmin.vue";
import UserManagement from "./components/UserManagement.vue";
import AdminAnalytics from "./components/AdminAnalytics.vue";

const routes = [
  { path: "/", component: Content }, 
  { path: "/login", component: LoginPage },
  // { path: "/register", component: RegisterPage },
  { 
    path: "/admin", 
    component: AdminLayout,
    children: [
      { path: "dashboard", component: AdminDashboard }, // /admin/dashboard also shows dashboard
      { path: "subjects", component: SubjectsAdmin },
      { path: "quiz", component: QuizManagement },
      { path: "chapters", component: ChapterAdmin },
      { path: "users", component: UserManagement },
      { path: "analytics", component: AdminAnalytics }
    ]
  },
  
  { path: "/user", component: UserLayout,
    children: [
      { path: "dashboard", component: UserDashboard },
      { path: "quiz/:quizId", component: QuizInterface },
      { path: "results" , component: QuizHistory },
      { path: "results/:scoreId", component: QuizHistory },
      { path: "analytics", component: UserAnalytics },
      { path: "profile", component: UserProfile }
    ]
  },

];
export const router = createRouter({
    history: createWebHistory(),
    routes
})

// export default router

// this.$router.go(-1)