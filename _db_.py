import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database
conn = sqlite3.connect('trivia.db')
c = conn.cursor()

# ===== TABLES =====
# Users table (for login)
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        profile_image TEXT DEFAULT 'default.jpg',
        score INTEGER DEFAULT 0
    )
''')

# Series table (existing)
c.execute('''
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        genre TEXT NOT NULL,
        platform TEXT NOT NULL
    )
''')

# Trivia questions table (new!)
c.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        wrong_answers TEXT NOT NULL,  -- JSON array: ["ans1", "ans2", "ans3"]
        series_id INTEGER,
        episode TEXT,
        FOREIGN KEY (series_id) REFERENCES series(id)
    )
''')

# User achievements (new!)
c.execute('''
    CREATE TABLE IF NOT EXISTS user_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        achievement TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# ===== SEED DATA =====
# Add a test user
hashed_password = generate_password_hash('test123')
c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('quiz_master', hashed_password))

# Add sample series
series = [
    ('game of thrones', 'action', 'hbo'),
    ('stranger things', 'horror', 'netflix'),
    ('the office', 'comedy', 'netflix'),
    ('breaking bad', 'drama', 'netflix'),
    ('friends', 'comedy', 'hbo'),
    ('the mandalorian', 'sci-fi', 'disney'),
    ('the witcher', 'fantasy', 'netflix'),
    ('the boys', 'action', 'amazon'),
    ('chernobyl', 'drama', 'hbo'),
    ('attack on titan', 'anime', 'netflix'),
    ('one piece', 'anime', 'hulu'),
    ('money heist', 'thriller', 'netflix'),
    ('true detective', 'thriller', 'hbo'),
    ('modern family', 'comedy', 'netflix'),
    ('westworld', 'sci-fi', 'hbo'),
    ('the handmaid\'s tale', 'drama', 'hulu'),
    ('the marvelous mrs. maisel', 'comedy', 'amazon prime'),
    ('the big bang theory', 'comedy', 'netflix'),
]
c.executemany('INSERT INTO series (name, genre, platform) VALUES (?, ?, ?)', series)

# Add sample questions
questions = [
    # Game of Thrones
    ("What is the name of Jon Snow's direwolf?", "Ghost", '["Grey Wind", "Nymeria", "Summer"]', 1, "Season 1"),
    ("Who kills the Night King?", "Arya Stark", '["Jon Snow", "Daenerys Targaryen", "Bran Stark"]', 1, "Season 8"),
    # Stranger Things
    ("What is the name of the alternate dimension in Stranger Things?", "The Upside Down", '["The Void", "The Nether", "The Other Side"]', 2, "Season 1"),
    ("Who is Eleven's real name?", "Jane Hopper", '["El Hopper", "Jane Byers", "El Byers"]', 2, "Season 1"),
    # The Office
    ("What is Michael Scott's famous catchphrase?", "That's what she said", '["Boom, roasted", "I declare bankruptcy", "Dwight, you ignorant slut"]', 3, "Season 2"),
    ("Who does Jim marry?", "Pam Beesly", '["Karen Filippelli", "Angela Martin", "Kelly Kapoor"]', 3, "Season 6"),
    # Breaking Bad
    ("What is Walter White's alias?", "Heisenberg", '["The Cook", "Mr. White", "The Danger"]', 4, "Season 2"),
    ("What is the name of Walter and Jesse's RV?", "The Crystal Ship", '["The Rolling Lab", "The Meth Mobile", "The Breaking Bad"]', 4, "Season 1"),
    # Friends
    ("What is Chandler Bing's job?", "Statistical Analysis and Data Reconfiguration", '["Advertising", "Lawyer", "Chef"]', 5, "Season 1"),
    ("What is the name of Ross's monkey?", "Marcel", '["George", "Kong", "Bongo"]', 5, "Season 1"),
    # The Mandalorian
    ("What is the name of the Child (Baby Yoda)?", "Grogu", '["Yaddle", "Yoda Jr.", "Mando Jr."]', 6, "Season 1"),
    ("What is the Mandalorian's real name?", "Din Djarin", '["Boba Fett", "Jango Fett", "Cara Dune"]', 6, "Season 1"),
    # The Witcher
    ("What is Geralt of Rivia's profession?", "Witcher", '["Sorcerer", "Knight", "Bard"]', 7, "Season 1"),
    ("Who sings 'Toss a Coin to Your Witcher'?", "Jaskier", '["Geralt", "Yennefer", "Ciri"]', 7, "Season 1"),
]
c.executemany('''
    INSERT INTO questions (question, correct_answer, wrong_answers, series_id, episode)
    VALUES (?, ?, ?, ?, ?)
''', questions)

conn.commit()
conn.close()