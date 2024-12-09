// Legg til spill via skjemaet
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
    }).then(response => response.json())
      .then(data => {
          alert(data.message);
          window.location.href = '/games/view';
      });
});
