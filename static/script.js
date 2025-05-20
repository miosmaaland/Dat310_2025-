let currentQuestion = null;
let score = 0;

function getQueryParams() {
    const params = {};
    window.location.search
        .substring(1)
        .split("&")
        .forEach(pair => {
            const [key, value] = pair.split("=");
            if (key && value) params[key] = decodeURIComponent(value);
        });
    return params;
}


async function loadQuestion() {
    try {
        const params = getQueryParams();
        const queryString = new URLSearchParams(params).toString();
        const response = await fetch(`/get_question?${queryString}`);
        currentQuestion = await response.json();

        // Display question
        document.getElementById('question').textContent = currentQuestion.question;
        document.getElementById('series-info').textContent = `Category: ${currentQuestion.category_name} - Level ${currentQuestion.level}`;
        document.getElementById('feedback').textContent = '';

        // Clear previous answers
        const answersContainer = document.getElementById('answers');
        answersContainer.innerHTML = '';

        // Combine and shuffle correct + wrong answers
        const answers = [
            currentQuestion.correct_answer,
            ...currentQuestion.wrong_answers
        ];
        answers.sort(() => Math.random() - 0.5); // Shuffle

        // Create answer buttons
        answers.forEach(answer => {
            const button = document.createElement('button');
            button.className = 'answer-btn';
            button.textContent = answer;
            button.onclick = () => checkAnswer(answer);
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

        document.querySelectorAll('.answer-btn').forEach(button => {
            const isCorrect = button.textContent === currentQuestion.correct_answer;
            const isSelected = button.textContent === selectedAnswer;

            if (isCorrect) {
                button.style.backgroundColor = '#4CAF50';
            } else if (isSelected) {
                button.style.backgroundColor = '#ff4444';
            }

            button.disabled = true;
        });

        if (result.correct) {
            score += 10;
            feedbackEl.textContent = `✅ Correct! +10 points!`;
        } else {
            feedbackEl.textContent = `❌ Wrong! The correct answer was: ${currentQuestion.correct_answer}`;
        }

        document.getElementById('score').textContent = `Score: ${score}`;
        setTimeout(loadQuestion, 2000);

    } catch (error) {
        console.error('Error checking answer:', error);
    }
}

async function skipQuestion() {
    score = Math.max(0, score - 5);
    document.getElementById('score').textContent = `Score: ${score}`;
    document.getElementById('feedback').textContent = "⏩ Skipped! -5 points";
    setTimeout(loadQuestion, 1000);
}

window.addEventListener('DOMContentLoaded', () => {
    loadQuestion();
    document.getElementById('skip-btn').addEventListener('click', skipQuestion);
});
