<script>
export default {
  name: "NavPage",
  props: {
    signedIn: Boolean,
    roleId: { type: Number, default: 3 }, // 1=admin, 2=professional, 3=customer
    profilePic: { type: String, default: "" }
  },
  data() {
    return {
      search: "",
      trending: [
        { label: "AC Repair", value: "Ac Repair" },
        { label: "Plumbing", value: "plumbing" },
        { label: "Electrical", value: "electrical" },
        { label: "Cleaning Services", value: "cleaning" }
      ]
    };
  },
  methods: {
    submitSearch() {
      if (this.search.trim()) {
        this.$router.push(`/viewservice?query_global=${encodeURIComponent(this.search.trim())}`);
      }
    }
  }
};
</script>

<template>
  <header class="fixed-top shadow-sm backdrop-blur navbar navbar-expand-lg">
    <div class="container-fluid">
      <!-- Logo -->
      <a class="d-flex align-items-center navbar-brand" href="/">
        <img
          src="/src/assets/JC_logo(2).avif"
          alt="Logo"
          class="rounded-circle navbar-logo"
        />
      </a>

      <!-- Toggler -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar Content -->
      <div class="collapse navbar-collapse justify-content-between" id="navbarNav">
        <!-- Center Search -->
        <form @submit.prevent="submitSearch" class="position-relative d-flex mx-auto w-50">
          <input
            v-model="search"
            id="search-input"
            class="search-bar form-control"
            type="text"
            placeholder="Search..."
            required
          />
          <!-- Trending Dropdown -->
          <div class="position-absolute mt-1 dropdown-menu show" style="width: 100%;" v-if="search.length">
            <div class="dropdown-header">Trending Searches</div>
            <div class="dropdown-divider"></div>
            <a
              v-for="item in trending"
              :key="item.value"
              class="dropdown-item"
              :href="`/viewservice?query_global=${item.value}`"
            >
              {{ item.label }}
            </a>
          </div>
        </form>

        <!-- Nav Links -->
        <ul class="ms-auto me-3 navbar-nav">
          <li class="nav-item"><a class="underline-effect nav-link" href="/">Home</a></li>
          <li class="nav-item"><a class="underline-effect nav-link" href="/viewservice">Services</a></li>
          <li class="nav-item"><a class="underline-effect nav-link" href="/#footer">Support</a></li>
          <li class="nav-item"><a class="underline-effect nav-link" href="/aboutus">About</a></li>
          <li class="nav-item" v-if="signedIn"><a class="underline-effect nav-link" href="/summary">Summary</a></li>
        </ul>

        <!-- User Controls -->
        <div class="d-flex align-items-center">
          <template v-if="!signedIn">
            <a class="me-2 btn-outline-primary btn" @click="$router.push('/login')">Sign In</a>
            <a class="btn-outline-primary btn" @click="$router.push('/register')">Sign Up</a>
          </template>

          <template v-else>
            <div class="dropdown">
              <img
                :src="profilePic || '/src/assets/JC_logo(2).avif'"
                class="rounded-circle profile-pic"
                data-bs-toggle="dropdown"
                aria-expanded="false"
                alt="Profile"
              />
              <i class="ms-1 bi-caret-down-fill bi"></i>
              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <a class="dropdown-item" :href="roleId === 1 ? '/admin/dashboard' : roleId === 2 ? '/professional/dashboard' : '/customer/dashboard'">Dashboard</a>
                </li>
                <li><a class="dropdown-item" href="/user_profile">View Profile</a></li>
                <li v-if="roleId !== 1">
                  <a class="dropdown-item" :href="roleId === 2 ? '/professional/dashboard#mybookings' : '/customer/dashboard#mybookings'">My Bookings</a>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li><a class="dropdown-item" href="/signout">Sign out</a></li>
              </ul>
            </div>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 0.5rem 1rem;
}

.navbar-logo {
  height: 50px;
  width: 50px;
  object-fit: cover;
}

.profile-pic {
  height: 40px;
  width: 40px;
  object-fit: cover;
  cursor: pointer;
}

.search-bar {
  border-radius: 8px;
  padding: 6px 12px;
  border: 2px solid #ccc;
  font-size: 16px;
}

.nav-link {
  color: #000 !important;
  position: relative;
}

.nav-link.underline-effect::after {
  content: "";
  position: absolute;
  width: 0%;
  height: 2px;
  background: black;
  bottom: -2px;
  left: 0;
  transition: width 0.3s;
}

.nav-link.underline-effect:hover::after {
  width: 100%;
}
</style>
