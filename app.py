from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from pathlib import Path
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "change-this-to-a-long-random-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "students.db"
MODEL_PATH = BASE_DIR / "model" / "career_model.json"
HANDWRITING_DIR = BASE_DIR / "handwriting_notes"


# ---------------- DATABASE ----------------

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                age INTEGER,
                education TEXT,
                college TEXT,
                graduation_year INTEGER,
                skills TEXT,
                experience TEXT
            )
        """)


init_db()


# ---------------- LOAD MODEL ----------------

if MODEL_PATH.exists():
    with open(MODEL_PATH, "r", encoding="utf-8") as file:
        model = json.load(file)
else:
    model = {"skills": [], "centroids": {}}


# ---------------- CAREER SKILLS ----------------

career_skills = {
    "Data Analyst": [
        "python", "sql", "excel", "power bi", "statistics"
    ],
    "Software Developer": [
        "java", "python", "sql", "git", "html", "css"
    ],
    "Data Scientist": [
        "python", "sql", "statistics", "machine learning", "pandas"
    ],
    "Frontend Developer": [
        "html", "css", "javascript", "react"
    ],
    "Backend Developer": [
        "python", "java", "node.js", "express", "sql", "api", "git"
    ],
    "Full Stack Developer": [
        "html", "css", "javascript", "react",
        "node.js", "express", "sql", "git"
    ],
    "Cybersecurity Analyst": [
        "networking", "linux", "cybersecurity",
        "security tools", "python"
    ],
    "Cloud Engineer": [
        "cloud", "aws", "linux", "networking", "docker", "git"
    ],
    "Mobile App Developer": [
        "java", "kotlin", "flutter", "dart", "android"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "git"
    ]
}


# ---------------- SKILL RECOMMENDATIONS ----------------

skill_recommendations = {
    "python": "Learn Python fundamentals and practice coding problems.",
    "sql": "Learn SQL queries, joins and database operations.",
    "excel": "Learn Excel formulas, Pivot Tables and data analysis.",
    "power bi": "Learn Power BI and create interactive dashboards.",
    "statistics": "Learn statistics and probability.",
    "java": "Learn Java programming and OOP concepts.",
    "git": "Learn Git commands and version control.",
    "html": "Learn HTML structure and forms.",
    "css": "Learn CSS styling and responsive design.",
    "javascript": "Learn JavaScript and DOM manipulation.",
    "react": "Learn React components, props and state.",
    "machine learning": "Learn Machine Learning fundamentals.",
    "pandas": "Learn Pandas for data analysis.",
    "node.js": "Learn Node.js for server-side development.",
    "express": "Learn Express.js and build REST APIs.",
    "api": "Learn REST API concepts and practice building APIs.",
    "networking": "Learn TCP/IP, DNS, ports and networking basics.",
    "linux": "Practice Linux commands and permissions.",
    "cybersecurity": "Learn cybersecurity fundamentals and safe lab practice.",
    "security tools": "Learn defensive security tools in authorized labs.",
    "cloud": "Learn cloud computing fundamentals.",
    "aws": "Learn AWS, IAM, EC2 and S3.",
    "docker": "Learn Docker images and containers.",
    "kotlin": "Learn Kotlin and Android app development.",
    "flutter": "Learn Flutter widgets and mobile UI.",
    "dart": "Learn Dart fundamentals.",
    "android": "Learn Android app structure and development."
}


# ---------------- HELPER FUNCTIONS ----------------

def profile_is_complete(student):
    return all([
        student["age"],
        student["education"],
        student["college"],
        student["graduation_year"],
        student["skills"]
    ])


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "student_id" not in session:
            flash("Please login to continue.", "error")
            return redirect(url_for("login"))
        return function(*args, **kwargs)
    return wrapper


def normalize_skills(skills):
    aliases = {
        "js": "javascript",
        "html5": "html",
        "css3": "css",
        "react.js": "react",
        "reactjs": "react",
        "node": "node.js",
        "nodejs": "node.js",
        "express.js": "express",
        "aws cloud": "aws",
        "amazon web services": "aws",
        "cyber security": "cybersecurity",
        "powerbi": "power bi",
        "machine-learning": "machine learning"
    }

    normalized = []

    for skill in skills:
        value = skill.strip().lower()
        value = aliases.get(value, value)

        if value and value not in normalized:
            normalized.append(value)

    return normalized


# ---------------- REGISTRATION ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not phone or not password:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("register"))

        if len(phone) != 10 or not phone.isdigit():
            flash("Enter a valid 10-digit phone number.", "error")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        try:
            with get_db_connection() as connection:
                connection.execute("""
                    INSERT INTO students
                    (name, email, phone, password_hash)
                    VALUES (?, ?, ?, ?)
                """, (name, email, phone, password_hash))

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("Email already registered. Please login.", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db_connection() as connection:
            student = connection.execute(
                "SELECT * FROM students WHERE email = ?",
                (email,)
            ).fetchone()

        if student and check_password_hash(
            student["password_hash"], password
        ):
            session.clear()
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]

            if profile_is_complete(student):
                return redirect(url_for("home"))

            return redirect(url_for("student_details"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("login"))


# ---------------- STUDENT DETAILS ----------------

@app.route("/student-details", methods=["GET", "POST"])
@login_required
def student_details():
    with get_db_connection() as connection:
        student = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (session["student_id"],)
        ).fetchone()

    if student is None:
        session.clear()
        return redirect(url_for("login"))

    if request.method == "GET" and profile_is_complete(student):
        return redirect(url_for("home"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        age_text = request.form.get("age", "").strip()
        education = request.form.get("education", "").strip()
        college = request.form.get("college", "").strip()
        year_text = request.form.get("graduation_year", "").strip()

        student_skills = ", ".join(
            normalize_skills(
                request.form.get("skills", "").split(",")
            )
        )
        experience = request.form.get("experience", "").strip()

        if not all([
            full_name, age_text, education,
            college, year_text, student_skills
        ]):
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("student_details"))

        try:
            age = int(age_text)
            graduation_year = int(year_text)
        except ValueError:
            flash("Enter a valid age and graduation year.", "error")
            return redirect(url_for("student_details"))

        if not 16 <= age <= 100:
            flash("Enter an age between 16 and 100.", "error")
            return redirect(url_for("student_details"))

        with get_db_connection() as connection:
            connection.execute("""
                UPDATE students
                SET name = ?, age = ?, education = ?, college = ?,
                    graduation_year = ?, skills = ?, experience = ?
                WHERE id = ?
            """, (
                full_name,
                age,
                education,
                college,
                graduation_year,
                student_skills,
                experience,
                session["student_id"]
            ))

        session["student_name"] = full_name
        flash("Student details saved successfully!", "success")
        return redirect(url_for("home"))

    return render_template("student_details.html", student=student)


# ---------------- CAREER PREDICTION ----------------

def predict_career(student_skills):
    skills = set(normalize_skills(student_skills))

    scores = {
        career: sum(1 for skill in required if skill in skills)
        for career, required in career_skills.items()
    }

    # Exact frontend skill set should recommend Frontend Developer.
    frontend_skills = {"html", "css", "javascript", "react"}

    if frontend_skills.issubset(skills):
        backend_skills = {"node.js", "express", "api", "sql"}

        if len(skills & backend_skills) >= 2:
            return "Full Stack Developer"

        return "Frontend Developer"

    # Distinctive skills help select specialized careers.
    preferences = [
        ("Cybersecurity Analyst", {"cybersecurity", "security tools"}),
        ("Cloud Engineer", {"cloud", "aws", "docker"}),
        ("Mobile App Developer", {"flutter", "dart", "kotlin", "android"}),
        ("Backend Developer", {"node.js", "express", "api"}),
        ("Data Scientist", {"machine learning", "pandas"}),
        ("Data Analyst", {"excel", "power bi"}),
        ("Software Developer", {"java"}),
        ("Frontend Developer", {"react", "javascript"}),
        ("Web Developer", {"html", "css", "git"})
    ]

    highest_score = max(scores.values())

    best_careers = [
        career for career, score in scores.items()
        if score == highest_score
    ]

    for career, distinctive_skills in preferences:
        if (
            career in best_careers
            and skills.intersection(distinctive_skills)
        ):
            return career

    return best_careers[0]
@app.route("/")
def index():
    return redirect(url_for("register"))


# ---------------- CAREER DASHBOARD ----------------

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def home():
    result = None

    with get_db_connection() as connection:
        student = connection.execute(
            "SELECT * FROM students WHERE id = ?",
            (session["student_id"],)
        ).fetchone()

    if student is None:
        session.clear()
        return redirect(url_for("login"))

    if request.method == "POST":
        skills_input = request.form.get("skills", "")
        student_skills = normalize_skills(skills_input.split(","))

        if not student_skills:
            flash("Please enter at least one skill.", "error")
            return redirect(url_for("home"))

        predicted_career = predict_career(student_skills)
        required_skills = career_skills[predicted_career]

        missing_skills = [
            skill for skill in required_skills
            if skill not in student_skills
        ]

        matched_skills = len(required_skills) - len(missing_skills)

        match_percentage = round(
            matched_skills / len(required_skills) * 100
        ) if required_skills else 0

        recommendations = [
            skill_recommendations[skill]
            for skill in missing_skills
            if skill in skill_recommendations
        ]

        result = {
            "career": predicted_career,
            "match_percentage": match_percentage,
            "student_skills": student_skills,
            "required_skills": required_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations
        }

    return render_template(
        "index.html",
        careers=career_skills.keys(),
        result=result,
        student=student
    )




# ---------------- LEARNING PAGES ----------------

@app.route('/courses')
@login_required
def courses():
    return render_template('courses.html')


@app.route('/notes')
@login_required
def notes():
    return render_template('notes.html')


@app.route('/python-notes')
@login_required
def python_notes():
    return render_template('python_notes.html')


@app.route('/handwriting-notes')
@login_required
def handwriting_notes():
    return render_template('handwriting_notes.html')



@app.route('/handwriting-notes/pdf/<path:filename>')
@login_required
def open_handwriting_pdf(filename):
    # First try the exact filename requested by the HTML link.
    pdf_path = HANDWRITING_DIR / filename

    # If the link's filename has a small spelling difference, use the only
    # PDF in the handwriting_notes folder (if there is exactly one).
    if not pdf_path.is_file():
        pdf_files = list(HANDWRITING_DIR.glob('*.pdf'))
        if len(pdf_files) == 1:
            pdf_path = pdf_files[0]
        else:
            available = ', '.join(file.name for file in pdf_files) or 'No PDF files found'
            return (
                f"PDF not found. Requested: {filename}. "
                f"Folder checked: {HANDWRITING_DIR}. Available PDFs: {available}",
                404
            )

    return send_from_directory(
        str(pdf_path.parent),
        pdf_path.name,
        as_attachment=False
    )


if __name__ == "__main__":
    app.run(debug=True)
