<!-- in this page , admin can see all users and manage them -->
<template>
  <div class="py-4 container">
    <h2 class="mb-4 fw-bold">User Management</h2>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="loading" class="py-5 text-center">
      <div class="spinner-border text-primary"></div>
    </div>
    <div v-else>
      <div class="d-flex align-items-center justify-content-between mb-3">
        <input
          v-model="searchQuery"
          class="form-control form-control-sm"
          placeholder="Search users by name, email, or role..."
          style="max-width: 300px;"
        />
        <button class="btn btn-success" @click="showAdd = !showAdd">
          <i class="bi bi-plus-circle"></i> Add User
        </button>
      </div>
      <transition name="fade">
        <div v-if="showAdd" class="mb-4 p-3 card">
          <h5 class="mb-3 fw-bold">Add New User</h5>
          <form @submit.prevent="addUser" class="row g-2">
            <div class="col-md-3">
              <input v-model="newUser.full_name" class="form-control" placeholder="Full Name" required />
            </div>
            <div class="col-md-3">
              <input v-model="newUser.email" class="form-control" placeholder="Email" type="email" required />
            </div>
            <div class="col-md-3">
              <input v-model="newUser.password" class="form-control" placeholder="Password" type="password" required />
            </div>
            <div class="col-md-2">
              <select v-model="newUser.role" class="form-select" required>
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div class="col-md-1">
              <button class="w-100 btn btn-success" type="submit">Add</button>
            </div>
          </form>
        </div>
      </transition>
      <div class="table-responsive">
        <table class="table table-bordered table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, idx) in filteredUsers" :key="user.id">
              <td>{{ idx + 1 }}</td>
              <td v-if="editId !== user.id">{{ user.full_name }}</td>
              <td v-else>
                <input v-model="editForm.full_name" class="form-control form-control-sm" />
              </td>
              <td v-if="editId !== user.id">{{ user.email }}</td>
              <td v-else>
                <input v-model="editForm.email" class="form-control form-control-sm" />
              </td>
              <td v-if="editId !== user.id">
                <span class="badge" :class="user.role === 'admin' ? 'bg-danger' : 'bg-info'">{{ user.role }}</span>
              </td>
              <td v-else>
                <select v-model="editForm.role" class="form-select-sm form-select">
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </td>
              <td>
                <template v-if="editId === user.id">
                  <button class="me-1 btn btn-success btn-sm" @click="updateUser(user.id)">
                    <i class="bi bi-check-lg"></i>
                  </button>
                  <button class="btn btn-secondary btn-sm" @click="cancelEdit">
                    <i class="bi bi-x-lg"></i>
                  </button>
                </template>
                <template v-else>
                  <button class="me-1 btn-outline-primary btn btn-sm" @click="startEdit(user)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn-outline-danger btn btn-sm" @click="deleteUser(user.id)">
                    <i class="bi bi-trash"></i>
                  </button>
                </template>
              </td>
            </tr>
            <tr v-if="filteredUsers.length === 0">
              <td colspan="5" class="text-muted text-center">No users found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "UserManagement",
  data() {
    return {
      users: [],
      loading: true,
      error: "",
      showAdd: false,
      newUser: { full_name: "", email: "", password: "", role: "user" },
      editId: null,
      editForm: { full_name: "", email: "", role: "user" },
      searchQuery: "",
      token: localStorage.getItem("token") || ""
    };
  },
  computed: {
    filteredUsers() {
      if (!this.searchQuery.trim()) return this.users;
      const q = this.searchQuery.trim().toLowerCase();
      return this.users.filter(
        u =>
          (u.full_name && u.full_name.toLowerCase().includes(q)) ||
          (u.email && u.email.toLowerCase().includes(q)) ||
          (u.role && u.role.toLowerCase().includes(q))
      );
    }
  },
  methods: {
    fetchUsers() {
      this.loading = true;
      axios
        .get("http://127.0.0.1:5000/api/users", {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(res => {
          // Map username to full_name if full_name is missing (for backward compatibility)
          this.users = res.data.map(u => ({
            ...u,
            full_name: u.full_name || u.username || ""
          }));
          this.loading = false;
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error loading users";
          this.loading = false;
        });
    },
    addUser() {
      axios
        .post("http://127.0.0.1:5000/api/users", this.newUser, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${this.token}`
          }
        })
        .then(() => {
          this.newUser = { full_name: "", email: "", password: "", role: "user" };
          this.fetchUsers();
          this.showAdd = false;
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error adding user";
        });
    },
    startEdit(user) {
      this.editId = user.id;
      this.editForm = { full_name: user.full_name, email: user.email, role: user.role };
    },
    cancelEdit() {
      this.editId = null;
      this.editForm = { full_name: "", email: "", role: "user" };
    },
    updateUser(id) {
      axios
        .put(
          `http://127.0.0.1:5000/api/users/${id}`,
          {
            full_name: this.editForm.full_name,
            email: this.editForm.email,
            role: this.editForm.role
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.token}`
            }
          }
        )
        .then(() => {
          this.fetchUsers();
          this.cancelEdit();
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error updating user";
        });
    },
    deleteUser(id) {
      if (!confirm("Are you sure you want to delete this user?")) return;
      axios
        .delete(`http://127.0.0.1:5000/api/users/${id}`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(() => {
          this.fetchUsers();
        })
        .catch(err => {
          this.error = err.response?.data?.message || "Error deleting user";
        });
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.table th, .table td {
  vertical-align: middle;
}
.badge.bg-danger {
  background: #dc3545 !important;
}
.badge.bg-info {
  background: #0dcaf0 !important;
  color: #fff;
}
</style>