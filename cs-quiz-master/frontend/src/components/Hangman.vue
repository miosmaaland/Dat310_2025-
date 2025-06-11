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
              <router-link class="nav-link" to="/play">Play</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/profile">Profile</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/hangman">Hangman</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/logout">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>


    <section class="hero-section d-flex flex-column justify-content-center align-items-center text-center py-5 mb-4">
  <div class="hero-icon mb-3">
    <span style="font-size: 3rem;">🎮</span>
  </div>
  <h1 class="display-5 fw-bold text-white">CS Hangman</h1>
  <p class="lead text-white-50 mb-0">Guess the CS term before you run out of tries!</p>
</section>

  <div class="container mt-5">
    <h2 class="mb-4">CS Hangman</h2>

    <div class="hangman-box mb-3 text-center">
      <img
        :src="hangmanImages[wrongGuesses]"
        alt="hangman"
        style="max-width: 200px;"
      />
    </div>

    <h1 class="text-center mb-4">CS Hangman</h1>

    <div class="game-box mb-4 text-center">
      <ul
        class="word-display list-inline"
        style="font-size: 2rem; letter-spacing: 0.3rem; padding: 0; margin-bottom: 1rem;"
      >
        <li
          v-for="(letter, index) in selectedWord"
          :key="index"
          class="letter"
          :class="{ guessed: guessedLetters.includes(letter) }"
          style="border-bottom: 2px solid black; min-width: 1.5rem; display: inline-block; text-transform: uppercase; user-select: none; padding: 0 0.3rem; margin-right: 0.1rem;"
        >
          {{ guessedLetters.includes(letter) ? letter : "" }}
        </li>
      </ul>

      <h4 class="hint-text mb-2">
        Hint: <b>{{ currentHint }}</b>
      </h4>

      <h4 class="guesses-text mb-3">
        Incorrect guesses: <b>{{ wrongGuesses }} / {{ maxWrongGuesses }}</b>
      </h4>

      
      <div class="keyboard mb-3" style="max-width: 400px; margin: 0 auto;">
        <button
          v-for="letter in letters"
          :key="letter"
          :disabled="guessedLetters.includes(letter) || gameOver"
          @click="handleGuess(letter)"
          style="width: 2.5rem; height: 2.5rem; margin: 0.15rem; font-weight: bold; text-transform: uppercase; cursor: pointer;"
        >
          {{ letter }}
        </button>
      </div>

      <div class="mb-3" style="max-width: 200px; margin: 0 auto;">
        <input
          v-model="guessInput"
          @keyup.enter="makeGuess"
          class="form-control text-center"
          maxlength="1"
          placeholder="Enter a letter"
          :disabled="gameOver"
        />
      </div>

      <button
        @click="makeGuess"
        class="btn btn-primary"
        style="display: block; margin: 0 auto;"
        :disabled="gameOver"
      >
        Guess
      </button>

      <p class="mt-3 font-weight-bold" style="min-height: 1.5rem;">{{ message }}</p>
    </div>

    
    <div
      v-if="gameOver"
      class="game-modal"
      style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 1000;"
    >
      <div
        class="content bg-light p-4 rounded text-center"
        style="max-width: 350px; width: 100%;"
      >
        <img
          :src="gameWon ? victoryGif : lostGif"
          :alt="gameWon ? 'Victory' : 'Game Over'"
          style="max-width: 150px; margin-bottom: 1rem;"
        />
        <h4>{{ gameWon ? "Congratulations! 🎉" : "Game Over! 😔" }}</h4>
        <p>The correct word was: <b>{{ selectedWord.join('') }}</b></p>
        <button @click="resetGame" class="btn btn-success mt-3">Play Again</button>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  name: "HangmanGame",
  data() {
    return {
      csTerms: [
        { word: "ALGORITHM", hint: "A step by step procedure for solving a problem" },
        { word: "RECURSION", hint: "A function that calls itself" },
        { word: "ARRAY", hint: "A collection of elements stored at contiguous memory locations" },
        { word: "STACK", hint: "A data structure that follows LIFO principle" },
        { word: "QUEUE", hint: "A data structure that follows FIFO principle" },
        { word: "BINARY", hint: "Base-2 number system using only 0 and 1" },
        { word: "COMPILER", hint: "Translates source code into machine code" },
        { word: "DATABASE", hint: "Organized collection of structured information" },
        { word: "ENCRYPTION", hint: "Process of converting information into secret code" },
        { word: "FIREWALL", hint: "Network security system that monitors and controls traffic" },
        { word: "JAVASCRIPT", hint: "Popular programming language for web development" },
        { word: "PYTHON", hint: "High-level programming language known for simplicity" },
        { word: "VARIABLE", hint: "Storage location with an associated name" },
        { word: "FUNCTION", hint: "Reusable block of code that performs a specific task" },
        { word: "BOOLEAN", hint: "Data type with only two possible values: true or false" },
      ],
      letters: "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split(""),
      selectedWord: [],
      currentHint: "",
      guessedLetters: [],
      wrongGuesses: 0,
      maxWrongGuesses: 6,
      guessInput: "",
      message: "",
      gameOver: false,
      gameWon: false,
      hangmanImages: [
        "/hang-man-images/hangman-0.svg",
        "/hang-man-images/hangman-1.svg",
        "/hang-man-images/hangman-2.svg",
        "/hang-man-images/hangman-3.svg",
        "/hang-man-images/hangman-4.svg",
        "/hang-man-images/hangman-5.svg",
        "/hang-man-images/hangman-6.svg",
      ],
      victoryGif: "/hang-man-images/victory.gif",
      lostGif: "/hang-man-images/lost.gif",
    };
  },
  created() {
    this.resetGame();
  },
  methods: {
    resetGame() {
      const randomTerm = this.csTerms[Math.floor(Math.random() * this.csTerms.length)];
      this.selectedWord = randomTerm.word.split("");
      this.currentHint = randomTerm.hint;
      this.guessedLetters = [];
      this.wrongGuesses = 0;
      this.guessInput = "";
      this.message = "";
      this.gameOver = false;
      this.gameWon = false;
    },
    handleGuess(letter) {
      if (this.gameOver || this.guessedLetters.includes(letter)) return;

      this.guessedLetters.push(letter);

      if (!this.selectedWord.includes(letter)) {
        this.wrongGuesses++;
        this.message = `Wrong guess! ${this.maxWrongGuesses - this.wrongGuesses} guesses left.`;
      } else {
        this.message = "Good guess!";
      }

      this.checkGameStatus();
    },
    makeGuess() {
      const letter = this.guessInput.toUpperCase();

      if (letter.length !== 1 || !this.letters.includes(letter)) {
        this.message = "Please enter a valid single letter.";
        this.guessInput = "";
        return;
      }

      if (this.guessedLetters.includes(letter)) {
        this.message = "You already guessed that letter!";
        this.guessInput = "";
        return;
      }

      this.handleGuess(letter);
      this.guessInput = "";
    },
    checkGameStatus() {
      
      const uniqueLetters = [...new Set(this.selectedWord)];
      const allGuessed = uniqueLetters.every((letter) =>
        this.guessedLetters.includes(letter)
      );

      if (allGuessed) {
        this.message = "Congratulations! You've won!";
        this.gameOver = true;
        this.gameWon = true;
        return;
      }

      if (this.wrongGuesses >= this.maxWrongGuesses) {
        this.message = `Game Over! The word was "${this.selectedWord.join("")}".`;
        this.gameOver = true;
        this.gameWon = false;
      }
    },
  },
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(120deg, #e83e8c 0%, #007bff 100%);
  min-height: 220px;
  border-radius: 0 0 2rem 2rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.hero-icon {
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.15));
}
</style>
