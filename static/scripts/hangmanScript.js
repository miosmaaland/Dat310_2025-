const wordDisplay = document.querySelector(".word-display");
const hangmanImg = document.querySelector("#hangman-img");
const guessesText = document.querySelector(".guesses-text b");
const keyboardDiv = document.querySelector(".keyboard");
const gameModal = document.querySelector(".game-modal");
const playAgainBtn = document.querySelector(".play-again");
const hintText = document.querySelector(".hint-text b");
const resultTitle = document.querySelector("#result-title");
const finalWordText = document.querySelector("#final-word");
const resultGif = document.querySelector("#result-gif");

let selectedWord = "";
let correctLetters = [];
let wrongGuessCount = 0;
const maxGuesses = 6;

function getRandomWord() {
    const { word, hint } = wordList[Math.floor(Math.random() * wordList.length)];
    selectedWord = word.toLowerCase();
    correctLetters = [];
    wrongGuessCount = 0;

    // Reset UI
    hangmanImg.src = `/static/hang-man-images/hangman-0.svg`;
    guessesText.innerText = `${wrongGuessCount} / ${maxGuesses}`;
    hintText.innerText = hint;
    wordDisplay.innerHTML = selectedWord
        .split("")
        .map(() => `<li class="letter"></li>`)
        .join("");
    keyboardDiv.querySelectorAll("button").forEach(btn => btn.disabled = false);
    gameModal.classList.remove("show");
}

// Keyboard generation
function createKeyboard() {
    const letters = "abcdefghijklmnopqrstuvwxyz";
    keyboardDiv.innerHTML = "";
    for (let letter of letters) {
        const button = document.createElement("button");
        button.innerText = letter;
        button.addEventListener("click", () => handleGuess(letter, button));
        keyboardDiv.appendChild(button);
    }
}

// Guess handling
function handleGuess(letter, button) {
    button.disabled = true;
    if (selectedWord.includes(letter)) {
        [...selectedWord].forEach((char, index) => {
            if (char === letter) {
                wordDisplay.querySelectorAll("li")[index].innerText = char;
                wordDisplay.querySelectorAll("li")[index].classList.add("guessed");
            }
        });

        if (!correctLetters.includes(letter)) {
            correctLetters.push(letter);
        }
    } else {
        wrongGuessCount++;
        hangmanImg.src = `/static/hang-man-images/hangman-${wrongGuessCount}.svg`;
    }
    guessesText.innerText = `${wrongGuessCount} / ${maxGuesses}`;
    checkGameStatus();
}


// Game end check
function checkGameStatus() {
    if (wrongGuessCount === maxGuesses) {
        endGame(false);
    } else if (correctLetters.length === [...new Set(selectedWord.split(""))].length) {
        endGame(true);
    }
}

// End game
function endGame(win) {
    gameModal.classList.add("show");

    resultTitle.innerText = win ? "You Won! 🎉" : "Game Over!";
    resultGif.src = win
        ? "/static/hang-man-images/victory.gif"
        : "/static/hang-man-images/lost.gif";
    finalWordText.innerText = selectedWord;

    // Disable all keys
    keyboardDiv.querySelectorAll("button").forEach(btn => btn.disabled = true);
}


// Replay
playAgainBtn.addEventListener("click", () => {
    getRandomWord();
});

document.addEventListener("DOMContentLoaded", () => {
    createKeyboard();
    getRandomWord();
});

