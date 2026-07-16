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
        cursor = db.cursor()
        
        # Check if chat_messages table exists and does NOT have chat_id column
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_messages'")
        table_exists = cursor.fetchone()
        
        has_chat_id = False
        if table_exists:
            cursor.execute("PRAGMA table_info(chat_messages)")
            columns = cursor.fetchall()
            has_chat_id = any(col['name'] == 'chat_id' for col in columns)
        
        # If legacy table exists (no chat_id), let's rename it to migrate it
        if table_exists and not has_chat_id:
            db.execute("ALTER TABLE chat_messages RENAME TO legacy_chat_messages")
        
        # Create chats table
        db.execute(
            '''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            '''
        )
        
        # Create new chat_messages table
        db.execute(
            '''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
            )
            '''
        )
        
        # If we had legacy messages, migrate them
        if table_exists and not has_chat_id:
            cursor.execute("SELECT COUNT(*) FROM legacy_chat_messages")
            legacy_count = cursor.fetchone()[0]
            if legacy_count > 0:
                # Create a default chat for the legacy messages
                now = datetime.utcnow().isoformat()
                cursor.execute(
                    "INSERT INTO chats (title, created_at) VALUES (?, ?)",
                    ("Imported Chat", now)
                )
                chat_id = cursor.lastrowid
                
                # Copy messages
                cursor.execute(
                    f"INSERT INTO chat_messages (chat_id, sender, message, created_at) SELECT {chat_id}, sender, message, created_at FROM legacy_chat_messages"
                )
            
            db.execute("DROP TABLE legacy_chat_messages")
            
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


@app.route('/api/chats')
def list_chats():
    db = get_db()
    rows = db.execute(
        'SELECT id, title, created_at FROM chats ORDER BY id DESC'
    ).fetchall()
    return jsonify({'chats': [
        {'id': row['id'], 'title': row['title'], 'created_at': row['created_at']}
        for row in rows
    ]})


@app.route('/api/chats', methods=['POST'])
def create_chat():
    now = datetime.utcnow().isoformat()
    db = get_db()
    cursor = db.execute(
        'INSERT INTO chats (title, created_at) VALUES (?, ?)',
        ('New Chat', now)
    )
    db.commit()
    chat_id = cursor.lastrowid
    return jsonify({'id': chat_id, 'title': 'New Chat', 'created_at': now})


@app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    db = get_db()
    db.execute('DELETE FROM chats WHERE id = ?', (chat_id,))
    db.execute('DELETE FROM chat_messages WHERE chat_id = ?', (chat_id,))
    db.commit()
    return jsonify({'success': True})


@app.route('/api/chats/<int:chat_id>/messages')
def get_chat_messages(chat_id):
    db = get_db()
    rows = db.execute(
        'SELECT sender, message, created_at FROM chat_messages WHERE chat_id = ? ORDER BY id ASC',
        (chat_id,)
    ).fetchall()
    return jsonify({'messages': [
        {'sender': row['sender'], 'message': row['message'], 'created_at': row['created_at']}
        for row in rows
    ]})


@app.route('/api/history')
def history():
    db = get_db()
    latest_chat = db.execute('SELECT id FROM chats ORDER BY id DESC LIMIT 1').fetchone()
    if not latest_chat:
        return jsonify({'messages': []})
    
    rows = db.execute(
        'SELECT sender, message, created_at FROM chat_messages WHERE chat_id = ? ORDER BY id ASC',
        (latest_chat['id'],)
    ).fetchall()
    return jsonify({'messages': [
        {'sender': row['sender'], 'message': row['message'], 'created_at': row['created_at']}
        for row in rows
    ]})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_input = (data.get('message') or '').strip()
    chat_id = data.get('chat_id')

    if not user_input:
        return jsonify({'reply': 'Please enter a message.'})

    db = get_db()
    if not chat_id:
        latest = db.execute('SELECT id FROM chats ORDER BY id DESC LIMIT 1').fetchone()
        if latest:
            chat_id = latest['id']
        else:
            now = datetime.utcnow().isoformat()
            cursor = db.execute(
                'INSERT INTO chats (title, created_at) VALUES (?, ?)',
                ('New Chat', now)
            )
            chat_id = cursor.lastrowid

    reply = get_response(user_input)
    now = datetime.utcnow().isoformat()

    chat_info = db.execute('SELECT title FROM chats WHERE id = ?', (chat_id,)).fetchone()
    if chat_info and chat_info['title'] == 'New Chat':
        title = user_input[:30] + '...' if len(user_input) > 30 else user_input
        title = title.capitalize()
        db.execute('UPDATE chats SET title = ? WHERE id = ?', (title, chat_id))

    db.execute(
        'INSERT INTO chat_messages (chat_id, sender, message, created_at) VALUES (?, ?, ?, ?)',
        (chat_id, 'user', user_input, now),
    )
    db.execute(
        'INSERT INTO chat_messages (chat_id, sender, message, created_at) VALUES (?, ?, ?, ?)',
        (chat_id, 'bot', reply, now),
    )
    db.commit()

    return jsonify({'reply': reply, 'chat_id': chat_id})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

