from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "exam_system_secret"


# =====================================================
# AUTO GENERATE 120 STUDENTS WITH ROLL NO, NAME, DEPT
# =====================================================

students = {}

for i in range(1, 121):

    username = f"student{i}"

    students[username] = {
        "password": f"pass{i}",
        "name": f"Student {i}",
        "dept": "CSE",
        "roll": f"CSE2025{i:03}"
    }

# Example custom student
students["sahasra"] = {
    "password": "1234",
    "name": "Sahasra Kosetti",
    "dept": "CSE",
    "roll": "CSE2025000"
}


# =====================================================
# QUESTION PAPER (PASTE YOUR QUESTIONS HERE)
# =====================================================

questions = {

    1: {
        "text": "Python developed by?",
        "options": ["James Gosling", "Guido van Rossum", "Dennis Ritchie", "Mark"]
    },

    2: {
        "text": "Capital of India?",
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"]
    },

    3: {
        "text": "Which is database?",
        "options": ["MySQL", "Python", "HTML", "CSS"]
    }

}


# =====================================================
# ANSWER SHEET (UPLOAD / PASTE ANSWERS HERE)
# =====================================================

answer_key = {

    1: "Guido van Rossum",
    2: "Delhi",
    3: "MySQL"

}


# =====================================================
# GRADE FUNCTION
# =====================================================

def calculate_grade(percentage):

    if percentage >= 90:
        return "A+"

    elif percentage >= 75:
        return "A"

    elif percentage >= 60:
        return "B"

    elif percentage >= 50:
        return "C"

    else:
        return "F"


# =====================================================
# PROFESSIONAL CSS
# =====================================================

css = """
<style>

body {
    margin:0;
    background: linear-gradient(135deg, #1d2b64, #f8cdda);
    font-family: Arial;
}

.container {

    width: 500px;
    margin: auto;
    margin-top: 80px;
    background: white;
    padding: 30px;
    border-radius: 15px;
}

.exam {

    width: 900px;
    margin: auto;
    margin-top: 40px;
    background: white;
    padding: 30px;
    border-radius: 15px;
}

.center {
    text-align: center;
}

.question {

    background: #f2f4ff;
    padding: 15px;
    margin-top: 15px;
    border-radius: 10px;
}

button {

    padding: 12px 40px;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    border: none;
    border-radius: 25px;
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

.grade {
    font-size: 20px;
    color: blue;
}

</style>
"""


# =====================================================
# LOGIN PAGE
# =====================================================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username in students and students[username]["password"] == password:

            session["user"] = username

            return redirect("/exam")

        else:

            return css + """

            <div class="container center">

            <h2>Invalid Login</h2>

            <a href="/"><button>Try Again</button></a>

            </div>
            """

    return css + """

    <div class="container">

    <h2 class="center">Online Exam Login</h2>

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

            ans = request.form.get(f"q{qno}")

            if ans == answer_key[qno]:

                score += 1

        total = len(questions)

        percentage = (score / total) * 100

        grade = calculate_grade(percentage)

        result = "PASS" if percentage >= 50 else "FAIL"

        result_class = "pass" if result == "PASS" else "fail"

        return css + f"""

        <div class="container center">

        <h2>Exam Result</h2>

        Name: {student['name']}<br><br>

        Department: {student['dept']}<br><br>

        Roll No: {student['roll']}<br><br>

        Score: {score}/{total}<br><br>

        Percentage: {percentage:.2f}%<br><br>

        <div class="grade">Grade: {grade}</div><br>

        <div class="{result_class}">Result: {result}</div><br>

        <a href="/logout"><button>Logout</button></a>

        </div>
        """

    html = css + """

    <div class="exam">

    <h2 class="center">Question Paper</h2>

    <form method="post">
    """

    for qno, q in questions.items():

        html += f"""

        <div class="question">

        <b>Q{qno}. {q['text']}</b><br><br>
        """

        for opt in q["options"]:

            html += f"""

            <input type="radio" name="q{qno}" value="{opt}" required> {opt}<br>
            """

        html += "</div>"

    html += """

    <br>
    <div class="center">
    <button type="submit">Submit Answer Sheet</button>
    </div>

    </form>

    </div>
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
