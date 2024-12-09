from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialiser Flask-appen
app = Flask(__name__)

# Database-konfigurasjon
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser databasen
db = SQLAlchemy(app)

# Importer routes
from routes.game_routes import game_routes

# Registrer Blueprint for games
app.register_blueprint(game_routes)

# Start applikasjonen
if __name__ == '__main__':
    app.run(debug=True, port = 47829)
