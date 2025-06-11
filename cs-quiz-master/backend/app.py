from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import re
import json
import random


app = Flask(__name__, static_folder='static/vue', static_url_path='')
app.secret_key = 'your_secret_key_here'

CORS(app, supports_credentials=True, origins=[
    "http://localhost:8080",
    "http://192.168.1.158:8080", 
    "http://localhost:5173"
])

def get_db():
    conn = sqlite3.connect('csquiz.db')
    conn.row_factory = sqlite3.Row
    return conn


UPLOAD_FOLDER = os.path.join(app.static_folder, '../profile_images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = user['is_admin']
        return jsonify({
            "success": True,
            "user_id": user['id'],
            "username": user['username'],
            "is_admin": user['is_admin']
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password_raw = data.get('password', '')

    
    if not username or len(username) < 3 or len(username) > 20:
        return jsonify({"error": "Username must be 3-20 characters."}), 400
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({"error": "Username can only contain letters, numbers, and underscores."}), 400

    
    if not email or not re.match(r'^[^@\s]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({"error": "Please enter a valid email address."}), 400

    
    if not password_raw or len(password_raw) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400
    if not any(char.isdigit() for char in password_raw):
        return jsonify({"error": "Password must contain at least one number."}), 400
    if not any(char.isalpha() for char in password_raw):
        return jsonify({"error": "Password must contain at least one letter."}), 400
    if re.search(r'\s', password_raw):
        return jsonify({"error": "Password cannot contain spaces."}), 400

    password = generate_password_hash(password_raw)
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username, email, password, score) VALUES (?, ?, ?, 0)',
                     (username, email, password))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "User created."}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Username or email already exists"}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"}), 200

@app.route('/api/user/theme', methods=['GET'])
def get_theme():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    user = conn.execute('SELECT theme FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    if user:
        return jsonify({'theme': user['theme']})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/api/user/theme', methods=['POST'])
def set_theme():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    theme = data.get('theme')
    if theme not in ['light', 'dark']:
        return jsonify({'error': 'Invalid theme'}), 400
    conn = get_db()
    conn.execute('UPDATE users SET theme = ? WHERE id = ?', (theme, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'theme': theme})

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT id, username, is_admin FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify({'id': user['id'], 'username': user['username'], 'is_admin': user['is_admin']})
    else:
        return jsonify({'error': 'User not found'}), 404



@app.route('/api/user/profile_image', methods=['POST'])
def upload_profile_image():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(f"user_{session['user_id']}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        conn = get_db()
        conn.execute('UPDATE users SET profile_image = ? WHERE id = ?', (filename, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'profile_image': f"/static/profile_images/{filename}"})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/user/profile_image', methods=['GET'])
def get_profile_image():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    user = conn.execute('SELECT profile_image FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    if user and user['profile_image']:
        return jsonify({'profile_image': f"/static/profile_images/{user['profile_image']}"})
    return jsonify({'profile_image': '/default.jpg'})

@app.route('/static/profile_images/<filename>')
def serve_profile_image(filename):
    
    return send_from_directory(os.path.join(app.static_folder, '../profile_images'), filename)



@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    conn = get_db()
    users = conn.execute('SELECT id, username, score FROM users ORDER BY score DESC').fetchall()
    result = []
    for user in users:
        achievements = conn.execute('''
            SELECT a.name FROM achievements a
            JOIN user_achievements ua ON a.id = ua.achievement_id
            WHERE ua.user_id = ?
        ''', (user['id'],)).fetchall()
        achievement_names = [a['name'] for a in achievements]
        result.append({
            "username": user["username"],
            "score": user["score"],
            "achievements": achievement_names
        })
    conn.close()
    return jsonify(result)



@app.route('/api/skip', methods=['POST'])
def skip_question():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    conn.execute('UPDATE users SET score = score - 5 WHERE id = ?', (session['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Skipped question, -5 points'})



@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    categories = conn.execute('SELECT id, name FROM categories').fetchall()
    conn.close()
    return jsonify([{'id': c['id'], 'name': c['name']} for c in categories])

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    question_id = data.get('question_id')
    answer = data.get('answer')
    conn = get_db()
    user_id = session['user_id']
    question = conn.execute('SELECT * FROM questions WHERE id = ?', (question_id,)).fetchone()
    session['streak'] = session.get('streak', 0)
    session['categories_answered'] = session.get('categories_answered', [])
    if question:
        correct_answer = question['correct_answer']
        if correct_answer.strip().lower() == answer.strip().lower():
            conn.execute('UPDATE users SET score = score + 10 WHERE id = ?', (user_id,))
            conn.commit()
            user = conn.execute('SELECT score FROM users WHERE id = ?', (user_id,)).fetchone()
            new_score = user['score']
            
            already = conn.execute('SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=1', (user_id,)).fetchone()
            if not already:
                conn.execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', (user_id, 1))
            
            if new_score >= 100:
                already = conn.execute('SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=2', (user_id,)).fetchone()
                if not already:
                    conn.execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', (user_id, 2))
            
            if new_score >= 500:
                already = conn.execute('SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=3', (user_id,)).fetchone()
                if not already:
                    conn.execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', (user_id, 3))
            
            if new_score >= 1000:
                already = conn.execute('SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=5', (user_id,)).fetchone()
                if not already:
                    conn.execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', (user_id, 5))
        
            session['streak'] = session.get('streak', 0) + 1
            if session['streak'] == 5:
                already = conn.execute('SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=4', (user_id,)).fetchone()
                if not already:
                    conn.execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', (user_id, 4))
            if session['streak'] == 10:
                already = conn.execute('SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=7', (user_id,)).fetchone()
                if not already:
                    conn.execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', (user_id, 7))
            
            categories = conn.execute('SELECT id FROM categories').fetchall()
            cat_ids = [cat['id'] for cat in categories]
            categories_answered = session.get('categories_answered', [])
            if question['category_id'] not in categories_answered:
                categories_answered.append(question['category_id'])
            session['categories_answered'] = categories_answered
            if len(set(categories_answered)) == len(cat_ids):
                already = conn.execute('SELECT 1 FROM user_achievements WHERE user_id=? AND achievement_id=6', (user_id,)).fetchone()
                if not already:
                    conn.execute('INSERT INTO user_achievements (user_id, achievement_id) VALUES (?, ?)', (user_id, 6))
            conn.commit()
            conn.close()
            return jsonify({'correct': True, 'correct_answer': correct_answer, 'message': 'Correct answer!'})
        else:
            session['streak'] = 0
            conn.close()
            return jsonify({'correct': False, 'correct_answer': correct_answer})
    conn.close()
    return jsonify({'correct': False, 'correct_answer': None, 'error': 'Question not found'})

@app.route('/api/user/achievements', methods=['GET'])
def get_user_achievements():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    achievements = conn.execute('''
        SELECT a.id, a.name, a.description
        FROM achievements a
        JOIN user_achievements ua ON a.id = ua.achievement_id
        WHERE ua.user_id = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return jsonify([{'id': a['id'], 'name': a['name'], 'description': a['description']} for a in achievements])


@app.route('/api/question', methods=['GET'])
def get_random_question():
    category = request.args.get('category')
    level = request.args.get('level')
    conn = get_db()
    query = 'SELECT * FROM questions'
    params = []
    conditions = []
    if category:
        conditions.append('category_id = ?')
        params.append(int(category))
    if level:
        conditions.append('level = ?')
        params.append(int(level))
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    query += ' ORDER BY RANDOM() LIMIT 1'
    question = conn.execute(query, params).fetchone()
    conn.close()
    if question:
        wrong_answers = json.loads(question['wrong_answers'])
        options = wrong_answers + [question['correct_answer']]
        random.shuffle(options)
        labels = ['A', 'B', 'C', 'D']
        labeled_options = dict(zip(labels, options))
        return jsonify({
            'id': question['id'],
            'question': question['question'],
            'options': labeled_options
        })
    return jsonify({'error': 'No questions available'})




@app.route('/api/questions', methods=['GET'])
def get_all_questions():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    user = conn.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not user or user['is_admin'] != 1:
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    result = []
    for q in questions:
        result.append({
            'id': q['id'],
            'question': q['question'],
            'correct_answer': q['correct_answer'],
            'wrong_answers': json.loads(q['wrong_answers']),
            'category_id': q['category_id'],
            'level': q['level']
        })
    return jsonify(result)

@app.route('/api/questions', methods=['POST'])
def create_question():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    user = conn.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not user or user['is_admin'] != 1:
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403
    data = request.json
    question = data.get('question', '').strip()
    correct_answer = data.get('correct_answer', '').strip()
    wrong_answers = data.get('wrong_answers', [])
    category_id = data.get('category_id')
    level = data.get('level')
    
    if not question or not correct_answer or not wrong_answers or not category_id or not level:
        conn.close()
        return jsonify({'error': 'All fields are required.'}), 400
    if not isinstance(wrong_answers, list) or len(wrong_answers) != 3:
        conn.close()
        return jsonify({'error': 'Exactly 3 wrong answers required.'}), 400
    if correct_answer in wrong_answers:
        conn.close()
        return jsonify({'error': 'Wrong answers cannot match the correct answer.'}), 400
    if len(set(wrong_answers)) != 3:
        conn.close()
        return jsonify({'error': 'Wrong answers must be unique.'}), 400
    if not str(level).isdigit() or int(level) not in [1,2,3]:
        conn.close()
        return jsonify({'error': 'Level must be 1, 2, or 3.'}), 400
    if not str(category_id).isdigit() or int(category_id) < 1:
        conn.close()
        return jsonify({'error': 'Category ID must be a positive integer.'}), 400
    conn.execute(
        'INSERT INTO questions (question, correct_answer, wrong_answers, category_id, level) VALUES (?, ?, ?, ?, ?)',
        (question, correct_answer, json.dumps(wrong_answers), category_id, level)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True}), 201

@app.route('/api/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    user = conn.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not user or user['is_admin'] != 1:
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403
    data = request.json
    question = data.get('question', '').strip()
    correct_answer = data.get('correct_answer', '').strip()
    wrong_answers = data.get('wrong_answers', [])
    category_id = data.get('category_id')
    level = data.get('level')
    
    if not question or not correct_answer or not wrong_answers or not category_id or not level:
        conn.close()
        return jsonify({'error': 'All fields are required.'}), 400
    if not isinstance(wrong_answers, list) or len(wrong_answers) != 3:
        conn.close()
        return jsonify({'error': 'Exactly 3 wrong answers required.'}), 400
    if correct_answer in wrong_answers:
        conn.close()
        return jsonify({'error': 'Wrong answers cannot match the correct answer.'}), 400
    if len(set(wrong_answers)) != 3:
        conn.close()
        return jsonify({'error': 'Wrong answers must be unique.'}), 400
    if not str(level).isdigit() or int(level) not in [1,2,3]:
        conn.close()
        return jsonify({'error': 'Level must be 1, 2, 3, 4 or 5.'}), 400
    if not str(category_id).isdigit() or int(category_id) < 1:
        conn.close()
        return jsonify({'error': 'Category ID must be a positive integer.'}), 400
    conn.execute(
        'UPDATE questions SET question=?, correct_answer=?, wrong_answers=?, category_id=?, level=? WHERE id=?',
        (question, correct_answer, json.dumps(wrong_answers), category_id, level, question_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db()
    user = conn.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    if not user or user['is_admin'] != 1:
        conn.close()
        return jsonify({'error': 'Forbidden'}), 403
    conn.execute('DELETE FROM questions WHERE id=?', (question_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})



@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)