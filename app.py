from flask import Flask, render_template, request, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database.models import db, User, Interview, Conversation, Result
from config import Config
from interview_engine import InterviewEngine

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.before_first_request
# def create_tables():
#     db.create_all()
with app.app_context():
    db.create_all()

# ---------------- AUTH ----------------

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"],
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        interviews = Interview.query.all()
        users = User.query.all()
        return render_template("admin_dashboard.html", interviews=interviews, users=users)
    else:
        interviews = Interview.query.all()
        return render_template("user_dashboard.html", interviews=interviews)

# -------------- INTERVIEW API ----------------

@app.route("/start_interview/<int:id>")
@login_required
def start_interview(id):
    interview = Interview.query.get(id)
    return render_template("interview_chat.html", interview=interview)

@app.route("/api/interview", methods=["POST"])
@login_required
def interview_api():
    data = request.json
    interview = Interview.query.get(data["interview_id"])

    history = data["history"]
    question_number = data["question_number"]

    engine = InterviewEngine(
        interview.topic,
        interview.difficulty,
        interview.total_questions
    )

    response = engine.next_question(history, question_number)

    return jsonify({"response": response})

@app.route("/history")
@login_required
def history():
    results = Result.query.filter_by(user_id=current_user.id).all()
    return render_template("interview_history.html", results=results)

@app.route("/add_interview", methods=["POST"])
@login_required
def add_interview():
    if current_user.role != "admin":
        return redirect("/dashboard")

    interview = Interview(
        topic=request.form["topic"],
        difficulty=request.form["difficulty"],
        total_questions=request.form["total_questions"]
    )
    db.session.add(interview)
    db.session.commit()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
