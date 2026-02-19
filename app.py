from flask import Flask, request, redirect, session
import time
import openpyxl
import os

app = Flask(__name__)
app.secret_key = "exam_system_secret"

EXCEL_FILE = "results.xlsx"


# =====================================================
# CREATE EXCEL FILE IF NOT EXISTS
# =====================================================

if not os.path.exists(EXCEL_FILE):

    wb = openpyxl.Workbook()
    ws = wb.active

    ws.append([
        "Username",
        "Name",
        "Department",
        "Roll No",
        "Score",
        "Total",
        "Percentage",
        "Grade",
        "Result"
    ])

    wb.save(EXCEL_FILE)


# =====================================================
# SAVE RESULT TO EXCEL
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
        percent,
        grade,
        result
    ])

    wb.save(EXCEL_FILE)


# =====================================================
# STUDENTS
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

def calculate_grade(p):

    if p >= 90: return "A+"
    elif p >= 75: return "A"
    elif p >= 60: return "B"
    elif p >= 50: return "C"
    else: return "F"


# =====================================================
# CSS
# =====================================================

css = """

<style>

body{
margin:0;
font-family:Arial;
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

.login-box{

width:400px;
margin:auto;
margin-top:120px;
background:white;
color:black;
padding:40px;
border-radius:15px;
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
background:#ff512f;
color:white;
border:none;
border-radius:25px;
cursor:pointer;
}

.exam-container{

display:flex;
justify-content:center;
margin-top:30px;
gap:20px;
}

.logo{

width:200px;
background:white;
color:black;
padding:20px;
border-radius:15px;
text-align:center;
}

.timer{

width:200px;
background:red;
padding:20px;
border-radius:15px;
text-align:center;
font-size:22px;
}

.question-area{

width:700px;
background:white;
color:black;
padding:30px;
border-radius:15px;
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

<script>

function startTimer(duration) {

let timer = duration;

setInterval(function () {

let minutes = parseInt(timer / 60, 10)
let seconds = parseInt(timer % 60, 10)

minutes = minutes < 10 ? "0" + minutes : minutes;
seconds = seconds < 10 ? "0" + seconds : seconds;

document.getElementById("timer").textContent = minutes + ":" + seconds;

if (--timer < 0) {
timer = 0;
}

}, 1000);

}

</script>

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

    return css+"""

    <div class="login-box">

    <h2 class="center">Exam Login</h2>

    <form method="post">

    Username
    <input name="username">

    Password
    <input type="password" name="password">

    <div class="center">
    <button>Login</button>
    </div>

    </form>

    </div>
    """


# =====================================================
# EXAM
# =====================================================

@app.route("/exam", methods=["GET","POST"])
def exam():

    if "user" not in session:
        return redirect("/")

    student=students[session["user"]]

    if request.method=="POST":

        score=0

        for q in questions:

            if request.form.get(f"q{q}")==answer_key[q]:
                score+=1

        total=len(questions)
        percent=(score/total)*100
        grade=calculate_grade(percent)
        result="PASS" if percent>=50 else "FAIL"

        save_result(session["user"], student, score, total, percent, grade, result)

        return css+f"""

        <div class="login-box center">

        Name: {student['name']}<br>
        Dept: {student['dept']}<br>
        Roll: {student['roll']}<br>
        Score: {score}/{total}<br>
        Percentage: {percent:.2f}%<br>
        Grade: {grade}<br>
        Result: {result}

        </div>
        """

    html=css+"""

    <body onload="startTimer(1800)">

    <div class="exam-container">

    <div class="logo">

    <img src="YOUR_LOGO.png" width="150">

    </div>

    <div class="question-area">

    <h2 class="center">Question Paper</h2>

    <form method="post">
    """

    for qno,q in questions.items():

        html+=f"<div class='question'><b>{q['text']}</b><br>"

        for opt in q["options"]:

            html+=f"<input type='radio' name='q{qno}' value='{opt}' required>{opt}<br>"

        html+="</div>"

    html+="""<br><div class="center"><button>Submit</button></div></form></div>

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
    app.run()
