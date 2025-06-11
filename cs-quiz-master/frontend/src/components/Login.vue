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
      <h2 class="mb-4">Login</h2>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="username" type="text" class="form-control" id="username" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" id="password" required />
        </div>
        <button type="submit">Login</button>
        <p v-if="errorMessage">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserLogin",
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
  login() {
    this.errorMessage = "";
    const username = this.username.trim();
    const password = this.password;

    
    if (!username || !password) {
      this.errorMessage = "Please enter both username and password.";
      return;
    }
    if (username.length < 3 || username.length > 20) {
      this.errorMessage = "Username must be 3-20 characters.";
      return;
    }
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      this.errorMessage = "Username can only contain letters, numbers, and underscores.";
      return;
    }
    
    fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          localStorage.setItem('user_id', data.user_id);
          localStorage.setItem('username', data.username);
          localStorage.setItem('is_admin', data.is_admin);
          this.$router.push('/');
        } else {
          this.errorMessage = data.error || "Login failed";
        }
      });
  },
},
};
</script>