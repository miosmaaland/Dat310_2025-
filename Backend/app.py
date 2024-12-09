from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database-konfigurasjon
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Spillmodell
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Not Completed')

# Opprett databasen
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([{
        'id': game.id,
        'name': game.name,
        'genre': game.genre,
        'release_date': game.release_date,
        'status': game.status
    } for game in games])

@app.route('/games', methods=['POST'])
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

@app.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    data = request.json
    game = Game.query.get_or_404(id)
    game.name = data.get('name', game.name)
    game.genre = data.get('genre', game.genre)
    game.release_date = data.get('release_date', game.release_date)
    game.status = data.get('status', game.status)
    db.session.commit()
    return jsonify({'message': 'Game updated successfully!'})



@app.route('/games/view')
def games_view():
    return render_template('games_view.html')

@app.route('/games/add')
def games_add():
    return render_template('games_add.html')


@app.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get_or_404(id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
