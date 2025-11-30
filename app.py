from flask import Flask, jsonify, request, render_template
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Data directory
DATA_DIR = 'data'
DB_FILE = os.path.join(DATA_DIR, 'liftlevel.db')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Database connection helper
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row 
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

# Helper functions for XP and leveling
def calculate_xp(weight, reps, sets):
    """Calculate XP: weight * reps * sets / 10"""
    return int((weight * reps * sets) / 10)

def calculate_level(xp):
    """Calculate level based on XP. Level 1: 0-999, Level 2: 1000-1999, etc."""
    return (xp // 1000) + 1

def get_xp_progress(xp, level):
    """Get XP progress for current level"""
    xp_for_current_level = (level - 1) * 1000
    xp_in_current_level = xp - xp_for_current_level
    xp_needed_for_next = 1000
    return {
        'current': xp_in_current_level,
        'needed': xp_needed_for_next,
        'percentage': min(100, (xp_in_current_level / xp_needed_for_next) * 100)
    }

# Database helper functions
def get_user_data():
    """Get user data from database"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data WHERE id = 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def update_user_data(total_xp, level):
    """Update user data in database"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE user_data SET total_xp = ?, level = ? WHERE id = 1', (total_xp, level))
    conn.commit()
    conn.close()

def get_exercises():
    """Get all exercises from database"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exercises ORDER BY id')
    exercises = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return exercises

def add_workout_to_history(exercise_id, exercise_name, weight, reps, sets, xp_earned):
    """Add a workout to history"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workout_history (exercise_id, exercise_name, weight, reps, sets, xp_earned, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (exercise_id, exercise_name, weight, reps, sets, xp_earned, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_workout_history(limit=10):
    """Get workout history from database"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workout_history ORDER BY timestamp DESC LIMIT ?', (limit,))
    workouts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return workouts

@app.route('/')
def index():
    """Main page - render the workout tracking interface"""
    user_data = get_user_data()
    exercises = get_exercises()
    workout_history = get_workout_history(10)
    xp_progress = get_xp_progress(user_data['total_xp'], user_data['level'])
    
    return render_template('index.html',
                         user_data=user_data,
                         exercises=exercises,
                         workout_history=workout_history,
                         xp_progress=xp_progress)

@app.route('/api/log-workout', methods=['POST'])
def log_workout():
    """API endpoint to log a workout"""
    data = request.json
    exercise_id = data.get('exercise_id')
    weight = float(data.get('weight', 0))
    reps = int(data.get('reps', 0))
    sets = int(data.get('sets', 0))
    
    # Calculate XP
    xp_earned = calculate_xp(weight, reps, sets)
    
    # Get current user data
    user_data = get_user_data()
    old_level = user_data['level']
    
    # Update XP and level
    new_total_xp = user_data['total_xp'] + xp_earned
    new_level = calculate_level(new_total_xp)
    update_user_data(new_total_xp, new_level)
    
    # Get exercise name
    exercises = get_exercises()
    exercise_name = next((ex['name'] for ex in exercises if ex['id'] == exercise_id), 'Unknown')
    
    # Add to workout history
    add_workout_to_history(exercise_id, exercise_name, weight, reps, sets, xp_earned)
    
    xp_progress = get_xp_progress(new_total_xp, new_level)
    
    return jsonify({
        'success': True,
        'xp_earned': xp_earned,
        'total_xp': new_total_xp,
        'level': new_level,
        'leveled_up': new_level > old_level,
        'xp_progress': xp_progress
    })

@app.route('/api/user-data', methods=['GET'])
def get_user_data_api():
    """API endpoint to get user data"""
    user_data = get_user_data()
    xp_progress = get_xp_progress(user_data['total_xp'], user_data['level'])
    
    return jsonify({
        'total_xp': user_data['total_xp'],
        'level': user_data['level'],
        'xp_progress': xp_progress
    })

@app.route('/api/reset-character', methods=['POST'])
def reset_character():
    """API endpoint to reset character (XP, level, and workout history)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Reset user data
    cursor.execute('UPDATE user_data SET total_xp = 0, level = 1 WHERE id = 1')
    
    # Clear workout history
    cursor.execute('DELETE FROM workout_history')
    
    conn.commit()
    conn.close()
    
    # Get updated data
    user_data = get_user_data()
    xp_progress = get_xp_progress(user_data['total_xp'], user_data['level'])
    
    return jsonify({
        'success': True,
        'total_xp': 0,
        'level': 1,
        'xp_progress': xp_progress
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
