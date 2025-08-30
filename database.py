import sqlite3
# -------------------------
# Database Setup
# -------------------------
conn = sqlite3.connect("pets.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE
)
""")
# Create pets table (linked to users)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    species TEXT DEFAULT 'VirtualPet',
    hunger REAL DEFAULT 50,
    happiness REAL DEFAULT 50,
    energy REAL DEFAULT 50,
    last_updated TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Create pet_history table (linked to pets)
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

# -------------------------
# Add default user if none exists
# -------------------------
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", 
                   ("player1", "player1@example.com"))
    print("Default user added: player1")

conn.commit()
conn.close()

print("Database with users, pets, and pet_history tables created successfully!")
