<script>
import SidebarAdmin from './SidebarAdmin.vue'
export default {
  name: "AdminLayout",
  components: { SidebarAdmin },
  data() {
    return {
      isCollapsed: false,
      isCategoryOpen: false, // collapsed by default
    };
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
      if (this.isCollapsed) this.isCategoryOpen = false;
    },
    toggleCategory() {
      this.isCategoryOpen = !this.isCategoryOpen;
    }
  }
};
</script>

<template>
  <div class="admin-dashboard" :class="{ 'sidebar-collapsed': isCollapsed }">
    <SidebarAdmin
      :is-collapsed="isCollapsed"
      :is-category-open="isCategoryOpen"
      @toggleSidebar="toggleSidebar"
      @toggleCategory="toggleCategory"
    />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
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
.admin-dashboard.sidebar-collapsed .main-content {
  padding-left: 70px;
}
</style>
