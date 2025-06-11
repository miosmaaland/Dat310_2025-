<template>
  <main>
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand" to="/">CS Quiz Master</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Home</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/play">Play</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/profile">Profile</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/hangman">Hangman</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button class="nav-link btn btn-danger" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    
    <section class="hero-section d-flex flex-column justify-content-center align-items-center text-center py-5 mb-4">
      <div class="hero-icon mb-3">
        <span style="font-size: 3rem;">🏆</span>
      </div>
      <h1 class="display-5 fw-bold text-white">Leaderboard</h1>
      <p class="lead text-white-50 mb-0">See how you stack up against the competition!</p>
    </section>

    <section class="container my-5">
      <div class="mb-3 d-flex flex-column flex-md-row gap-2 align-items-center justify-content-center">
        <input v-model="search" class="form-control" placeholder="Search by username" style="max-width: 200px;" />
        <select v-model="sortBy" class="form-select" style="max-width: 180px;">
          <option value="score-desc">Score (High to Low)</option>
          <option value="score-asc">Score (Low to High)</option>
          <option value="username-asc">Username (A-Z)</option>
          <option value="username-desc">Username (Z-A)</option>
        </select>
      </div>
      <div class="table-responsive">
        <table class="table table-striped table-hover shadow rounded">
          <thead class="table-dark">
            <tr>
              <th>Rank</th>
              <th>Username</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in filteredAndSortedLeaderboard" :key="user.username">
              <td>{{ index + 1 }}</td>
              <td>
                {{ user.username }}
                <div v-if="user.achievements && user.achievements.length" class="small text-muted">
                  <span v-for="ach in user.achievements" :key="ach" class="badge bg-success me-1">{{ ach }}</span>
                </div>
              </td>
              <td>{{ user.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: "LeaderboardTable",
  data() {
    return {
      leaderboard: [],
      search: "",
      sortBy: "score-desc",
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    },
    filteredAndSortedLeaderboard() {
      let filtered = this.leaderboard.filter(u =>
        u.username.toLowerCase().includes(this.search.toLowerCase())
      );
      if (this.sortBy === "score-desc") {
        filtered.sort((a, b) => b.score - a.score);
      } else if (this.sortBy === "score-asc") {
        filtered.sort((a, b) => a.score - b.score);
      } else if (this.sortBy === "username-asc") {
        filtered.sort((a, b) => a.username.localeCompare(b.username));
      } else if (this.sortBy === "username-desc") {
        filtered.sort((a, b) => b.username.localeCompare(a.username));
      }
      return filtered;
    }
  },
  methods: {
    logout() {
      fetch('/api/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
        .then(() => {
          localStorage.clear();
          this.$router.push('/');
        });
    },
  },
  mounted() {
    fetch('/api/leaderboard')
      .then((res) => res.json())
      .then((data) => {
        this.leaderboard = data;
      });
  },
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(120deg, #6610f2 0%, #007bff 100%);
  min-height: 220px;
  border-radius: 0 0 2rem 2rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}

.hero-icon {
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.15));
}
</style>