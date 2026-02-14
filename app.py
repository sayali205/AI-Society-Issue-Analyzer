from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import joblib

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ================= LOAD ML MODEL =================
model = joblib.load("complaint_model.pkl")


# ================= DATABASE =================
db = sqlite3.connect("society.db", check_same_thread=False)
cur = db.cursor()


# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT,
role TEXT
)
""")


# Create complaints table
cur.execute("""
CREATE TABLE IF NOT EXISTS complaints(
id INTEGER PRIMARY KEY AUTOINCREMENT,
issue TEXT,
priority TEXT,
action TEXT,
username TEXT
)
""")


# Create default admin
cur.execute("SELECT * FROM users WHERE username='admin'")
if not cur.fetchone():
    cur.execute(
    "INSERT INTO users(username,password,role) VALUES('admin','admin123','admin')")
    db.commit()


# ================= HOME =================
@app.route("/", methods=["GET","POST"])
def index():

    priority=None
    action=None
    user_complaints=[]

    # If NOT logged in
    if "user" not in session:

        return render_template(
            "index.html",
            logged_in=False
        )


    # If logged in and form submitted
    if request.method=="POST":

        complaint=request.form["complaint"]

        # Predict priority
        priority=model.predict([complaint])[0]


        # Define action
        if priority=="High":

            action="""Immediate action required
Notify society secretary
Call maintenance team"""

        elif priority=="Medium":

            action="""Fix within few hours
Inform maintenance"""

        else:

            action="""Normal issue
Fix later"""


        # Save complaint
        cur.execute("""
        INSERT INTO complaints(issue,priority,action,username)
        VALUES(?,?,?,?)
        """,(complaint,priority,action,session["user"]))

        db.commit()


    # Fetch complaints
    cur.execute("""
    SELECT * FROM complaints
    WHERE username=?
    ORDER BY id DESC
    """,(session["user"],))

    user_complaints=cur.fetchall()


    return render_template(
        "index.html",
        priority=priority,
        action=action,
        logged_in=True,
        user_complaints=user_complaints,
        role=session.get("role")
    )


# ================= REGISTER =================
@app.route("/register", methods=["GET","POST"])
def register():

    error=None

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]
        confirm=request.form["confirm"]

        if password!=confirm:

            error="Password mismatch"

        else:

            try:

                cur.execute("""
                INSERT INTO users(username,password,role)
                VALUES(?,?,?)
                """,(username,password,"resident"))

                db.commit()

                session["user"]=username
                session["role"]="resident"

                return redirect("/")

            except:

                error="Username already exists"


    return render_template("register.html",error=error)


# ================= LOGIN =================
@app.route("/login", methods=["GET","POST"])
def login():

    error=None

    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]

        cur.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """,(username,password))

        user=cur.fetchone()

        if user:

            session["user"]=user[1]
            session["role"]=user[3]

            return redirect("/")

        else:

            error="Invalid username or password"


    return render_template("login.html",error=error)


# ================= LOGOUT =================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# ================= ADMIN DASHBOARD =================
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    if session["role"]!="admin":
        return redirect("/")

    cur.execute("""
    SELECT priority,COUNT(*)
    FROM complaints
    GROUP BY priority
    """)

    stats=cur.fetchall()

    cur.execute("SELECT * FROM complaints ORDER BY id DESC")

    complaints=cur.fetchall()

    return render_template(
        "dashboard.html",
        stats=stats,
        complaints=complaints
    )
@app.route("/analyze", methods=["POST"])
def analyze():

    if "user" not in session:
        return redirect("/login")

    issue = request.form["issue"].lower()

    if "water" in issue:
        category = "Water Problem"
        priority = "High"
    elif "electric" in issue:
        category = "Electricity Problem"
        priority = "High"
    elif "garbage" in issue:
        category = "Cleanliness Problem"
        priority = "Medium"
    else:
        category = "General Issue"
        priority = "Low"

    result = {
        "category": category,
        "priority": priority
    }

    return render_template("dashboard.html",
                           user=session["user"],
                           result=result)


# ================= RUN =================
if __name__=="__main__":

    app.run(debug=True)
