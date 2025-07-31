<template>
  <div class="py-5 container">
    <div class="justify-content-center row">
      <div class="col-md-7">
        <div class="p-4 card">
          <div class="d-flex align-items-center mb-4">
            <h3 class="mb-1 fw-bold">{{ user.full_name }}</h3>
            <button class="ms-auto btn-outline-primary btn" @click="editMode = true">
              <i class="me-2 fas fa-edit"></i>Edit
            </button>
          </div>
          <div v-if="!editMode">
            <dl class="mb-0 row">
              <dt class="col-sm-4">Username</dt>
              <dd class="col-sm-8">{{ user.username }}</dd>
              <dt class="col-sm-4">Email</dt>
              <dd class="col-sm-8">{{ user.email }}</dd>
              <dt class="col-sm-4">Qualification</dt>
              <dd class="col-sm-8">{{ user.qualification || '-' }}</dd>
              <dt class="col-sm-4">Date of Birth</dt>
              <dd class="col-sm-8">{{ formatDate(user.dob) }}</dd>
              <dt class="col-sm-4">Member Since</dt>
              <dd class="col-sm-8">{{ formatDate(user.created_at) }}</dd>
            </dl>
          </div>
          <div v-else>
            <form @submit.prevent="saveProfile">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input v-model="editForm.full_name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="editForm.email" class="form-control" type="email" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input v-model="editForm.username" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Qualification</label>
                <input v-model="editForm.qualification" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label">Date of Birth</label>
                <input v-model="editForm.dob" class="form-control" type="date" />
              </div>
              <div class="d-flex gap-2">
                <button class="btn btn-primary" type="submit">Save</button>
                <button class="btn btn-secondary" type="button" @click="editMode = false">Cancel</button>
              </div>
            </form>
          </div>
          <div v-if="successMsg" class="mt-3 alert alert-success">{{ successMsg }}</div>
          <div v-if="errorMsg" class="mt-3 alert alert-danger">{{ errorMsg }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "UserProfile",
  data() {
    return {
      user: {
        id: null,
        full_name: "",
        email: "",
        username: "",
        qualification: "",
        dob: "",
        created_at: ""
      },
      editMode: false,
      editForm: {
        full_name: "",
        email: "",
        username: "",
        qualification: "",
        dob: ""
      },
      successMsg: "",
      errorMsg: "",
      token: localStorage.getItem("token") || ""
    };
  },
  async mounted() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/profile", {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        this.user = {
          id: res.data.id,
          full_name: res.data.full_name || res.data.username || "",
          email: res.data.email || "",
          username: res.data.username || "",
          qualification: res.data.qualification || "",
          dob: res.data.dob || "",
          created_at: res.data.created_at || ""
        };
        this.editForm = { ...this.user };
        this.errorMsg = "";
        if (
          (!this.user.full_name && !this.user.username) &&
          !this.user.email
        ) {
          this.errorMsg = "No user data found. Please check your backend /api/profile response. Make sure it returns at least username or email.";
        }
      } catch (err) {
        this.errorMsg = "Could not load profile. Please make sure you are logged in and your backend /api/profile endpoint returns user info.";
      }
    },
    async saveProfile() {
      try {
        const payload = {
          full_name: this.editForm.full_name,
          email: this.editForm.email,
          username: this.editForm.username,
          qualification: this.editForm.qualification,
          dob: this.editForm.dob
        };
        await axios.put(
          `http://127.0.0.1:5000/api/profile`,
          payload,
          { headers: { Authorization: `Bearer ${this.token}` } }
        );
        this.successMsg = "Profile updated successfully!";
        this.errorMsg = "";
        this.editMode = false;
        await this.fetchProfile();
      } catch (err) {
        this.errorMsg = err.response?.data?.message || "Update failed.";
        this.successMsg = "";
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "-";
      const d = new Date(dateStr);
      if (isNaN(d.getTime())) return "-";
      return d.toLocaleDateString();
    }
  }
};
</script>

<style scoped>
.card {
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
</style>

