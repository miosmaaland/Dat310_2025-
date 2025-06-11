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
            <li class="nav-item"><router-link class="nav-link" to="/">Home</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/profile">Profile</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/leaderboard">Leaderboard</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/hangman">Hangman</router-link></li>
            <li class="nav-item">
              <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <section class="hero-section d-flex flex-column justify-content-center align-items-center text-center py-5 mb-4">
      <div class="hero-icon mb-3">
        <span style="font-size: 3rem;">💻</span>
      </div>
      <h1 class="display-5 fw-bold text-white">Computer Science Challenge</h1>
      <p class="lead text-white-50 mb-0">Test your knowledge and earn points!</p>
    </section>

    <div class="container mt-4">
      <form class="row g-3 mb-4" @submit.prevent="fetchQuestion">
        <div class="col-md-5">
          <label for="category" class="form-label">Category</label>
          <select v-model="category" id="category" class="form-select">
            <option value="">Any</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>
        <div class="col-md-5">
          <label for="level" class="form-label">Level</label>
          <select v-model="level" id="level" class="form-select">
            <option value="">Any</option>
            <option value="1">Level 1</option>
            <option value="2">Level 2</option>
            <option value="3">Level 3</option>
          </select>
        </div>
        <div class="col-md-2 d-flex align-items-end">
          <button type="submit" class="btn btn-primary w-100">New Question</button>
        </div>
      </form>
      

      <div v-if="question" class="card mb-3 shadow">
        <div class="card-body">
          <h5 class="card-title">{{ question.question }}</h5>
          <div class="list-group">
            <button
              v-for="(option, key) in question.options"
              :key="key"
              @click="submitAnswer(key)"
              class="list-group-item list-group-item-action"
              :disabled="loading"
            >
              {{ key }}: {{ option }}
            </button>
          </div>
        </div>
      </div>
      <div v-else class="text-center text-muted mb-3">No question loaded.</div>

      <div class="mb-3">
        <button class="btn btn-warning" @click="skipQuestion" :disabled="loading">
          ⏩ Skip Question (-5)
        </button>
      </div>
      <p class="fs-5" :class="{'text-success': correctAnswer, 'text-danger': correctAnswer === false}">
        {{ message }}
      </p>
      <div class="fs-4">Score: {{ score }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuizPlay",
  data() {
    return {
      categories: [],
      category: "",
      level: "",
      question: null,
      score: 0,
      message: '',
      correctAnswer: null,
      loading: false,
    };
  },
  methods: {
    fetchCategories() {
      fetch('/api/categories')
        .then(res => res.json())
        .then(data => {
          this.categories = data;
        });
    },
    fetchScore() {
      fetch('/api/leaderboard')
        .then(res => res.json())
        .then(data => {
          const username = localStorage.getItem('username');
          const user = data.find(u => u.username === username);
          if (user) this.score = user.score;
        });
    },
    fetchQuestion() {
      this.loading = true;
      let url = '/api/question';
      const params = [];
      if (this.category) params.push(`category=${encodeURIComponent(this.category)}`);
      if (this.level) params.push(`level=${encodeURIComponent(this.level)}`);
      if (params.length) url += '?' + params.join('&');
      fetch(url)
        .then((res) => res.json())
        .then((data) => {
          if (!data.error) {
            this.question = data;
            this.message = '';
            this.correctAnswer = null;
          } else {
            this.question = null;
            this.message = data.error;
          }
          this.loading = false;
        })
        .catch(() => {
          this.message = 'Failed to load question.';
          this.loading = false;
        });
    },
    submitAnswer(key) {
      if (this.loading) return;
      this.loading = true;
      const answerText = this.question.options[key];
      fetch('/api/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ question_id: this.question.id, answer: answerText }),
      })
        .then((res) => res.json())
        .then((data) => {
          this.correctAnswer = data.correct;
          if (data.correct) {
            this.message = 'Correct! +10 points';
          } else {
            this.message = data.correct_answer
              ? `Wrong! The correct answer was ${data.correct_answer}`
              : 'Wrong! (No correct answer found)';
          }
          this.fetchScore();
          setTimeout(() => {
            this.fetchQuestion();
            this.message = '';
            this.correctAnswer = null;
          }, 1000);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    skipQuestion() {
      if (this.loading) return;
      this.loading = true;
      fetch('/api/skip', { method: 'POST' })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            this.message = 'Question skipped. -5 points';
            this.fetchScore();
            setTimeout(() => {
              this.fetchQuestion();
            }, 800);
          } else {
            this.message = data.error || 'Could not skip the question.';
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },

    logout() {
      fetch('/api/logout', { method: 'POST' })
        .then(() => {
          localStorage.clear();
          this.$router.push('/');
        });
    },
  },
  mounted() {
    this.fetchCategories();
    this.fetchScore();
    this.fetchQuestion();
  },
  watch: {
    category() {
      this.fetchQuestion();
    },
    level() {
      this.fetchQuestion();
    }
  }
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(120deg, #fd7e14 0%, #007bff 100%);
  min-height: 220px;
  border-radius: 0 0 2rem 2rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.hero-icon {
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.15));
}
</style>