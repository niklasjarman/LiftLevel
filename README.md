# 💪 LiftLevel - Strength Tracking App

A gamified workout tracking web application where users log workouts, earn experience points (XP), and level up their character with AI-generated evolution images.

![LiftLevel](https://img.shields.io/badge/LiftLevel-Strength%20Tracking-orange?style=for-the-badge)

## ✨ Features

- **Workout Logging**: Log exercises with weight, reps, and sets
- **XP System**: Earn XP based on workout intensity (XP = weight × reps × sets / 10)
- **Progressive Leveling**: Formula-based leveling system that gets progressively harder (Max Level: 10)
- **Character Evolution**: Unlock new AI-generated character images as you level up
- **Workout History**: Track your past workouts with detailed history
- **Reset Functionality**: Reset your character to start fresh
- **Beautiful UI**: Modern dark theme with orange accents

## 🛠️ Tech Stack

- **Backend**: Python 3.x + Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with dark theme (#1f1f1f background, #ff6d1f accent)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/niklasjarman/LiftLevel.git
cd LiftLevel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python3 app.py
```

The app will be available at `http://localhost:5000`

## 📖 How to Use

1. **Log a Workout**:
   - Select an exercise from the dropdown
   - Enter weight (lbs), reps, and sets
   - Click "Log Workout"
   - Earn XP based on your workout!

2. **Level Up**:
   - Each level requires progressively more XP
   - Level 1: 0-999 XP
   - Level 2: 1000-2499 XP
   - Level 3: 2500-4999 XP
   - And so on... (Formula: `XP = 1000 * (level - 1)^1.8`)
   - Max Level: 10

3. **Character Evolution**:
   - Your character image evolves as you level up
   - Each level unlocks a new, more impressive character design
   - Higher levels feature extravagant effects (gold, emerald, diamond)

4. **Reset Character**:
   - Click the "🔄 Reset" button in the header
   - Confirm to reset XP, level, and workout history

## 📁 Project Structure

```
LiftLevel/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── data/                 # Database storage
│   └── liftlevel.db      # SQLite database (auto-generated)
├── templates/            # HTML templates
│   └── index.html        # Main page template
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Stylesheet
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   └── images/           # Character evolution images
│       ├── level_1.png
│       ├── level_2.png
│       └── ...
└── IMAGE_PROMPTS.md      # AI image generation prompts
```

## 🎮 Leveling System

The leveling system uses a formula-based approach that gets progressively harder:

- **Formula**: `XP = 1000 * (level - 1)^1.8`
- **Max Level**: 10
- **XP Calculation**: `XP = (weight × reps × sets) / 10`

### Level Requirements

| Level | Total XP Required | XP Needed for Next Level |
|-------|------------------|-------------------------|
| 1     | 0                | 1,000                   |
| 2     | 1,000            | ~1,800                  |
| 3     | ~2,800           | ~2,400                  |
| 4     | ~5,200           | ~3,200                  |
| 5     | ~8,200           | ~4,200                  |
| 6     | ~12,400          | ~5,400                  |
| 7     | ~17,800          | ~6,800                  |
| 8     | ~24,600          | ~8,400                  |
| 9     | ~33,000          | ~10,200                 |
| 10    | ~43,200          | MAX LEVEL               |

## 🎨 Character Evolution

As you level up, your character evolves with increasingly impressive designs:

- **Levels 1-5**: Progressive muscle development from stick figure to superhero
- **Level 6**: Impossibly massive muscles
- **Level 7**: Extreme physique with bulging veins
- **Level 8**: Golden highlights and shimmering effects
- **Level 9**: Emerald green metallic sheen with glowing effects
- **Level 10**: Diamond and crystal muscles with prismatic light

## 🔧 API Endpoints

- `GET /` - Main application page
- `POST /api/log-workout` - Log a new workout
- `GET /api/user-data` - Get current user stats
- `POST /api/reset-character` - Reset character to Level 1

## 📝 Database Schema

### user_data
- `id` (INTEGER PRIMARY KEY)
- `total_xp` (INTEGER)
- `level` (INTEGER)

### exercises
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT)
- `category` (TEXT)

### workout_history
- `id` (INTEGER PRIMARY KEY)
- `exercise_id` (INTEGER)
- `exercise_name` (TEXT)
- `weight` (REAL)
- `reps` (INTEGER)
- `sets` (INTEGER)
- `xp_earned` (INTEGER)
- `timestamp` (TEXT)

## 🤖 AI Tools Used

This project was developed with assistance from AI tools:

- **Cursor**: Code generation, debugging, and UI design
- **DALL·E**: Character evolution images

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

**Niklas Jarman**

- GitHub: [@niklasjarman](https://github.com/niklasjarman)

## 🙏 Acknowledgments

- Character images generated using AI image generation tools
- Built with Flask and modern web technologies

---

**Level up your strength journey! 💪**

