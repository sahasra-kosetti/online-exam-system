from flask import Flask, request, redirect, session, url_for
import time
import openpyxl
import os

app = Flask(__name__)
app.secret_key = "secret123"

EXCEL_FILE = "results.xlsx"
EXAM_TIME = 1800


# =====================================================
# CREATE EXCEL FILE
# =====================================================

if not os.path.exists(EXCEL_FILE):

    wb = openpyxl.Workbook()
    ws = wb.active

    ws.title = "Results"

    ws.append([
        "Username",
        "Name",
        "Department",
        "Roll",
        "Score",
        "Total",
        "Percentage",
        "Grade",
        "Result"
    ])

    wb.save(EXCEL_FILE)


# =====================================================
# SAVE RESULT
# =====================================================

def save_result(user, student, score, total, percent, grade, result):

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active

    ws.append([
        user,
        student["name"],
        student["dept"],
        student["roll"],
        score,
        total,
        percent,
        grade,
        result
    ])

    wb.save(EXCEL_FILE)


# =====================================================
# STUDENTS
# =====================================================

students = {}

for i in range(1,121):

    students[f"student{i}"] = {

        "password":f"pass{i}",
        "name":f"Student {i}",
        "dept":"CSE",
        "roll":f"CSE2025{i:03}"

    }


# =====================================================
# QUESTIONS
# =====================================================

questions = {

1:{
"text":"Python developed by?",
"options":["Dennis Ritchie","Guido van Rossum","James Gosling","Mark"]
},

2:{
"text":"Secure protocol?",
"options":["HTTP","HTTPS","FTP","SMTP"]
},

3:{
"text":"FIFO structure?",
"options":["Stack","Queue","Tree","Graph"]
}

}


# =====================================================
# ANSWERS
# =====================================================

answer_key = {

1:"Guido van Rossum",
2:"HTTPS",
3:"Queue"

}


# =====================================================
# GRADE
# =====================================================

def get_grade(p):

    if p>=90:return "A+"
    elif p>=75:return "A"
    elif p>=60:return "B"
    elif p>=50:return "C"
    else:return "F"


# =====================================================
# CSS
# =====================================================

css = """

<style>

body{
font-family:Arial;
background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
margin:0;
}

.login{
background:white;
width:400px;
margin:auto;
margin-top:120px;
padding:30px;
border-radius:10px;
}

.center{text-align:center;}

button{
padding:10px 30px;
background:#ff512f;
color:white;
border:none;
border-radius:20px;
}

.exam{
display:flex;
justify-content:center;
gap:40px;
margin-top:20px;
}

.logo img{
width:120px;
}

.paper{
background:white;
padding:20px;
width:600px;
border-radius:10px;
}

.timer{
color:white;
font-size:25px;
}

.question{
margin-top:15px;
}

.option{
margin-left:15px;
}

.result{
background:white;
width:400px;
margin:auto;
margin-top:100px;
padding:20px;
border-radius:10px;
text-align:center;
}

.pass{color:green;}
.fail{color:red;}

</style>


<script>

function timer(sec){

let t=sec;

setInterval(function(){

let m=parseInt(t/60)
let s=parseInt(t%60)

if(m<10)m="0"+m
if(s<10)s="0"+s

document.getElementById("timer").innerHTML=m+":"+s

if(t<=0){

document.getElementById("examForm").submit()

}

t--

},1000)

}

</script>

"""


# =====================================================
# LOGIN
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

<h2 class="center">Login</h2>

<form method="post">

Username<br>
<input name="username"><br><br>

Password<br>
<input type="password" name="password"><br><br>

<div class="center">
<button>Login</button>
</div>

</form>

</div>

"""


# =====================================================
# EXAM
# =====================================================

@app.route("/exam",methods=["GET","POST"])
def exam():

    if "user" not in session:
        return redirect("/")

    student = students[session["user"]]

    remain = EXAM_TIME - int(time.time() - session["start"])

    if request.method=="POST":

        score=0

        for q in questions:

            if request.form.get(f"q{q}") == answer_key[q]:

                score+=1

        total=len(questions)

        percent=int(score/total*100)

        grade=get_grade(percent)

        result="PASS" if percent>=50 else "FAIL"

        save_result(session["user"],student,score,total,percent,grade,result)

        return css+f"""

<div class="result">

<h2>Result</h2>

Name: {student['name']}<br>
Dept: {student['dept']}<br>
Roll: {student['roll']}<br><br>

Score: {score}/{total}<br>
Percentage: {percent}%<br>
Grade: {grade}<br>

<h3 class="{'pass' if result=='PASS' else 'fail'}">{result}</h3>

</div>

"""


    html = css+f"""

<body onload="timer({remain})">

<div class="exam">

<div class="logo">

<img src="/static/college_logo.png">

</div>


<div class="paper">

<h2 class="center">Question Paper</h2>

<form method="post" id="examForm">

"""


    for q in questions:

        html+=f"<div class='question'><b>Q{q}. {questions[q]['text']}</b><br>"

        for opt in questions[q]["options"]:

            html+=f"""
<label class="option">
<input type="radio" name="q{q}" value="{opt}"> {opt}
</label><br>
"""

        html+="</div>"


    html+="""

<br>

<div class="center">
<button>Submit</button>
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
