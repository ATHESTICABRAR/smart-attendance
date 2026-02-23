from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date, datetime
import math

app = Flask(__name__)
app.secret_key = "attendance_secret"
DB = "database.db"

# COLLEGE LOCATION (example)
COLLEGE_LAT = 12.9716
COLLEGE_LON = 77.5946
ALLOWED_RADIUS = 0.15  # km (150 meters)

# ---------------- DATABASE ----------------
def db():
    return sqlite3.connect(DB)

def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        student_id TEXT,
        day TEXT,
        status TEXT,
        time TEXT,
        lat REAL,
        lon REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS teacher (
        username TEXT,
        password TEXT
    )
    """)

    # Default teacher
    cur.execute("SELECT * FROM teacher")
    if not cur.fetchone():
        cur.execute("INSERT INTO teacher VALUES ('admin', 'admin123')")

    con.commit()
    con.close()

# ---------------- LOCATION CHECK ----------------
def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2) * 111

# ---------------- STUDENT PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        sid = request.form["student_id"]
        lat = float(request.form["lat"])
        lon = float(request.form["lon"])

        if distance(lat, lon, COLLEGE_LAT, COLLEGE_LON) > ALLOWED_RADIUS:
            return "❌ Attendance allowed only inside college"

        today = str(date.today())
        now = datetime.now().strftime("%H:%M:%S")

        con = db()
        cur = con.cursor()

        cur.execute("""
        SELECT * FROM attendance WHERE student_id=? AND day=?
        """, (sid, today))

        if not cur.fetchone():
            cur.execute("""
            INSERT INTO attendance VALUES (?, ?, ?, ?, ?, ?)
            """, (sid, today, "Present", now, lat, lon))

        con.commit()
        con.close()
        return "✅ Attendance Marked Successfully"

    return render_template("student.html")

# ---------------- TEACHER LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM teacher WHERE username=? AND password=?", (u, p))
        if cur.fetchone():
            session["teacher"] = True
            return redirect("/teacher")
    return render_template("login.html")

# ---------------- TEACHER DASHBOARD ----------------
@app.route("/teacher")
def teacher():
    if not session.get("teacher"):
        return redirect("/login")

    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM attendance ORDER BY day DESC")
    records = cur.fetchall()
    con.close()

    return render_template("teacher.html", records=records)

# ---------------- EDIT ATTENDANCE ----------------
@app.route("/edit/<sid>/<day>/<status>")
def edit(sid, day, status):
    con = db()
    cur = con.cursor()
    cur.execute("""
    UPDATE attendance SET status=? WHERE student_id=? AND day=?
    """, (status, sid, day))
    con.commit()
    con.close()
    return redirect("/teacher")

# ---------------- WHATSAPP SHARE ----------------
@app.route("/share")
def share():
    today = str(date.today())
    con = db()
    cur = con.cursor()

    cur.execute("SELECT student_id FROM attendance WHERE day=? AND status='Present'", (today,))
    present = [x[0] for x in cur.fetchall()]

    cur.execute("SELECT student_id FROM attendance WHERE day=? AND status='Absent'", (today,))
    absent = [x[0] for x in cur.fetchall()]

    con.close()

    text = f"|| Attendance {today}\n\nPresent ({len(present)}):\n" + ", ".join(present)
    text += "\n\nAbsent (" + str(len(absent)) + "):\n" + ", ".join(absent)

    return redirect("https://wa.me/?text=" + text)

# ---------------- RUN ----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)