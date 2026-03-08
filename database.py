import sqlite3

conn = sqlite3.connect("spiea.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
name TEXT,
cgpa REAL,
skills INTEGER,
score REAL,
prediction TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")