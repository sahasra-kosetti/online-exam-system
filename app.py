from flask import Flask, render_template_string, request, redirect, session

app = Flask(__name__)
app.secret_key = "exam_secret"

# Student database
students = {
    "sahasra": "1234",
    "student1": "1111",
    "student2": "2222"
}

# Questions
questions = [
    {
        "question": "Capital of India?",
        "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "5 + 3 = ?",
        "options": ["6", "7", "8", "9"],
        "answer": "8"
    }
]

# ---------------- LOGIN PAGE ---------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in students and students[username] == password:
            session["user"] = username
            return redirect("/exam")
        else:
            return "Invalid login"

    return '''
        <h2>Student Login</h2>
        <form method="post">
            Username: <input name="username"><br><br>
            Password: <input name="password" type="password"><br><br>
            <button type="submit">Login</button>
        </form>
    '''

# ---------------- EXAM PAGE ---------------- #
@app.route("/exam", methods=["GET", "POST"])
def exam():

    if "user" not in session:
        return redirect("/")

    if request.method == "POST":

        score = 0
        for i, q in enumerate(questions):
            ans = request.form.get(f"q{i}")
            if ans == q["answer"]:
                score += 1

        percentage = (score / len(questions)) * 100

        if percentage >= 50:
            result = "PASS"
        else:
            result = "FAIL"

        return f"""
        <h2>Result</h2>
        Score: {score}/{len(questions)}<br>
        Percentage: {percentage}%<br>
        Result: {result}<br><br>
        <a href='/logout'>Logout</a>
        """

    html = "<h2>Online Exam</h2><form method='post'>"

    for i, q in enumerate(questions):
        html += f"<p>{q['question']}</p>"
        for opt in q["options"]:
            html += f"<input type='radio' name='q{i}' value='{opt}' required> {opt}<br>"

    html += "<br><button type='submit'>Submit</button></form>"

    return html

# ---------------- LOGOUT ---------------- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# IMPORTANT for gunicorn
if __name__ == "__main__":
    app.run()
