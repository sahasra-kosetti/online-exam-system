from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "exam_secret_key_123"


# =====================================================
# 120 STUDENTS AUTO GENERATED (COMMON BRANCH CSE)
# =====================================================

students = {}

for i in range(1, 121):
    students[f"student{i}"] = {
        "password": f"pass{i}",
        "name": f"Student {i}",
        "branch": "CSE"
    }

students["sahasra"] = {
    "password": "1234",
    "name": "Sahasra Kosetti",
    "branch": "CSE"
}


# =====================================================
# QUESTION PAPER (YOU WILL GIVE TEXT HERE)
# =====================================================

questions = {

    1: {
        "text": "Your Question 1 here",
        "options": ["A", "B", "C", "D"]
    },

    2: {
        "text": "Your Question 2 here",
        "options": ["A", "B", "C", "D"]
    },

    3: {
        "text": "Your Question 3 here",
        "options": ["A", "B", "C", "D"]
    }

}


# =====================================================
# ANSWER SHEET (YOU WILL GIVE ANSWERS HERE)
# =====================================================

answer_key = {

    1: "A",
    2: "B",
    3: "C"

}


# =====================================================
# PROFESSIONAL CSS
# =====================================================

css = """
<style>

body {
    margin: 0;
    background: linear-gradient(135deg, #667eea, #764ba2);
    font-family: Arial;
}

.container {
    width: 450px;
    margin: auto;
    margin-top: 100px;
    background: white;
    padding: 30px;
    border-radius: 15px;
}

.exam {
    width: 800px;
    margin: auto;
    margin-top: 40px;
    background: white;
    padding: 30px;
    border-radius: 15px;
}

.center {
    text-align: center;
}

button {
    padding: 12px 40px;
    border: none;
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 20px;
    font-size: 16px;
}

.pass {
    color: green;
    font-size: 22px;
}

.fail {
    color: red;
    font-size: 22px;
}

</style>
"""


# =====================================================
# LOGIN PAGE
# =====================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = request.form["username"]
        password = request.form["password"]

        if user in students and students[user]["password"] == password:

            session["user"] = user
            return redirect("/exam")

        else:

            return css + "<div class='container'><h2>Invalid Login</h2></div>"

    return css + """

    <div class="container">

    <h2 class="center">Student Login</h2>

    <form method="post">

    Username:<br>
    <input type="text" name="username" required><br><br>

    Password:<br>
    <input type="password" name="password" required><br><br>

    <div class="center">
    <button type="submit">Login</button>
    </div>

    </form>

    </div>
    """


# =====================================================
# EXAM PAGE
# =====================================================

@app.route("/exam", methods=["GET", "POST"])
def exam():

    if "user" not in session:
        return redirect("/")

    student = students[session["user"]]

    if request.method == "POST":

        score = 0

        for qno in questions:

            student_ans = request.form.get(f"q{qno}")

            if student_ans == answer_key[qno]:
                score += 1

        total = len(questions)

        percentage = (score / total) * 100

        result = "PASS" if percentage >= 50 else "FAIL"

        result_class = "pass" if result == "PASS" else "fail"

        return css + f"""

        <div class="container center">

        <h2>Result</h2>

        Name: {student['name']}<br>
        Branch: {student['branch']}<br>
        Score: {score}/{total}<br>
        Percentage: {percentage:.2f}%<br>

        <p class="{result_class}">{result}</p>

        <a href="/logout"><button>Logout</button></a>

        </div>
        """

    html = css + "<div class='exam'><h2 class='center'>Question Paper</h2><form method='post'>"

    for qno, q in questions.items():

        html += f"<p><b>Q{qno}. {q['text']}</b></p>"

        for opt in q["options"]:

            html += f"""
            <input type="radio" name="q{qno}" value="{opt}" required> {opt}<br>
            """

    html += """

    <br>
    <div class="center">
    <button type="submit">Submit Answer Sheet</button>
    </div>

    </form></div>
    """

    return html


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":
    app.run()
