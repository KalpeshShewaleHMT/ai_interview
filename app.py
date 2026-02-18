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

@app.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect("/login")

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
    interview = db.session.get(Interview, data["interview_id"])
    question_number = data["question_number"]
    user_answer = data.get("answer", "")
    
    # Prevent re-attempt
    existing_result = Result.query.filter_by(
        user_id=current_user.id,
        interview_id=interview.id
    ).first()
    
    if existing_result:
        return jsonify({"completed": True, "message": "Interview already completed."})

    # Get previous conversation from DB
    conversations = Conversation.query.filter_by(
        user_id=current_user.id,
        interview_id=interview.id
    ).order_by(Conversation.question_number).all()

    history = ""
    for c in conversations:
        history += f"\nAI: {c.question}\nUser: {c.answer}"

    engine = InterviewEngine(
        interview.topic,
        interview.difficulty,
        interview.total_questions
    )

    # If final question → generate feedback
    if question_number > interview.total_questions:
        return jsonify({"completed": True})

    ai_response = engine.next_question(history, question_number)

    # If this is final question (feedback phase)
    if question_number == interview.total_questions:
        # Extract score
        try:
            feedback_part = ai_response.split("SCORE:")[0].replace("FEEDBACK:", "").strip()
            score_part = ai_response.split("SCORE:")[1].strip()
            score = int(score_part.split()[0])
        except:
            feedback_part = ai_response
            score = 0

        result = Result(
            user_id=current_user.id,
            interview_id=interview.id,
            feedback=feedback_part,
            score=score
        )
        db.session.add(result)
        db.session.commit()

        return jsonify({
            "response": ai_response,
            "completed": True
        })

    # Save question + answer
    new_convo = Conversation(
        user_id=current_user.id,
        interview_id=interview.id,
        question_number=question_number,
        question=ai_response,
        answer=user_answer
    )
    db.session.add(new_convo)
    db.session.commit()

    return jsonify({
        "response": ai_response,
        "completed": False
    })


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
