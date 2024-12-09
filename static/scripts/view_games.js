// Hent spill og vis dem på siden
function fetchGames() {
    fetch('/games')
        .then(response => response.json())
        .then(games => {
            const container = document.getElementById('games-container');
            container.innerHTML = '';
            games.forEach(game => {
                const gameElement = document.createElement('div');
                gameElement.innerHTML = `
                    <p><strong>${game.name}</strong> (${game.genre}) 
                    - ${game.release_date || 'Ingen dato'}
                    <br>Status: ${game.status}</p>
                    <button onclick="deleteGame(${game.id})">Slett</button>
                `;
                container.appendChild(gameElement);
            });
        });
}

// Slett spill
function deleteGame(id) {
    fetch(`/games/${id}`, {
        method: 'DELETE'
    }).then(() => fetchGames());
}

// Last inn spill når siden åpnes
document.addEventListener('DOMContentLoaded', fetchGames);
