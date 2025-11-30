from flask import Flask
import os
import sqlite3

app = Flask(__name__)

# Data directory
DATA_DIR = 'data'
DB_FILE = os.path.join(DATA_DIR, 'liftlevel.db')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Database connection helper
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This makes rows accessible like dictionaries
    return conn

# Initialize database and create tables
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create user_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1
        )
    ''')
    
    # Create exercises table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    # Create workout_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id INTEGER,
            exercise_name TEXT,
            weight REAL,
            reps INTEGER,
            sets INTEGER,
            xp_earned INTEGER,
            timestamp TEXT,
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        )
    ''')
    
    # Initialize user_data if empty
    cursor.execute('SELECT COUNT(*) as count FROM user_data')
    if cursor.fetchone()['count'] == 0:
        cursor.execute('INSERT INTO user_data (total_xp, level) VALUES (0, 1)')
    
    # Initialize exercises if empty
    cursor.execute('SELECT COUNT(*) as count FROM exercises')
    if cursor.fetchone()['count'] == 0:
        default_exercises = [
            ('Bench Press', 'Chest'),
            ('Squat', 'Legs'),
            ('Deadlift', 'Back'),
            ('Bicep Curls', 'Arms'),
            ('Shoulder Press', 'Shoulders'),
            ('Pull-ups', 'Back'),
            ('Leg Press', 'Legs'),
            ('Tricep Dips', 'Arms'),
            ('Lunges', 'Legs'),
            ('Rows', 'Back')
        ]
        cursor.executemany('INSERT INTO exercises (name, category) VALUES (?, ?)', default_exercises)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '<h1>LiftLevel App</h1><p>Backend test</p>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
