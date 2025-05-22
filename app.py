from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key!


def get_db():
    conn = sqlite3.connect('csquiz.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


# ===== HOMEPAGE & LEADERBOARD =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leaderboard')
def leaderboard():
    conn = get_db()
    top_users = conn.execute('''
        SELECT username, score FROM users
        ORDER BY score DESC
        LIMIT 10
    ''').fetchall()
    conn.close()
    return render_template('leaderboard.html', users=top_users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('profile'))
        else:
            return "Invalid credentials!", 401
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists!", 400
        finally:
            conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

# ===== TRIVIA GAME ROUTES =====
@app.route('/play')
def play():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('play_menu.html', categories=categories)

@app.route('/start_game', methods=['POST'])
def start_game():
    category_id = request.form.get('category_id')
    level = request.form.get('level')

    query_params = {}
    if category_id:
        query_params['category_id'] = category_id
    if level:
        query_params['level'] = level

    return redirect(url_for('game') + '?' + '&'.join(f"{k}={v}" for k, v in query_params.items()))

@app.route('/game')
def game():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('play.html')


@app.route('/get_question')
def get_question():
    category_id = request.args.get('category_id')
    level = request.args.get('level')

    conn = get_db()
    query = '''
        SELECT q.*, c.name AS category_name 
        FROM questions q
        JOIN categories c ON q.category_id = c.id
        WHERE 1 = 1
    '''
    params = []

    if category_id:
        query += ' AND q.category_id = ?'
        params.append(category_id)
    if level:
        query += ' AND q.level = ?'
        params.append(level)

    query += ' ORDER BY RANDOM() LIMIT 1'
    question = conn.execute(query, params).fetchone()
    conn.close()

    if not question:
        return jsonify({"error": "No questions available"}), 404

    question_dict = dict(question)
    question_dict['wrong_answers'] = json.loads(question['wrong_answers'])
    return jsonify(question_dict)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get('answer')
    question_id = data.get('question_id')
    
    conn = get_db()
    try:
        
        correct_answer = conn.execute(
            'SELECT correct_answer FROM questions WHERE id = ?',
            (question_id,)
        ).fetchone()['correct_answer']
        
        
        if user_answer == correct_answer:
            conn.execute(
                'UPDATE users SET score = score + 10 WHERE id = ?',
                (session['user_id'],)
            )
            conn.commit()
            return jsonify({"correct": True})
        else:
            return jsonify({"correct": False})
    finally:
        conn.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/hangman')
def hangman():
    return render_template('hangman.html')

if __name__ == '__main__':
    app.run(debug=True)