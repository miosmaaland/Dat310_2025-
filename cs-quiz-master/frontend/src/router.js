import { createRouter, createWebHistory } from "vue-router";
import AdminPanel from "./components/Admin.vue";

import HomePage from "./components/Home.vue";
import HangmanGame from "./components/Hangman.vue";
import LeaderboardTable from "./components/Leaderboard.vue";
import UserLogin from "./components/Login.vue";
import QuizPlay from "./components/Play.vue";
import UserProfile from "./components/Profile.vue";
import UserSignup from "./components/Signup.vue";




const routes = [
  { path: "/", component: HomePage }, 
  { path: "/profile", component: UserProfile },
  { path: "/signup", component: UserSignup },
  { path: "/play", component: QuizPlay },
  { path: "/leaderboard", component: LeaderboardTable },
  { path: "/hangman", component: HangmanGame },
  { path: "/login", component: UserLogin },
  { path: "/admin", component: AdminPanel },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  if (to.path === '/admin' && localStorage.getItem('is_admin') !== '1') {
    next('/'); //Laget for å unngå luringer som ikke er admin å få tilgang
  } else {
    next();
  }
});

export default router;