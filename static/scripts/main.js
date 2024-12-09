// Hent spill fra serveren og vis dem
function fetchGames() {
    fetch('/games')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('games-container');
            container.innerHTML = '';
            data.forEach(game => {
                const gameItem = document.createElement('div');
                gameItem.className = 'game-item';
                gameItem.dataset.id = game.id;

                gameItem.innerHTML = `
                    <strong>${game.name}</strong> (${game.genre}) 
                    - ${game.release_date || 'Ingen dato'}
                    <br>Status: ${game.status}
                    <button onclick="deleteGame(${game.id})">Slett</button>
                `;
                container.appendChild(gameItem);
            });
        });
}

// Legg til nytt spill
document.getElementById('add-game-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const gameData = {
        name: document.getElementById('name').value,
        genre: document.getElementById('genre').value,
        release_date: document.getElementById('release_date').value
    };
    fetch('/games', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(gameData)
    }).then(() => {
        fetchGames();
        this.reset();
    });
});

// Slett spill
function deleteGame(id) {
    fetch(`/games/${id}`, {
        method: 'DELETE'
    }).then(() => {
        fetchGames();
    });
}

// Last inn spill når siden åpnes
document.addEventListener('DOMContentLoaded', () => {
    fetchGames();
});
