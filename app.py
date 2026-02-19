from flask import Flask, request, redirect, session, url_for
import time
import openpyxl
import os

app = Flask(__name__)
app.secret_key = "exam_system_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "results.xlsx")
EXAM_DURATION = 1800   # 30 minutes


# =====================================================
# CREATE EXCEL FILE
# =====================================================

if not os.path.exists(EXCEL_FILE):

    wb = openpyxl.Workbook()
    ws = wb.active

    ws.title = "Exam Results"

    ws.append([
        "Username",
        "Name",
        "Department",
        "Roll No",
        "Score",
        "Total",
        "Percentage",
        "Grade",
        "Result",
        "Time"
    ])

    wb.save(EXCEL_FILE)


# =====================================================
# SAVE RESULT
# =====================================================

def save_result(username, student, score, total, percent, grade, result):

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active

    ws.append([
        username,
        student["name"],
        student["dept"],
        student["roll"],
        score,
        total,
        round(percent,2),
        grade,
        result,
        time.strftime("%Y-%m-%d %H:%M:%S")
    ])

    wb.save(EXCEL_FILE)


# =====================================================
# STUDENTS AUTO GENERATE
# =====================================================

students = {}

for i in range(1,121):

    students[f"student{i}"] = {

        "password": f"pass{i}",
        "name": f"Student {i}",
        "dept": "CSE",
        "roll": f"CSE2025{i:03}"

    }


# custom student

students["sahasra"] = {

    "password":"1234",
    "name":"Sahasra Kosetti",
    "dept":"BCA Data Science",
    "roll":"2347390190"

}


# =====================================================
# QUESTIONS
# =====================================================

questions = {

    1:{
        "text":"Which protocol is secure?",
        "options":["HTTP","HTTPS","FTP","SMTP"]
    },

    2:{
        "text":"Binary search complexity?",
        "options":["O(n)","O(log n)","O(n log n)","O(1)"]
    },

    3:{
        "text":"FIFO structure?",
        "options":["Stack","Queue","Tree","Graph"]
    },

    4:{
        "text":"Python creator?",
        "options":["Dennis Ritchie","Guido van Rossum","James Gosling","Mark"]
    },

    5:{
        "text":"Database example?",
        "options":["Python","MySQL","HTML","CSS"]
    }

}


# =====================================================
# ANSWERS
# =====================================================

answer_key = {

    1:"HTTPS",
    2:"O(log n)",
    3:"Queue",
    4:"Guido van Rossum",
    5:"MySQL"

}


# =====================================================
# GRADE FUNCTION
# =====================================================

def grade(p):

    if p>=90:return "A+"
    elif p>=75:return "A"
    elif p>=60:return "B"
    elif p>=50:return "C"
    else:return "F"

# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



# =====================================================
# PROFESSIONAL CSS + TIMER SCRIPT
# =====================================================

css = """

<style>

body{
margin:0;
font-family:Segoe UI;
background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

/* LOGIN */

.login{

width:400px;
margin:auto;
margin-top:120px;
background:white;
padding:40px;
border-radius:12px;
}

.center{text-align:center;}

input{

width:100%;
padding:12px;
margin-top:10px;
margin-bottom:20px;

}
.question input[type="radio"]{
width:auto;
margin-right:8px;
}


button{

padding:12px 40px;
background:#ff512f;
color:white;
border:none;
border-radius:25px;

}


/* EXAM */

.exam{

display:flex;
justify-content:center;
gap:40px;
margin-top:20px;

}

.logo img{

width:140px;

}

.timer{

color:white;
font-size:28px;

}

.paper{

background:white;
padding:30px;
border-radius:12px;
width:700px;

}

.question{

margin-top:15px;

}

.result{

width:400px;
margin:auto;
margin-top:100px;
background:white;
padding:30px;
border-radius:12px;
text-align:center;

}

.pass{color:green;font-size:22px;}
.fail{color:red;font-size:22px;}
.grade{color:blue;font-size:20px;}

</style>


<script>

function startTimer(duration){

let timer=duration;

setInterval(function(){

let m=parseInt(timer/60)
let s=parseInt(timer%60)

m=m<10?"0"+m:m
s=s<10?"0"+s:s

document.getElementById("timer").innerHTML=m+":"+s

if(timer<=0){

document.getElementById("examForm").submit()

}

timer--

},1000)

}

</script>

"""


# =====================================================
# LOGIN PAGE
# =====================================================

@app.route("/",methods=["GET","POST"])
def login():

    if request.method=="POST":

        u=request.form["username"]
        p=request.form["password"]

        if u in students and students[u]["password"]==p:

            session["user"]=u
            session["start"]=time.time()

            return redirect("/exam")

    return css+"""

<div class="login">

<h2 class="center">Student Login</h2>

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

@app.route("/exam",methods=["GET","POST"])
def exam():

    if "user" not in session:
        return redirect("/")

    student=students[session["user"]]

    elapsed=time.time()-session["start"]

    remaining=int(EXAM_DURATION-elapsed)

    if remaining<=0:

        return redirect("/submit")

    if request.method=="POST":

        score=0

        for q in questions:

            if request.form.get(f"q{q}")==answer_key[q]:
                score+=1

        total=len(questions)

        percent=(score/total)*100

        g=grade(percent)

        result="PASS" if percent>=50 else "FAIL"

        save_result(session["user"],student,score,total,percent,g,result)

        return css+f"""

<div class="result">

<h2>Exam Result</h2>

Name: {student['name']}<br><br>
Dept: {student['dept']}<br><br>
Roll: {student['roll']}<br><br>

Score: {score}/{total}<br><br>

Percentage: {percent:.2f}%<br><br>

<div class="grade">Grade: {g}</div><br>

<div class="{'pass' if result=='PASS' else 'fail'}">
{result}
</div>

<br><br>

<a href="/logout">
<button>Logout</button>
</a>

</div>

"""



    html=css+f"""

<body onload="startTimer({remaining})">

<div class="exam">

<div class="logo">

<img src="/static/college_logo.png">

</div>

<div class="paper">

<h2 class="center">Question Paper</h2>

<form method="post" id="examForm">

"""


    for q,qdata in questions.items():

        html+=f"<div class='question'><b>Q{q}. {qdata['text']}</b><br>"

        for opt in qdata["options"]:

            html+=f"""
<input type="radio" name="q{q}" value="{opt}" required>
{opt}<br>
"""

        html+="</div>"


    html+="""


<br>

<div class="center">
<button>Submit Exam</button>
</div>

</form>

</div>

<div class="timer">

Time Left<br>

<span id="timer">30:00</span>

</div>

</div>

</body>

"""

    return html


# =====================================================
# RUN
# =====================================================

if __name__=="__main__":
    app.run(debug=True)
