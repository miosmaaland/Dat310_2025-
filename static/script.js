let currentQuestion = null;
let score = 0;

async function loadQuestion() {
    try {
        const response = await fetch('/get_question');
        currentQuestion = await response.json();
        
        // Display question
        document.getElementById('question').textContent = currentQuestion.question;
        document.getElementById('series-info').textContent = `From: ${currentQuestion.series_name} (${currentQuestion.episode})`;
        document.getElementById('feedback').textContent = '';

        // Clear previous answers
        const answersContainer = document.getElementById('answers');
        answersContainer.innerHTML = '';

        // Create answer options
        const answers = [
            currentQuestion.correct_answer,
            ...JSON.parse(currentQuestion.wrong_answers) // Parse JSON string
        ];
        answers.sort(() => Math.random() - 0.5); // Shuffle

        // Add buttons to the DOM
        answers.forEach(answer => {
            const button = document.createElement('button');
            button.className = 'answer-btn';
            button.textContent = answer;
            button.onclick = () => checkAnswer(answer); // Attach click handler
            answersContainer.appendChild(button);
        });

    } catch (error) {
        console.error('Error loading question:', error);
    }
}

async function checkAnswer(selectedAnswer) {
    try {
        const response = await fetch('/check_answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                answer: selectedAnswer,
                question_id: currentQuestion.id
            })
        });

        const result = await response.json();
        const feedbackEl = document.getElementById('feedback');

        // Highlight answers
        document.querySelectorAll('.answer-btn').forEach(button => {
            const isCorrect = button.textContent === currentQuestion.correct_answer;
            const isSelected = button.textContent === selectedAnswer;

            if (isCorrect) {
                button.style.backgroundColor = '#4CAF50'; // Green for correct
            } else if (isSelected) {
                button.style.backgroundColor = '#ff4444'; // Red for wrong
            }

            button.disabled = true; // Disable buttons after selection
        });

        if (result.correct) {
            score += 10;
            feedbackEl.textContent = `✅ Correct! +10 points!`;
        } else {
            feedbackEl.textContent = `❌ Wrong! The correct answer was: ${currentQuestion.correct_answer}`;
        }

        // Update score display and leaderboard logic
        document.getElementById('score').textContent = `Score: ${score}`;
        setTimeout(loadQuestion, 2000);

    } catch (error) {
        console.error('Error checking answer:', error);
    }
}


async function skipQuestion() {
    score = Math.max(0, score - 5); // Prevent negative scores
    document.getElementById('score').textContent = `Score: ${score}`;
    document.getElementById('feedback').textContent = "⏩ Skipped! -5 points";
    setTimeout(loadQuestion, 1000);
}


window.addEventListener('DOMContentLoaded', () => {
    loadQuestion();
    document.getElementById('skip-btn').addEventListener('click', skipQuestion);
});