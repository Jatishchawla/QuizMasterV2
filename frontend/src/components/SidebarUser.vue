<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Header -->
    <div class="sidebar-header">
      <div class="logo-section">
        <span class="brand-name" v-if="!isCollapsed">USER</span>
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
          :class="{ active: $route.path === '/user/dashboard' }"
          to="/user/dashboard"
        >
          <i class="bi bi-house"></i>
          <span v-if="!isCollapsed">Dashboard</span>
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/user/results' }"
          to="/user/results"
        >
          <i class="bi bi-clipboard-data"></i>
          <span v-if="!isCollapsed">Results</span>
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/user/analytics' }"
          to="/user/analytics"
        >
          <i class="bi bi-bar-chart"></i>
          <span v-if="!isCollapsed">Analytics</span>
        </RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink
          class="nav-link"
          :class="{ active: $route.path === '/user/profile' }"
          to="/user/profile"
        >
          <i class="bi bi-person"></i>
          <span v-if="!isCollapsed">Profile</span>
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
  name: "SidebarUser",
  props: {
    isCollapsed: { type: Boolean, default: false }
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
  .brand-name {
    display: none !important;
  }
}
</style>
