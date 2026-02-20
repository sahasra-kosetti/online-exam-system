from flask import Flask, request, redirect, session, url_for
import time
import openpyxl
import os

app = Flask(__name__)
app.secret_key = "exam_system_secret"

EXCEL_FILE = "results.xlsx"
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
# STUDENTS DATA (MANUAL)
# =====================================================

students = {

"D.Pravallika":{
    "password":"7894",
    "name":"D.Pravallika",
    "dept":"BCA Data Science",
    "roll":"2347390685"
},

"A. Amani":{
    "password":"1235",
    "name":"A. Amani",
    "dept":"BCA Data Science",
    "roll":"BCA2025002"
},

"K.Bhargavi Satya Durga Devi ":{
    "password":"1456",
    "name":"K.Bhargavi Satya Durga Devi ",
    "dept":"BCA Data Science",
    "roll":"2347390487"
},

" K.Mahalakshmi":{
    "password":"7794",
    "name":" K.Mahalakshmi",
    "dept":"BCA Data Science",
    "roll":"2347390121"
},

"Y.Deepthi Raajitha":{
    "password":"8964",
    "name":"Y.Deepthi Raajitha":{",
    "dept":"BCA Data Science",
    "roll":"2347390643"
},

"N.L.Madhulika ":{
    "password":"pass3",
    "name":"N.L.Madhulika ",
    "dept":"BCA Data Science",
    "roll":"2347390469"
}
    "D.Pravallika":{
    "password":"7894",
    "name":"D.Pravallika",
    "dept":"BCA Data Science",
    "roll":"2347390685"
},

"K.Bhavya sri":{
    "password":"pass2",
    "name":"K.Bhavya sri",
    "dept":"BCA Data Science",
    "roll":"2347390453"
},

" P. Mrudula ":{
    "password":"pass3",
    "name":" P. Mrudula ",
    "dept":"BCA Data Science",
    "roll":" 2347390537"
},
" M.Surekha":{
    "password":"7894",
    "name":" M.Surekha",
    "dept":"BCA Data Science",
    "roll":"2347390168"
},

" P. Lalitha":{
    "password":"pass2",
    "name":" P. Lalitha",
    "dept":"BCA Data Science",
    "roll":"2347390360"
},

" D. Lini Hadassa":{
    "password":"pass3",
    "name":" D. Lini Hadassa",
    "dept":"BCA Data Science",
    "roll":"2347390616"
},
"K. Venkata Lakshmi ":{
    "password":"7894",
    "name":"K. Venkata Lakshmi ",
    "dept":"BCA Data Science",
    "roll":"2347390581"
},

" V. Nandini Devi":{
    "password":"pass2",
    "name":" V. Nandini Devi",
    "dept":"BCA Data Science",
    "roll":" 2347390701"
},

"K.Jnana Deepthi ":{
    "password":"pass3",
    "name":"K.Jnana Deepthi ",
    "dept":"BCA Data Science",
    "roll":"2347390592"
},
"D.Pravallika":{
    "password":"7894",
    "name":"D.Pravallika",
    "dept":"BCA Data Science",
    "roll":"2347390685"
},

"L. Manga Charmila":{
    "password":"12365",
    "name":"L. Manga Charmila",
    "dept":"BCA Data Science",
    "roll":"2347390628"
},

"student3":{
    "password":"pass3",
    "name":"Student Name 3",
    "dept":"BCA Data Science",
    "roll":"BCA2025003"
}
"D.Pravallika":{
    "password":"7894",
    "name":"D.Pravallika",
    "dept":"BCA Data Science",
    "roll":"2347390685"
},

"student2":{
    "password":"pass2",
    "name":"Student Name 2",
    "dept":"BCA Data Science",
    "roll":"BCA2025002"
},

"student3":{
    "password":"pass3",
    "name":"Student Name 3",
    "dept":"BCA Data Science",
    "roll":"BCA2025003"
}
"D.Pravallika":{
    "password":"7894",
    "name":"D.Pravallika",
    "dept":"BCA Data Science",
    "roll":"2347390685"
},

"student2":{
    "password":"pass2",
    "name":"Student Name 2",
    "dept":"BCA Data Science",
    "roll":"BCA2025002"
},

"student3":{
    "password":"pass3",
    "name":"Student Name 3",
    "dept":"BCA Data Science",
    "roll":"BCA2025003"
}
"D.Pravallika":{
    "password":"7894",
    "name":"D.Pravallika",
    "dept":"BCA Data Science",
    "roll":"2347390685"
},

"student2":{
    "password":"pass2",
    "name":"Student Name 2",
    "dept":"BCA Data Science",
    "roll":"BCA2025002"
},

"student3":{
    "password":"pass3",
    "name":"Student Name 3",
    "dept":"BCA Data Science",
    "roll":"BCA2025003"
}
"D.Pravallika":{
    "password":"7894",
    "name":"D.Pravallika",
    "dept":"BCA Data Science",
    "roll":"2347390685"
},

"student2":{
    "password":"pass2",
    "name":"Student Name 2",
    "dept":"BCA Data Science",
    "roll":"BCA2025002"
},

"student3":{
    "password":"pass3",
    "name":"Student Name 3",
    "dept":"BCA Data Science",
    "roll":"BCA2025003"
}

# continue till student120

"sahasra":{
    "password":"1234",
    "name":"Sahasra Kosetti",
    "dept":"BCA Data Science",
    "roll":"2347390190"
}

}


# =====================================================
# QUESTIONS
# =====================================================

questions = {

    1: {
        "text": "Which of the following protocols is used for secure communication over the Internet?",
        "options": ["HTTP", "FTP", "HTTPS", "SMTP"]
    },

    2: {
        "text": "What is the time complexity of binary search algorithm?",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"]
    },

    3: {
        "text": "Which layer of OSI model is responsible for logical addressing?",
        "options": ["Transport Layer", "Network Layer", "Session Layer", "Data Link Layer"]
    },

    4: {
        "text": "Which data structure uses FIFO principle?",
        "options": ["Stack", "Queue", "Tree", "Graph"]
    },

    5: {
        "text": "Which SQL command is used to remove a table permanently?",
        "options": ["DELETE", "REMOVE", "DROP", "CLEAR"]
    },

    6: {
        "text": "Which of the following is NOT an operating system?",
        "options": ["Linux", "Windows", "Oracle", "MacOS"]
    },

    7: {
        "text": "Which normal form removes transitive dependency?",
        "options": ["1NF", "2NF", "3NF", "BCNF"]
    },

    8: {
        "text": "Which protocol is used to send emails?",
        "options": ["FTP", "SMTP", "HTTP", "SNMP"]
    },

    9: {
        "text": "Which sorting algorithm has best average time complexity?",
        "options": ["Bubble Sort", "Selection Sort", "Merge Sort", "Insertion Sort"]
    },

    10: {
        "text": "Which of the following is used for version control?",
        "options": ["Git", "Python", "MySQL", "HTML"]
    },

    11: {
        "text": "Which memory is fastest?",
        "options": ["RAM", "ROM", "Cache", "Hard Disk"]
    },

    12: {
        "text": "Which symbol is used for single line comment in Python?",
        "options": ["//", "#", "/* */", "--"]
    },

    13: {
        "text": "Which protocol is used for file transfer?",
        "options": ["FTP", "HTTP", "SMTP", "TCP"]
    },

    14: {
        "text": "Which data structure uses LIFO principle?",
        "options": ["Queue", "Stack", "Array", "Tree"]
    },

    15: {
        "text": "Which key is used to uniquely identify a record in database?",
        "options": ["Foreign Key", "Primary Key", "Candidate Key", "Alternate Key"]
    },
    16: {
        "text": "Which of the following is volatile memory?",
        "options": ["ROM", "Hard Disk", "RAM", "CD-ROM"]
    },

    17: {
        "text": "Which protocol is used to access web pages?",
        "options": ["HTTP", "FTP", "SMTP", "POP"]
    },

    18: {
        "text": "Which of the following is not a programming language?",
        "options": ["Python", "Java", "HTML", "Windows"]
    },

    19: {
        "text": "Which data structure is used in recursion?",
        "options": ["Queue", "Stack", "Tree", "Graph"]
    },

    20: {
        "text": "Which of the following is example of system software?",
        "options": ["MS Word", "Windows OS", "Chrome", "Photoshop"]
    },

    21: {
        "text": "Which SQL clause is used to filter records?",
        "options": ["WHERE", "ORDER", "GROUP", "FILTER"]
    },

    22: {
        "text": "Which is brain of computer?",
        "options": ["RAM", "CPU", "Hard Disk", "Monitor"]
    },

    23: {
        "text": "Which topology uses central hub?",
        "options": ["Ring", "Bus", "Star", "Mesh"]
    },

    24: {
        "text": "Which of the following is NoSQL database?",
        "options": ["MySQL", "Oracle", "MongoDB", "SQL Server"]
    },

    25: {
        "text": "Which keyword is used to create function in Python?",
        "options": ["function", "def", "create", "fun"]
    },

    26: {
        "text": "Which of the following is output device?",
        "options": ["Keyboard", "Mouse", "Printer", "Scanner"]
    },

    27: {
        "text": "Which layer ensures reliable data transfer?",
        "options": ["Transport Layer", "Application Layer", "Physical Layer", "Session Layer"]
    },

    28: {
        "text": "Which operator is used for exponent in Python?",
        "options": ["^", "**", "%", "//"]
    },

    29: {
        "text": "Which is default port of HTTP?",
        "options": ["80", "443", "21", "25"]
    },

    30: {
        "text": "Which is example of interpreted language?",
        "options": ["C", "C++", "Python", "Assembly"]
    } 

}


# =====================================================
# ANSWERS
# =====================================================

answer_key = {

    1: "HTTPS",
    2: "O(log n)",
    3: "Network Layer",
    4: "Queue",
    5: "DROP",
    6: "Oracle",
    7: "3NF",
    8: "SMTP",
    9: "Merge Sort",
    10: "Git",
    11: "Cache",
    12: "#",
    13: "FTP",
    14: "Stack",
    15: "Primary Key",
    16: "RAM",
    17: "HTTP",
    18: "Windows",
    19: "Stack",
    20: "Windows OS",
    21: "WHERE",
    22: "CPU",
    23: "Star",
    24: "MongoDB",
    25: "def",
    26: "Printer",
    27: "Transport Layer",
    28: "**",
    29: "80",
    30: "Python"

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
background: linear-gradient(90deg, #F6CFBE, #B9DCF2);
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
