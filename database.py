import sqlite3
from datetime import datetime

DB_NAME = "pets.db"

# -------------------------
# Database Setup
# -------------------------
def get_connection():
    """Create and return a DB connection."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """Initialize tables if they don’t exist."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Users
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE
        )
        """)

        # Pets
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT DEFAULT 'VirtualPet',
            hunger REAL DEFAULT 50,
            happiness REAL DEFAULT 50,
            energy REAL DEFAULT 50,
            health REAL DEFAULT 100,
            neglect_count INTEGER DEFAULT 0,
            self_destructive_index REAL DEFAULT 1.0,
            last_updated TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        # Pet History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            description TEXT,
            timestamp TEXT,
            pet_id INTEGER,
            FOREIGN KEY (pet_id) REFERENCES pets(id)
        )
        """)

        # Add default user if none exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", 
                           ("player1", "player1@example.com"))
            print("✅ Default user added: player1")

        conn.commit()
        print("✅ Database initialized successfully.")

# -------------------------
# Helper Functions
# -------------------------
def add_pet(name, species="VirtualPet", user_id=1):
    """Add a new pet and return its ID."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pets (name, species, hunger, happiness, energy, health, neglect_count, self_destructive_index, last_updated, user_id)
                VALUES (?, ?, 50, 50, 50, 100, 0, 1.0, ?, ?)
            """, (name, species, datetime.now().isoformat(), user_id))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"❌ Error adding pet: {e}")
        return None

def update_pet(pet_id, state):
    """Update pet state (dict expected)."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pets
                SET hunger=?, happiness=?, energy=?, health=?, neglect_count=?, self_destructive_index=?, last_updated=?
                WHERE id=?
            """, (
                state.get("hunger", 50), 
                state.get("happiness", 50), 
                state.get("energy", 50), 
                state.get("health", 100), 
                state.get("neglect_count", 0), 
                state.get("self_destructive_index", 1.0), 
                datetime.now().isoformat(), 
                pet_id
            ))
            conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error updating pet: {e}")

def save_pet_action(pet_id, action, description=""):
    """Save an action in pet history."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pet_history (action, description, timestamp, pet_id)
                VALUES (?, ?, ?, ?)
            """, (action, description, datetime.now().isoformat(), pet_id))
            conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Error saving pet action: {e}")
