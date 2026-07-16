import os
import random
import sqlite3
from datetime import datetime

from flask import Flask, g, jsonify, render_template, request

app = Flask(__name__, template_folder='templates')
DB_PATH = os.path.join(os.path.dirname(__file__), 'chatbot.db')


def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        db.execute(
            '''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            '''
        )
        db.commit()


@app.before_request
def setup_db():
    get_db()


def get_response(user_input):
    user_input = user_input.strip().lower()

    if user_input in ['hi', 'hello', 'hey']:
        return 'Hello! How can I help you?'
    if user_input == 'how are you':
        return 'I am doing great!'
    if user_input == 'what is your name':
        return 'I am a Rule-Based AI Chatbot.'
    if user_input == 'who created you':
        return 'I was created by Vinay.'
    if user_input == 'what can you do':
        return 'I can answer simple questions, tell time, tell jokes, perform calculations, and more.'
    if user_input == 'time':
        return datetime.now().strftime('%H:%M:%S')
    if user_input in ['date', "today's date"]:
        return datetime.now().strftime('%d-%m-%Y')
    if user_input == 'day':
        return datetime.now().strftime('%A')
    if user_input == 'month':
        return datetime.now().strftime('%B')
    if user_input == 'joke':
        return 'Why do programmers prefer dark mode? Because light attracts bugs!'
    if user_input == 'quote':
        return 'Success is the sum of small efforts repeated day after day.'
    if user_input == 'fact':
        return 'Honey never spoils. Archaeologists have found edible honey thousands of years old!'
    if user_input == 'motivate me':
        return 'Believe in yourself! Every expert was once a beginner.'
    if user_input == 'dice':
        return f'You rolled a {random.randint(1, 6)}'
    if user_input == 'coin':
        return random.choice(['Heads', 'Tails'])
    if user_input == 'help':
        return (
            'Available commands:\n'
            'hi, hello, hey\n'
            'how are you\n'
            'what is your name\n'
            'who created you\n'
            'what can you do\n'
            'time\n'
            'date\n'
            "today's date\n"
            'day\n'
            'month\n'
            'joke\n'
            'quote\n'
            'fact\n'
            'motivate me\n'
            'dice\n'
            'coin\n'
            'help\n'
            'bye, exit, quit'
        )
    if user_input in ['bye', 'exit', 'quit']:
        return 'Goodbye! Have a nice day.'
    return "Sorry, I don't understand that. Type 'help' to see available commands."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/history')
def history():
    db = get_db()
    rows = db.execute(
        'SELECT sender, message, created_at FROM chat_messages ORDER BY id ASC'
    ).fetchall()
    return jsonify({'messages': [
        {'sender': row['sender'], 'message': row['message'], 'created_at': row['created_at']}
        for row in rows
    ]})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_input = (data.get('message') or '').strip()

    if not user_input:
        return jsonify({'reply': 'Please enter a message.'})

    reply = get_response(user_input)
    now = datetime.utcnow().isoformat()

    db = get_db()
    db.execute(
        'INSERT INTO chat_messages (sender, message, created_at) VALUES (?, ?, ?)',
        ('user', user_input, now),
    )
    db.execute(
        'INSERT INTO chat_messages (sender, message, created_at) VALUES (?, ?, ?)',
        ('bot', reply, now),
    )
    db.commit()

    return jsonify({'reply': reply})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
