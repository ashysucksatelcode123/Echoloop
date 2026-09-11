import os
import flask_socketio
from flask import Flask, send_file, request
from flask_socketio import SocketIO, send
import sqlite3

# Finds the attached files
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')

# Setting up Echoloop
app = Flask(__name__, template_folder=template_dir)
app.config['Secret Key'] = 'echolooploopecho'
socketio = SocketIO(app, cors_allowed_origins="*")

# Loading HTML process
from flask import send_from_directory

@app.route('/')
def index():
    return send_file('index.html')

# Handles live messages
@socketio.on('message')
def handle_message(msg):
    print(f"[Echoloop Server] Received message: {msg}")

    # Sends message to everyone on the app
    packet = {
        'text': msg,
        'sender-id': request.sid
    }
    send(packet, broadcast=True)

# Starts the server
if __name__ == '__main__':
    print("> Echoloop starting up...")
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)

def init_db():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    text TEXT
    )
  ''' )
    conn.commit()
    conn.close()

def save_message(sender, text):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (sender, text) VALUES (?, ?)', (sender, text))
    conn.commit()
    conn.close()

def get_all_messages():
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()
    cursor.execute('SELECT sender, text FROM messages')
    rows = cursor.fetchall()
    conn.close()

    return [{"sender": row[0], "text": row[1]} for row in rows]

init_db()