from flask import Flask, request, redirect, session
import time

app = Flask(__name__)
app.secret_key = "exam_system_secret"


# =====================================================
# AUTO GENERATE 120 STUDENTS
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

students["sahasra"] = {
    "password": "1234",
    "name": "Sahasra Kosetti",
    "dept": "BCA- Data Science",
    "roll": "2347390190"
}


# =====================================================
# QUESTIONS
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
# ANSWERS
# =====================================================

answer_key = {

    1: "Guido van Rossum",
    2: "Delhi",
    3: "MySQL"

}


# =====================================================
# GRADE FUNCTION
# =====================================================

def calculate_grade(p):

    if p >= 90: return "A+"
    elif p >= 75: return "A"
    elif p >= 60: return "B"
    elif p >= 50: return "C"
    else: return "F"


# =====================================================
# PROFESSIONAL CSS
# =====================================================

css = """

<style>

body{
margin:0;
font-family:Arial;
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

/* LOGIN */

.login-box{

width:400px;
margin:auto;
margin-top:120px;
background:white;
color:black;
padding:40px;
border-radius:15px;
box-shadow:0 0 20px rgba(0,0,0,0.4);
}

.center{text-align:center;}

input{

width:100%;
padding:12px;
margin-top:5px;
margin-bottom:15px;
border-radius:8px;
border:1px solid gray;
}

button{

padding:12px 40px;
background: linear-gradient(90deg,#ff512f,#dd2476);
color:white;
border:none;
border-radius:25px;
font-size:16px;
cursor:pointer;
}

button:hover{

background: linear-gradient(90deg,#dd2476,#ff512f);

}


/* EXAM LAYOUT */

.exam-container{

display:flex;
justify-content:center;
margin-top:30px;

}

.timer{

width:200px;
background:#ff4b4b;
padding:20px;
border-radius:15px;
text-align:center;
font-size:22px;
height:100px;
}

.question-area{

width:700px;
background:white;
color:black;
padding:30px;
border-radius:15px;
margin-left:20px;
margin-right:20px;
}

.logo{

width:200px;
background:white;
padding:20px;
border-radius:15px;
text-align:center;
}

.question{

background:#f2f4ff;
padding:15px;
margin-top:15px;
border-radius:10px;
}

.pass{color:green;font-size:22px;}
.fail{color:red;font-size:22px;}
.grade{color:blue;font-size:20px;}

</style>

"""


# =====================================================
# LOGIN
# =====================================================

@app.route("/", methods=["GET","POST"])
def login():

    if request.method=="POST":

        u=request.form["username"]
        p=request.form["password"]

        if u in students and students[u]["password"]==p:

            session["user"]=u
            session["start"]=time.time()

            return redirect("/exam")

        else:

            return css+"""

            <div class="login-box center">
            Invalid Login<br><br>
            <a href="/"><button>Retry</button></a>
            </div>
            """

    return css+"""

    <div class="login-box">

    <h2 class="center">Online Exam Login</h2>

    <form method="post">

    Username
    <input name="username" required>

    Password
    <input type="password" name="password" required>

    <div class="center">
    <button>Login</button>
    </div>

    </form>

    </div>
    """


# =====================================================
# EXAM PAGE
# =====================================================

@app.route("/exam", methods=["GET","POST"])
def exam():

    if "user" not in session:
        return redirect("/")

    student=students[session["user"]]

    # TIMER
    elapsed=time.time()-session["start"]
    remaining=int(1800-elapsed)

    mins=remaining//60
    secs=remaining%60

    if request.method=="POST":

        score=0

        for q in questions:

            if request.form.get(f"q{q}")==answer_key[q]:
                score+=1

        total=len(questions)

        percent=(score/total)*100

        grade=calculate_grade(percent)

        result="PASS" if percent>=50 else "FAIL"

        cls="pass" if result=="PASS" else "fail"

        return css+f"""

        <div class="login-box center">

        <h2>Result</h2>

        Name: {student['name']}<br><br>

        Dept: {student['dept']}<br><br>

        Roll: {student['roll']}<br><br>

        Score: {score}/{total}<br><br>

        Percentage: {percent:.2f}%<br><br>

        <div class="grade">Grade: {grade}</div><br>

        <div class="{cls}">Result: {result}</div>

        <br>

        <a href="/logout"><button>Logout</button></a>

        </div>
        """

    html=css+f"""

    <div class="exam-container">

    <div class="timer">

    Time Left<br>

    {mins:02}:{secs:02}

    </div>

    <div class="question-area">

    <h2 class="center">Adhoc Network Tech</h2>

    <form method="post">
    """

    for qno,q in questions.items():

        html+=f"<div class='question'><b>Q{qno}. {q['text']}</b><br>"

        for opt in q["options"]:

            html+=f"<input type='radio' name='q{qno}' value='{opt}' required> {opt}<br>"

        html+="</div>"

    html+="""

    <br>

    <div class="center">

    <button>Submit</button>

    </div>

    </form>

    </div>

    <div class="logo">

    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg" width="150">

    <br><br>

    College Logo

    </div>

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

if __name__=="__main__":
    app.run()
