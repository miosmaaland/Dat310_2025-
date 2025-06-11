// Hangman Game JavaScript
const hangmanImages = [
   '/static/hang-man-images/hangman-0.svg',
   '/static/hang-man-images/hangman-1.svg',
   '/static/hang-man-images/hangman-2.svg',
   '/static/hang-man-images/hangman-3.svg',
   '/static/hang-man-images/hangman-4.svg',
   '/static/hang-man-images/hangman-5.svg',
   '/static/hang-man-images/hangman-6.svg'
];

let currentWord = '';
let correctLetters = [];
let wrongGuesses = 0;
const maxWrongGuesses = 6;

// CS Terms and hints
const csTerms = [
   { word: 'ALGORITHM', hint: 'A step by step procedure for solving a problem' },
   { word: 'RECURSION', hint: 'A function that calls itself' },
   { word: 'ARRAY', hint: 'A collection of elements stored at contiguous memory locations' },
   { word: 'STACK', hint: 'A data structure that follows LIFO principle' },
   { word: 'QUEUE', hint: 'A data structure that follows FIFO principle' },
   { word: 'BINARY', hint: 'Base-2 number system using only 0 and 1' },
   { word: 'COMPILER', hint: 'Translates source code into machine code' },
   { word: 'DATABASE', hint: 'Organized collection of structured information' },
   { word: 'ENCRYPTION', hint: 'Process of converting information into secret code' },
   { word: 'FIREWALL', hint: 'Network security system that monitors and controls traffic' },
   { word: 'JAVASCRIPT', hint: 'Popular programming language for web development' },
   { word: 'PYTHON', hint: 'High-level programming language known for simplicity' },
   { word: 'VARIABLE', hint: 'Storage location with an associated name' },
   { word: 'FUNCTION', hint: 'Reusable block of code that performs a specific task' },
   { word: 'BOOLEAN', hint: 'Data type with only two possible values: true or false' }
];

// DOM elements
const hangmanImg = document.getElementById('hangman-img');
const wordDisplay = document.querySelector('.word-display');
const hintText = document.querySelector('.hint-text b');
const guessesText = document.querySelector('.guesses-text b');
const keyboard = document.querySelector('.keyboard');
const gameModal = document.querySelector('.game-modal');
const resultTitle = document.getElementById('result-title');
const resultGif = document.getElementById('result-gif');
const finalWord = document.getElementById('final-word');
const playAgainBtn = document.querySelector('.play-again');

document.addEventListener('DOMContentLoaded', function() {
   initializeGame();
   createKeyboard();
   
   playAgainBtn.addEventListener('click', function() {
       gameModal.classList.remove('show');
       initializeGame();
       createKeyboard();
   });
});

function initializeGame() {
   // Reset game state
   correctLetters = [];
   wrongGuesses = 0;
   
   // Select random word
   const randomTerm = csTerms[Math.floor(Math.random() * csTerms.length)];
   currentWord = randomTerm.word;
   
   // Update UI
   hintText.textContent = randomTerm.hint;
   guessesText.textContent = `${wrongGuesses} / ${maxWrongGuesses}`;
   hangmanImg.src = hangmanImages[0];
   
   // Display word blanks
   displayWord();
}

function displayWord() {
   wordDisplay.innerHTML = '';
   
   for (let letter of currentWord) {
       const li = document.createElement('li');
       li.className = 'letter';
       
       if (correctLetters.includes(letter)) {
           li.textContent = letter;
           li.classList.add('guessed');
       }
       
       wordDisplay.appendChild(li);
   }
}

function createKeyboard() {
   keyboard.innerHTML = '';
   
   // Create keyboard buttons for A-Z
   for (let i = 65; i <= 90; i++) {
       const button = document.createElement('button');
       const letter = String.fromCharCode(i);
       button.textContent = letter;
       button.addEventListener('click', () => guessLetter(letter, button));
       keyboard.appendChild(button);
   }
}

function guessLetter(letter, buttonElement) {
   // Disable the clicked button
   buttonElement.disabled = true;
   
   if (currentWord.includes(letter)) {
       // Correct guess
       correctLetters.push(letter);
       displayWord();
       
       // Check if word is complete
       if (currentWord.split('').every(char => correctLetters.includes(char))) {
           endGame(true);
       }
   } else {
       // Wrong guess
       wrongGuesses++;
       hangmanImg.src = hangmanImages[wrongGuesses];
       guessesText.textContent = `${wrongGuesses} / ${maxWrongGuesses}`;
       
       // Check if game is over
       if (wrongGuesses === maxWrongGuesses) {
           endGame(false);
       }
   }
}

function endGame(won) {
   // Disable all keyboard buttons
   const buttons = keyboard.querySelectorAll('button');
   buttons.forEach(btn => btn.disabled = true);
   
   // Show result modal
   setTimeout(() => {
       if (won) {
           resultTitle.textContent = 'Congratulations! 🎉';
           resultGif.src = '/static/hang-man-images/victory.gif';
           resultGif.alt = 'Victory';
       } else {
           resultTitle.textContent = 'Game Over! 😔';
           resultGif.src = '/static/hang-man-images/lost.gif';
           resultGif.alt = 'Game Over';
       }
       
       finalWord.textContent = currentWord;
       gameModal.classList.add('show');
   }, 300);
}