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
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/play">Play</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn && isAdmin">
              <router-link class="nav-link" to="/admin">Admin</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/profile">Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/leaderboard">Leaderboard</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link class="nav-link" to="/hangman">Hangman</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <button class="nav-link btn btn-danger" @click="logout">Logout</button>
            </li>
            <template v-else>
              <li class="nav-item">
                <router-link class="nav-link" to="/login">Login</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/signup">Sign Up</router-link>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>

    
    <section class="hero-section d-flex flex-column justify-content-center align-items-center text-center py-5 mb-4">
      <div class="hero-icon mb-3">
        <span style="font-size: 4rem;">🧠</span>
      </div>
      <h1 class="display-4 fw-bold text-white">Welcome to CS Quiz Master!</h1>
      <p class="lead text-white-50 mb-4">Sharpen your computer science knowledge and rise to the top of the leaderboard!</p>
      <div class="d-flex flex-column flex-md-row gap-3 justify-content-center">
        <router-link v-if="isLoggedIn" class="btn btn-primary btn-lg px-4" to="/play">Start Quiz ▶️</router-link>
        <template v-else>
          <router-link class="btn btn-success btn-lg px-4" to="/signup">Sign Up to Play ✨</router-link>
          <router-link class="btn btn-outline-light btn-lg px-4" to="/login">Login 🔑</router-link>
        </template>
      </div>
    </section>

    
    <section class="container my-5">
      <div class="row g-4 justify-content-center">
        <div class="col-12 col-md-4">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-body text-center">
              <div class="mb-3" style="font-size: 2.5rem;">❓</div>
              <h5 class="card-title">Challenging Questions</h5>
              <p class="card-text">Answer trivia questions on networking, security, development, and more!</p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-body text-center">
              <div class="mb-3" style="font-size: 2.5rem;">🏆</div>
              <h5 class="card-title">Compete & Climb</h5>
              <p class="card-text">Earn points for every correct answer and climb the global leaderboard.</p>
            </div>
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div class="card h-100 shadow-sm border-0">
            <div class="card-body text-center">
              <div class="mb-3" style="font-size: 2.5rem;">🎯</div>
              <h5 class="card-title">Achievements</h5>
              <p class="card-text">Unlock achievements as you play and show off your CS skills!</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    
    <section class="container my-5">
  <h2 class="text-center mb-4">Leaderboard Preview</h2>
  <div class="table-responsive">
    <table class="table table-striped table-hover mx-auto" style="max-width: 500px;">
      <thead class="table-dark">
        <tr>
          <th>Rank</th>
          <th>User</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, idx) in topLeaderboard" :key="user.username">
          <td>{{ idx + 1 }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.score }}</td>
        </tr>
        <tr v-if="topLeaderboard.length === 0">
          <td colspan="3" class="text-center text-muted">No users yet</td>
        </tr>
      </tbody>
    </table>
  </div>
</section>

    
    <section class="container my-5">
      <h2 class="text-center mb-4">How It Works</h2>
      <div class="row justify-content-center">
        <div class="col-12 col-md-8">
          <ol class="list-group list-group-numbered">
            <li class="list-group-item">Answer trivia questions related to computer science concepts.</li>
            <li class="list-group-item">Earn points for every correct answer.</li>
            <li class="list-group-item">Compete with others and climb the leaderboard!</li>
            <li class="list-group-item">Unlock achievements and track your progress.</li>
            <li class="list-group-item">Play Hangman to guess CS terms and improve your skills.</li>
          </ol>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      topLeaderboard: [],
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user_id");
    },
    isAdmin() {
      return localStorage.getItem("is_admin") === "1";
    }
  },
  methods: {
    logout() {
      fetch('http://localhost:5001/api/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
        .then((res) => res.json())
        .then(() => {
          localStorage.clear();
          this.$router.push('/login');
        })
        .catch(() => {
          this.errorMessage = 'An error occurred. Please try again.';
        });
    },
  },
  mounted() {
    fetch('/api/leaderboard')
      .then(res => res.json())
      .then(data => {
        this.topLeaderboard = data.slice(0, 3);
      });
  }
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(120deg, #007bff 0%, #6610f2 100%);
  min-height: 320px;
  border-radius: 0 0 2rem 2rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.hero-icon {
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.15));
}
</style>