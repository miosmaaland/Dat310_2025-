import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database
conn = sqlite3.connect('csquiz.db')
c = conn.cursor()

# ===== TABLES =====
# Users table (login + profile)
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        profile_image TEXT DEFAULT 'default.jpg',
        score INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0
    )
''')

# Categories (formerly "series")
c.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
''')

# Questions table with levels
c.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        wrong_answers TEXT NOT NULL, -- JSON: ["ans1", "ans2", "ans3"]
        category_id INTEGER NOT NULL,
        level INTEGER NOT NULL, -- 1 = Easy, 2 = Medium, 3 = Hard
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
''')

# User achievements
c.execute('''
    CREATE TABLE IF NOT EXISTS user_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        achievement TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# ===== SEED DATA =====

# Admin/test user
hashed_password = generate_password_hash('test123')
c.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', ('quiz_master', hashed_password, 1))

# Categories
categories = [
    ('Networking', 'Questions about networks, protocols, and internet basics'),
    ('Security', 'Covers cybersecurity, encryption, and safe computing'),
    ('Development', 'Programming languages, concepts, and practices'),
    ('System Engineering', 'Operating systems, architecture, and file systems'),
    ('Databases', 'SQL, NoSQL, and data modeling')
]
c.executemany('INSERT INTO categories (name, description) VALUES (?, ?)', categories)

# Sample questions
questions = [
    # Networking (Easy)
    ("What does HTTP stand for?", "HyperText Transfer Protocol", '["HyperText Transmission Protocol", "HighText Transfer Protocol", "HyperTool Transfer Protocol"]', 1, 1),
    ("Which device connects different networks together?", "Router", '["Switch", "Modem", "Repeater"]', 1, 1),
    
    # Security (Medium)
    ("What is the main goal of a firewall?", "To block unauthorized access", '["To increase internet speed", "To store passwords", "To manage bandwidth"]', 2, 2),
    ("What does 'phishing' refer to?", "Fraudulent attempts to obtain sensitive data", '["Catching software bugs", "Scanning ports", "Encrypting files"]', 2, 2),
    
    # Development (Easy)
    ("What does 'HTML' stand for?", "HyperText Markup Language", '["HighText Markdown Language", "HyperTransfer Markup Language", "Hyperlink Text Mark Language"]', 3, 1),
    ("Which language is primarily used for styling web pages?", "CSS", '["JavaScript", "Python", "HTML"]', 3, 1),

    # System Engineering (Hard)
    ("Which of the following is a Linux package manager?", "apt", '["brew", "exe", "iso"]', 4, 3),
    ("What is a kernel in an operating system?", "The core component managing system resources", '["An antivirus program", "A bootloader", "A BIOS replacement"]', 4, 3),

    # Databases (Medium)
    ("Which SQL keyword is used to retrieve data?", "SELECT", '["GET", "FETCH", "QUERY"]', 5, 2),
    ("Which database is known for storing data in JSON format?", "MongoDB", '["MySQL", "PostgreSQL", "SQLite"]', 5, 2),
]

c.executemany('''
    INSERT INTO questions (question, correct_answer, wrong_answers, category_id, level)
    VALUES (?, ?, ?, ?, ?)
''', questions)

conn.commit()
conn.close()
