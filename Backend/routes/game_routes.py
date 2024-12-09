from flask import Blueprint, jsonify, request, render_template
from models import Game, db

# Lag Blueprint for games
game_routes = Blueprint('game_routes', __name__)

@game_routes.route('/')
def home():
    return render_template('index.html')

@game_routes.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([{
        'id': game.id,
        'name': game.name,
        'genre': game.genre,
        'release_date': game.release_date,
        'status': game.status
    } for game in games])

@game_routes.route('/games', methods=['POST'])
def add_game():
    data = request.json
    new_game = Game(
        name=data['name'],
        genre=data['genre'],
        release_date=data.get('release_date'),
        status=data.get('status', 'Not Completed')
    )
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game added successfully!'})

@game_routes.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    data = request.json
    game = Game.query.get_or_404(id)
    game.name = data.get('name', game.name)
    game.genre = data.get('genre', game.genre)
    game.release_date = data.get('release_date', game.release_date)
    game.status = data.get('status', game.status)
    db.session.commit()
    return jsonify({'message': 'Game updated successfully!'})

@game_routes.route('/games/view')
def games_view():
    return render_template('games_view.html')

@game_routes.route('/games/add')
def games_add():
    return render_template('games_add.html')

@game_routes.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully!'})
