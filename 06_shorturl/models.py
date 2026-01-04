import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = 'database.db'

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
                CREATE TABLE IF NOT EXISTS urls(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     original_url TEXT NOT NULL,
                     short_code TEXT UNIQUE NOT NULL,
                     visit_count INTEGER DEFAULT 0
                     )
            ''')
        conn.execute('''
                CREATE TABLE IF NOT EXISTS users(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT UNIQUE NOT NULL,
                     password_hash TEXT NOT NULL,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )
            ''')
        
def insert_url(original_url, short_code):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT into urls (original_url, short_code)
                     VALUES (?, ?)
        ''', (original_url, short_code))

def get_url(short_code):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute('SELECT * FROM urls WHERE short_code = ?',
        (short_code,))
        return cur.fetchone()
    
def increment_count(short_code):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            UPDATE urls
            SET visit_count = visit_count + 1
            WHERE short_code = ?
        ''', (short_code,))

def get_all_url():
     with sqlite3.connect(DB_NAME) as conn:
         cur = conn.execute('SELECT original_url, short_code, visit_count FROM urls ORDER by id DESC')
         return cur.fetchall()
    
def delete_url_by_code(short_code):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('DELETE from urls WHERE short_code = ?', (short_code,))

# User authentication functions
def create_user(username, password):
    """Create a new user with hashed password"""
    password_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
            ''', (username, password_hash))
            return True
    except sqlite3.IntegrityError:
        return False  # Username already exists

def get_user_by_username(username):
    """Get user by username"""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
        return cur.fetchone()

def verify_user(username, password):
    """Verify user credentials"""
    user = get_user_by_username(username)
    if user and check_password_hash(user[2], password):
        return {'id': user[0], 'username': user[1]}
    return None
