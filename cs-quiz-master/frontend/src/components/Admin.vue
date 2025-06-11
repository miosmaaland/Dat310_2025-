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
        <span style="font-size: 3rem;">🛠️</span>
      </div>
      <h1 class="display-5 fw-bold text-white">Admin Panel</h1>
      <p class="lead text-white-50 mb-0">Manage quiz questions and categories</p>
    </section>

    <div class="container mt-4">
      <div v-if="!isAdmin" class="alert alert-danger">You are not authorized to view this page.</div>
      <div v-else>
        <div class="card mb-4 shadow">
          <div class="card-body">
            <h4 class="card-title mb-3">Add New Question</h4>
            <form @submit.prevent="addQuestion">
              <div class="row g-2">
                <div class="col-md-6">
                  <input v-model="newQuestion.question" placeholder="Question" class="form-control mb-2" required />
                </div>
                <div class="col-md-6">
                  <input v-model="newQuestion.correct_answer" placeholder="Correct Answer" class="form-control mb-2" required />
                </div>
                <div class="col-12 col-md-4">
                  <input v-model="newQuestion.wrong1" placeholder="Wrong Answer 1" class="form-control mb-2" required />
                </div>
                <div class="col-12 col-md-4">
                  <input v-model="newQuestion.wrong2" placeholder="Wrong Answer 2" class="form-control mb-2" required />
                </div>
                <div class="col-12 col-md-4">
                  <input v-model="newQuestion.wrong3" placeholder="Wrong Answer 3" class="form-control mb-2" required />
                </div>
                <div class="col-6 col-md-3">
                  <input v-model.number="newQuestion.category_id" placeholder="Category ID" class="form-control mb-2" required />
                </div>
                <div class="col-6 col-md-3">
                  <input v-model.number="newQuestion.level" placeholder="Level (1-5)" class="form-control mb-2" required />
                </div>
                <div class="col-12 col-md-6 d-flex align-items-end">
                  <button class="btn btn-success w-100" type="submit">Add Question</button>
                </div>
              </div>
            </form>
            <div v-if="errorMessage" class="alert alert-danger mt-2">{{ errorMessage }}</div>
            <div v-if="successMessage" class="alert alert-success mt-2">{{ successMessage }}</div>
          </div>
        </div>

        <div class="card shadow">
          <div class="card-body">
            <h4 class="card-title mb-3">All Questions</h4>
            <div class="table-responsive">
              <table class="table table-bordered align-middle">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Question</th>
                    <th>Correct</th>
                    <th>Category</th>
                    <th>Level</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="q in questions" :key="q.id">
                    <td>{{ q.id }}</td>
                    <td>
                      <input v-if="editId === q.id" v-model="editQuestion.question" class="form-control" />
                      <span v-else>{{ q.question }}</span>
                    </td>
                    <td>
                      <input v-if="editId === q.id" v-model="editQuestion.correct_answer" class="form-control" />
                      <span v-else>{{ q.correct_answer }}</span>
                    </td>
                    <td>
                      <input v-if="editId === q.id" v-model.number="editQuestion.category_id" class="form-control" />
                      <span v-else>{{ q.category_id }}</span>
                    </td>
                    <td>
                      <input v-if="editId === q.id" v-model.number="editQuestion.level" class="form-control" />
                      <span v-else>{{ q.level }}</span>
                    </td>
                    <td>
                      <button v-if="editId !== q.id" class="btn btn-primary btn-sm" @click="startEdit(q)">Edit</button>
                      <button v-if="editId === q.id" class="btn btn-success btn-sm" @click="saveEdit(q.id)">Save</button>
                      <button v-if="editId === q.id" class="btn btn-secondary btn-sm" @click="cancelEdit">Cancel</button>
                      <button class="btn btn-danger btn-sm" @click="deleteQuestion(q.id)">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminPage",
  data() {
    return {
      questions: [],
      newQuestion: {
        question: "",
        correct_answer: "",
        wrong1: "",
        wrong2: "",
        wrong3: "",
        category_id: 1,
        level: 1,
      },
      editId: null,
      editQuestion: {},
      errorMessage: "",
      successMessage: "",
    };
  },
  computed: {
    isAdmin() {
      return localStorage.getItem("is_admin") === "1";
    },
  },
  methods: {
    logout() {
      fetch('/api/logout', { method: 'POST' })
        .then(() => {
          localStorage.clear();
          this.$router.push('/');
        });
    },
    fetchQuestions() {
      fetch("/api/questions", { credentials: "include" })
        .then((res) => res.json())
        .then((data) => {
          this.questions = data;
        });
    },
    addQuestion() {
      const errors = [];
      const q = this.newQuestion;
      if (!q.question.trim()) errors.push("Question is required.");
      if (!q.correct_answer.trim()) errors.push("Correct answer is required.");
      if (!q.wrong1.trim() || !q.wrong2.trim() || !q.wrong3.trim()) errors.push("All wrong answers are required.");
      if (![1,2,3,4,5].includes(Number(q.level))) errors.push("Level must be 1, 2, 3, 4 or 5.");
      if (!Number.isInteger(Number(q.category_id)) || Number(q.category_id) < 1) errors.push("Category ID must be a positive integer.");
      const wrongs = [q.wrong1.trim(), q.wrong2.trim(), q.wrong3.trim()];
      if (wrongs.includes(q.correct_answer.trim())) errors.push("Wrong answers cannot match the correct answer.");
      if (new Set(wrongs).size !== wrongs.length) errors.push("Wrong answers must be unique.");
      if (errors.length) {
        this.errorMessage = errors.join(" ");
        this.successMessage = "";
        return;
      }
      const payload = {
        question: q.question,
        correct_answer: q.correct_answer,
        wrong_answers: wrongs,
        category_id: q.category_id,
        level: q.level,
      };
      fetch("/api/questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(payload),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            this.successMessage = "Question added!";
            this.errorMessage = "";
            this.fetchQuestions();
            this.newQuestion = {
              question: "",
              correct_answer: "",
              wrong1: "",
              wrong2: "",
              wrong3: "",
              category_id: 1,
              level: 1,
            };
          } else {
            this.errorMessage = data.error || "Failed to add question.";
            this.successMessage = "";
          }
        });
    },
    deleteQuestion(id) {
  if (!confirm("Are you sure you want to delete this question?")) return;
  fetch(`/api/questions/${id}`, {
    method: "DELETE",
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        this.successMessage = "Question deleted!";
        this.errorMessage = "";
        this.fetchQuestions();
      } else {
        this.errorMessage = data.error || "Failed to delete question.";
        this.successMessage = "";
      }
    });
},
    startEdit(q) {
      this.editId = q.id;
      this.editQuestion = {
        question: q.question,
        correct_answer: q.correct_answer,
        category_id: q.category_id,
        level: q.level,
      };
    },
    saveEdit(id) {
      const original = this.questions.find(q => q.id === id);
      const payload = {
        question: this.editQuestion.question,
        correct_answer: this.editQuestion.correct_answer,
        wrong_answers: original.wrong_answers,
        category_id: this.editQuestion.category_id,
        level: this.editQuestion.level,
      };
      fetch(`/api/questions/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(payload),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            this.successMessage = "Question updated!";
            this.errorMessage = "";
            this.editId = null;
            this.editQuestion = {};
            this.fetchQuestions();
          } else {
            this.errorMessage = data.error || "Failed to update question.";
            this.successMessage = "";
          }
        });
    },
    cancelEdit() {
      this.editId = null;
      this.editQuestion = {};
    },
  },
  mounted() {
    this.fetchQuestions();
  },
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