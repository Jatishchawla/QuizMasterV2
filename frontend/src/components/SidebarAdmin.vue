<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Header -->
    <div class="sidebar-header">
      <div class="logo-section">
        <span class="brand-name" v-if="!isCollapsed">ADMIN</span>
      </div>
      <button class="sidebar-toggle" @click="$emit('toggleSidebar')">
        <i :class="isCollapsed ? 'bi bi-arrow-right-square' : 'bi bi-arrow-left-square'"></i>
      </button>
    </div>

    <!-- Navigation -->
    <ul class="flex-column nav">
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/admin/dashboard' }"
          to="/admin/dashboard"
        >
          <i class="bi-grid bi"></i>
          <span v-if="!isCollapsed">Dashboard</span>
        </RouterLink>
      </li>

      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/admin/subjects' }"
          to="/admin/subjects"
        >
          <i class="bi bi-file-earmark-text"></i>
          <span v-if="!isCollapsed">Subjects</span>
        </RouterLink>
      </li>

      <!-- Chapters nav item -->
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/admin/chapters' }"
          to="/admin/chapters"
        >
          <i class="bi bi-journal"></i>
          <span v-if="!isCollapsed">Chapters</span>
        </RouterLink>
      </li>
      <!-- End Chapters nav item -->

      <!-- Quiz nav item -->
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/admin/quiz' }"
          to="/admin/quiz"
        >
          <i class="bi bi-patch-question"></i>
          <span v-if="!isCollapsed">Quiz</span>
        </RouterLink>
      </li>
      <!-- End Quiz nav item -->

      <li class="nav-item">
        <RouterLink class="nav-link" to="/admin/analytics">
          <i class="bi bi-bar-chart"></i>
          <span v-if="!isCollapsed">Analytics</span>
        </RouterLink>
      </li>

      <!-- Users nav item -->
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/admin/users' }"
          to="/admin/users"
        >
          <i class="bi bi-people"></i>
          <span v-if="!isCollapsed">Users</span>
        </RouterLink>
      </li>
      <!-- End Users nav item -->

      <li class="nav-item">
        <RouterLink class="nav-link" to="#">
          <i class="bi bi-gear"></i>
          <span v-if="!isCollapsed">Setting</span>
        </RouterLink>
      </li>
    </ul>

    <!-- Logout -->
    <div class="sidebar-logout">
      <a @click="logoutUser" class="nav-link logout-link">
        <i class="bi-box-arrow-right bi"></i>
        <span v-if="!isCollapsed">Logout</span>
      </a>
    </div>
  </aside>
</template>

<script>
export default {
  name: "SidebarAdmin",
  props: {
    isCollapsed: { type: Boolean, default: false },
    isCategoryOpen: { type: Boolean, default: false }
  },
  methods: {
    logoutUser() {
      localStorage.clear();
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
/* Sidebar layout fixed below navbar */
.sidebar {
  position: fixed;
  left: 0;
  width: 260px;
  height: 100vh;
  background: #181c24;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 2px 0 16px rgba(0, 0, 0, 0.08);
  transition: width 0.3s;
  z-index: 1040;
  overflow-x: hidden;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header {
  position: relative;
  padding: 16px 20px 12px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #23262f;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: #fff;
}

.sidebar-toggle {
  position: absolute;
  top: 8px;
  right: 12px;
  background: #23262f;
  border: 1px solid #444;
  color: #bfc9da;
  font-size: 1.5rem;
  cursor: pointer;
  border-radius: 6px;
  padding: 4px 8px;
  display: flex;
  align-items: center;
}

.sidebar-toggle:hover {
  color: #fff;
  background: #181c24;
  border-color: #666;
}

.nav {
  flex: 1 1 auto;
  padding: 16px 0 0;
}

.nav-link {
  color: #bfc9da !important;
  font-size: 1.08rem;
  padding: 12px 24px;
  border-radius: 8px;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: background 0.2s, color 0.2s, padding 0.2s;
  white-space: nowrap;
  min-height: 44px;
}

.nav-link:hover,
.nav-link.active {
  background: #23262f;
  color: #fff !important;
}

.sidebar.collapsed .nav-link {
  justify-content: center;
  padding: 12px 0;
  gap: 0;
}

.category-toggle {
  justify-content: space-between;
}

.category-list {
  padding-left: 40px;
  list-style: none;
  margin: 0;
}

.sidebar.collapsed .category-list {
  display: none;
}

.category-list .nav-link {
  padding: 8px 0 8px 16px;
  font-size: 0.95rem;
  background: none;
  margin-bottom: 0;
}

.sidebar-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #23262f;
  padding: 16px 20px;
  border-radius: 12px;
  margin: 16px;
}

.sidebar-profile-collapsed {
  display: flex;
  justify-content: center;
  background: #23262f;
  padding: 12px 0;
  border-radius: 12px;
  margin: 16px;
}

.profile-pic {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  object-fit: cover;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-name {
  font-size: 1rem;
  font-weight: 600;
}

.profile-role {
  font-size: 0.85rem;
  color: #bfc9da;
}

.sidebar-logout {
  padding: 16px;
  border-top: 1px solid #23262f;
  display: flex;
  justify-content: center;
}

.logout-link {
  color: #e74c3c !important;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.08rem;
  padding: 8px 24px;
  border-radius: 8px;
}

.logout-link:hover {
  background: #23262f;
  color: #fff !important;
}

@media (max-width: 900px) {
  .sidebar {
    width: 70px;
  }
  .sidebar.collapsed {
    width: 70px;
  }
  .brand-name,
  .category-list,
  .profile-info {
    display: none !important;
  }
}
</style>
