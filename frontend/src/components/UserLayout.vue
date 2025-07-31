<script>
import SidebarUser from './SidebarUser.vue';
export default {
  name: "UserLayout",
  components: { SidebarUser },
  data() {
    return {
      isCollapsed: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    }
  }
};
</script>

<template>
  <div class="user-dashboard" :class="{ 'sidebar-collapsed': isCollapsed }">
    <SidebarUser
      :is-collapsed="isCollapsed"
      @toggleSidebar="toggleSidebar"
    />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.user-dashboard {
  display: flex;
  min-height: 100vh;
  background: #f4f6fb;
  transition: all 0.3s;
}
.main-content {
  flex: 1;
  padding-left: 260px;
  transition: padding-left 0.3s;
}
.user-dashboard.sidebar-collapsed .main-content {
  padding-left: 70px;
}
</style>