<template>
  <div>
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">CS Quiz Master</router-link>
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
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/signup">Sign Up</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-5">
      <h2 class="mb-4">Sign Up</h2>
      <form @submit.prevent="handleSignup">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="username" required />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input v-model="email" type="email" class="form-control" id="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" required />
        </div>
        <button type="submit" class="btn btn-success">Sign Up</button>
      </form>

      <p class="mt-3 text-success" v-if="successMessage">{{ successMessage }}</p>
      <p class="mt-3 text-danger" v-if="errorMessage">{{ errorMessage }}</p>

      <p class="mt-3">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserSignup",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      successMessage: "",
      errorMessage: ""
    };
  },
  methods: {
    async handleSignup() {
      const errors = [];
      const username = this.username.trim();
      const email = this.email.trim();
      const password = this.password;

      if (username.length < 3 || username.length > 20) {
        errors.push("Username must be 3-20 characters.");
      }
      if (!/^[a-zA-Z0-9_]+$/.test(username)) {
        errors.push("Username can only contain letters, numbers, and underscores.");
      }
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        errors.push("Please enter a valid email address.");
      }
      if (password.length < 8) {
        errors.push("Password must be at least 8 characters.");
      }
      if (!/\d/.test(password)) {
        errors.push("Password must contain at least one number.");
      }
      if (!/[a-zA-Z]/.test(password)) {
        errors.push("Password must contain at least one letter.");
      }
      if (/\s/.test(password)) {
        errors.push("Password cannot contain spaces.");
      }
      if (errors.length) {
        this.errorMessage = errors.join(" ");
        return;
      }
      this.errorMessage = "";

      try {
        const response = await fetch("/api/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: username,
            email: email,
            password: password,
          }),
        });
        const data = await response.json();
        if (!response.ok) {
          this.errorMessage = data.error || "Signup failed";
          return;
        }
        
        const loginRes = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: username,
            password: password,
          }),
          credentials: "include",
        });

        const loginData = await loginRes.json();
        if (loginData.success) {
          localStorage.setItem('user_id', loginData.user_id);
          localStorage.setItem('username', loginData.username);
          this.$router.push("/");
        } else {
          this.errorMessage = loginData.error || "Login after signup failed";
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = "Server error. Try again later.";
      }
    },
  },
};
</script>