from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "exam_secret_key"


# ---------------- STUDENT DATABASE ---------------- #
students = {
    "sahasra": "1234",
    "student1": "1111",
    "student2": "2222"
}


# ---------------- QUESTIONS ---------------- #
questions = [
    {
        "question": "Capital of India?",
        "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Python is a?",
        "options": ["Snake", "Programming Language", "Car", "Game"],
        "answer": "Programming Language"
    },
    {
        "question": "5 + 3 = ?",
        "options": ["6", "7", "8", "9"],
        "answer": "8"
    }
]


# ---------------- CSS STYLE ---------------- #
css = """
<style>

body {
    background-color: #f0f2f6;
    font-family: Arial;
}

.container {
    width: 400px;
    margin: auto;
    margin-top: 100px;
    padding: 30px;
    background: white;
    border-radius: 10px;
    box-shadow: 0px 0px 10px gray;
}

.exam-container {
    width: 700px;
    margin: auto;
    margin-top: 50px;
    padding: 30px;
    background: white;
    border-radius: 10px;
    box-shadow: 0px 0px 10px gray;
}

h2 {
    text-align: center;
}

input {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
}

.center-btn {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

button {
    padding: 10px 30px;
    background-color: #4CAF50;
    border: none;
    color: white;
    font-size: 16px;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}

.question {
    margin-top: 20px;
}

</style>
"""


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
            return css + """
            <div class="container">
                <h2>Login Failed</h2>
                <div class="center-btn">
                    <a href="/"><button>Try Again</button></a>
                </div>
            </div>
            """

    return css + """
    <div class="container">
        <h2>Student Login</h2>

        <form method="post">

            Username:
            <input type="text" name="username" required>

            Password:
            <input type="password" name="password" required>

            <div class="center-btn">
                <button type="submit">Login</button>
            </div>

        </form>
    </div>
    """


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

        return css + f"""
        <div class="container">

        <h2>Result</h2>

        <p><b>Score:</b> {score}/{len(questions)}</p>
        <p><b>Percentage:</b> {percentage:.2f}%</p>
        <p><b>Result:</b> {result}</p>

        <div class="center-btn">
            <a href="/logout"><button>Logout</button></a>
        </div>

        </div>
        """

    html = css + """
    <div class="exam-container">

    <h2>Online Exam</h2>

    <form method="post">
    """

    for i, q in enumerate(questions):

        html += f"<div class='question'><p><b>{q['question']}</b></p>"

        for opt in q["options"]:
            html += f"""
            <input type="radio" name="q{i}" value="{opt}" required> {opt}<br>
            """

        html += "</div>"

    html += """
    <div class="center-btn">
        <button type="submit">Submit Exam</button>
    </div>

    </form>
    </div>
    """

    return html


# ---------------- LOGOUT ---------------- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    app.run()
