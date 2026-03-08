from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from pdfminer.high_level import extract_text

app = Flask(__name__)

# -------------------------------
# Secret Key (use environment variable on Render)
# -------------------------------
app.secret_key = os.environ.get("SECRET_KEY", "spiea_secret_key")

# -------------------------------
# Upload folder
# -------------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------
# Database auto-create if missing
# -------------------------------
DB_FILE = "spiea.db"
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        cgpa REAL,
        skills INTEGER,
        score REAL,
        prediction TEXT
    )
    """)
    conn.close()

# -------------------------------
# Database connection
# -------------------------------
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# -------------------------------
# Resume Skill Extraction
# -------------------------------
def analyze_resume(filepath):
    text = extract_text(filepath).lower()
    skills_list = [
        "python", "java", "sql", "machine learning",
        "html", "css", "javascript", "flask",
        "django", "react", "data analysis"
    ]
    score = sum(1 for skill in skills_list if skill in text)
    return min(score, 10)

# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["user_id"] = user["id"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        name = request.form["name"]
        cgpa = float(request.form["cgpa"])
        skills = int(request.form["skills"])

        resume_file = request.files.get("resume")
        if resume_file and resume_file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, resume_file.filename)
            resume_file.save(filepath)
            detected_skills = analyze_resume(filepath)
            skills = max(skills, detected_skills)

        score = (cgpa * 10) * 0.6 + (skills * 10) * 0.4
        if score > 75:
            result = "High Placement Chance"
        elif score > 50:
            result = "Moderate Chance"
        else:
            result = "Low Placement Chance"

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (user_id,name,cgpa,skills,score,prediction)
            VALUES (?,?,?,?,?,?)
        """, (session["user_id"], name, cgpa, skills, score, result))
        conn.commit()
        conn.close()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE user_id=?", (session["user_id"],))
    records = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", records=records)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------------------------------
# Run app on Render
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)