// Quiz Game JavaScript
let currentQuestion = null;
let score = 0;

document.addEventListener('DOMContentLoaded', function() {
    loadNextQuestion();
    
    // Skip button functionality
    const skipBtn = document.getElementById('skip-btn');
    if (skipBtn) {
        skipBtn.addEventListener('click', function() {
            skipQuestion();
        });
    }
});

function loadNextQuestion() {
    fetch('/api/question')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('question').textContent = 'Error loading question: ' + data.error;
                return;
            }
            
            currentQuestion = data;
            displayQuestion(data);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('question').textContent = 'Error loading question';
        });
}

function displayQuestion(questionData) {
    const questionElement = document.getElementById('question');
    const answersElement = document.getElementById('answers');
    const feedbackElement = document.getElementById('feedback');
    
    questionElement.textContent = questionData.question;
    feedbackElement.textContent = '';
    
    // Clear previous answers
    answersElement.innerHTML = '';
    
    // Create answer buttons
    Object.entries(questionData.options).forEach(([key, value]) => {
        const button = document.createElement('button');
        button.className = 'answer-btn';
        button.textContent = `${key}. ${value}`;
        button.onclick = () => submitAnswer(key);
        answersElement.appendChild(button);
    });
}

function submitAnswer(answer) {
    if (!currentQuestion) return;
    
    // Disable all answer buttons
    const answerButtons = document.querySelectorAll('.answer-btn');
    answerButtons.forEach(btn => btn.disabled = true);
    
    fetch('/api/answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: currentQuestion.id,
            answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        const feedbackElement = document.getElementById('feedback');
        const scoreElement = document.getElementById('score');
        
        if (data.correct) {
            feedbackElement.textContent = 'Correct! +10 points';
            feedbackElement.style.color = 'green';
        } else {
            feedbackElement.textContent = `Incorrect. The correct answer was ${data.correct_answer}`;
            feedbackElement.style.color = 'red';
        }
        
        // Update score display
        scoreElement.textContent = `Score: ${data.total_score}`;
        
        // Load next question after delay
        setTimeout(() => {
            loadNextQuestion();
        }, 3000);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('feedback').textContent = 'Error submitting answer';
        
        // Re-enable buttons on error
        answerButtons.forEach(btn => btn.disabled = false);
    });
}

function skipQuestion() {
    if (!currentQuestion) return;
    
    // Deduct points for skipping
    fetch('/api/answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: currentQuestion.id,
            answer: 'SKIP'  // Special value for skip
        })
    })
    .then(response => response.json())
    .then(data => {
        const feedbackElement = document.getElementById('feedback');
        const scoreElement = document.getElementById('score');
        
        feedbackElement.textContent = 'Question skipped! -5 points';
        feedbackElement.style.color = 'orange';
        
        // Update score (assuming backend handles skip penalty)
        scoreElement.textContent = `Score: ${data.total_score}`;
        
        // Load next question after delay
        setTimeout(() => {
            loadNextQuestion();
        }, 2000);
    })
    .catch(error => {
        console.error('Error:', error);
        loadNextQuestion(); // Continue anyway
    });
}