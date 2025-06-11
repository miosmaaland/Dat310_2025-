<template>
  <main>
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark" aria-label="Main navigation">
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
              <router-link class="nav-link" to="/play">Play</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/leaderboard">Leaderboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/hangman">Hangman</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button class="nav-link btn btn-danger" @click="logout" aria-label="Logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>


    <section class="hero-section d-flex flex-column justify-content-center align-items-center text-center py-5 mb-4">
  <div class="hero-icon mb-3">
    <span style="font-size: 3rem;">👤</span>
  </div>
  <h1 class="display-5 fw-bold text-white">Your Profile</h1>
  <p class="lead text-white-50 mb-0">View your stats and achievements!</p>
</section>

    
    <section class="container mt-5 text-center">
      <div class="d-flex flex-column align-items-center mb-4">
        <img
          :src="profileImage"
          alt="Profile"
          class="rounded-circle shadow"
          style="width: 100px; height: 100px; object-fit: cover;"
        />
        <form @submit.prevent="uploadImage" class="mt-3" enctype="multipart/form-data">
          <input type="file" accept="image/*" @change="onFileChange" class="form-control mb-2" />
          <button v-if="selectedFile" class="btn btn-secondary btn-sm" type="submit">Upload Image</button>
        </form>
        <div v-if="uploadError" class="text-danger mt-2">{{ uploadError }}</div>
      </div>
      <h1>Hello, {{ username }}! 👋</h1>
      <p>Your Current Score: {{ score }}</p>
      <nav class="d-flex flex-column flex-md-row justify-content-center gap-3 mt-4">
        <router-link class="btn btn-primary" to="/play">Take More Quizzes</router-link>
        <button class="btn btn-danger" @click="logout">Logout</button>
      </nav>
      
      <div class="mt-4">
  <h3>Achievements</h3>
  <div v-if="achievements.length === 0" class="text-muted">No achievements yet.</div>
  <ul class="list-group list-group-flush d-inline-block text-start" style="max-width: 400px;">
    <li v-for="ach in achievements" :key="ach.id" class="list-group-item">
      <span class="badge bg-success me-2">🏅</span>
      <strong>{{ ach.name }}</strong>
      <div class="small text-muted">{{ ach.description }}</div>
    </li>
  </ul>
</div>
    </section>

    
    <button
      v-show="showBackToTop"
      @click="scrollToTop"
      class="btn btn-primary position-fixed"
      style="bottom: 30px; right: 30px; z-index: 1000;"
      aria-label="Back to top"
    >
      ↑ Top
    </button>
  </main>
</template>

<script>
export default {
  name: "UserProfile",
  data() {
    return {
      username: localStorage.getItem('username') || 'Guest',
      score: 0,
      profileImage: "/default.jpg",
      showBackToTop: false,
      selectedFile: null,
      uploadError: "",
      achievements: [],
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    }
  },
  methods: {
    logout() {
      fetch('/api/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
        .then((res) => res.json())
        .then(() => {
          localStorage.removeItem('user_id');
          localStorage.removeItem('username');
          this.$router.push('/');
        })
        .catch(() => {
          alert('Logout failed. Please try again.');
        });
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    handleScroll() {
      this.showBackToTop = window.scrollY > 200;
    },
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
      this.uploadError = "";
    },
    uploadImage() {
      if (!this.selectedFile) return;
      const formData = new FormData();
      formData.append('image', this.selectedFile);
      fetch('/api/user/profile_image', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            this.profileImage = 'http://localhost:5001' + data.profile_image + '?t=' + Date.now();
            this.selectedFile = null;
            this.uploadError = "";
          } else {
            this.uploadError = data.error || "Upload failed.";
          }
        })
        .catch(() => {
          this.uploadError = "Upload failed. Try again.";
        });
    },
    fetchProfileImage() {
      fetch('/api/user/profile_image', { credentials: 'include' })
        .then(res => res.json())
        .then(data => {
          if (data.profile_image) {
            this.profileImage = 'http://localhost:5001' + data.profile_image + '?t=' + Date.now();
          }
        });
    },
    fetchAchievements() {
      fetch('/api/user/achievements', { credentials: 'include' })
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            this.achievements = data;
          }
        });
    },
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    fetch('/api/leaderboard')
      .then((res) => res.json())
      .then((data) => {
        const user = data.find((u) => u.username === this.username);
        if (user) {
          this.score = user.score;
        }
      })
      .catch(() => {
        this.score = 0;
      });
    this.fetchProfileImage();
    this.fetchAchievements();
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  }
};
</script>

<style>
.hero-section {
  background: linear-gradient(120deg, #20c997 0%, #007bff 100%);
  min-height: 220px;
  border-radius: 0 0 2rem 2rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.hero-icon {
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.15));
}
</style>