import streamlit as st
import time

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Online Exam System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CSS ---------------- #
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #1e3c72, #2a5298);
}

.title {
    text-align: center;
    color: white;
    font-size: 40px;
    font-weight: bold;
}

.login-box {
    background: white;
    padding: 40px;
    border-radius: 15px;
    width: 400px;
    margin: auto;
    margin-top: 100px;
}

.timer-box {
    background: red;
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    font-size: 24px;
}

.question-box {
    background: white;
    padding: 30px;
    border-radius: 15px;
}

.logo-box {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

div.stButton > button {
    display: block;
    margin: auto;
    background-color: #2a5298;
    color: white;
    padding: 10px 40px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- STUDENTS ---------------- #
students = {
    "CSE001": {"password": "pass001", "name": "Rahul", "branch": "CSE"},
    "CSE002": {"password": "pass002", "name": "Anitha", "branch": "CSE"},
}

# ---------------- QUESTIONS ---------------- #
questions = [
    {
        "question": "Which library is used for Machine Learning?",
        "options": ["NumPy", "Pandas", "Scikit-learn", "Matplotlib"],
        "answer": "Scikit-learn"
    },
    {
        "question": "Which function trains ML model?",
        "options": ["fit()", "train()", "learn()", "build()"],
        "answer": "fit()"
    }
]

# ---------------- SESSION ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None


# ---------------- LOGIN ---------------- #
if not st.session_state.logged_in:

    st.markdown('<h1 class="title">ONLINE EXAM SYSTEM</h1>', unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in students and students[username]["password"] == password:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.start_time = time.time()

            st.success("Login Success")
            st.rerun()

        else:
            st.error("Invalid login")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- EXAM PAGE ---------------- #
else:

    st.markdown('<h1 class="title">QUESTION PAPER</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,3,1])

    # TIMER
    with col1:

        remaining = int(1800 - (time.time() - st.session_state.start_time))

        mins = remaining // 60
        secs = remaining % 60

        st.markdown(f"""
        <div class="timer-box">
        ⏱ Time Left<br>
        {mins:02d}:{secs:02d}
        </div>
        """, unsafe_allow_html=True)

    # QUESTIONS
    with col2:

        st.markdown('<div class="question-box">', unsafe_allow_html=True)

        answers = {}

        for i, q in enumerate(questions):

            st.write(f"Q{i+1}. {q['question']}")

            answers[i] = st.radio("", q["options"], key=i)

        if st.button("Submit Exam"):

            score = 0

            for i, q in enumerate(questions):

                if answers[i] == q["answer"]:
                    score += 1

            student = students[st.session_state.username]

            st.success(f"""
Name: {student['name']}
Branch: {student['branch']}
Score: {score}/{len(questions)}
Result: {"PASS" if score>=1 else "FAIL"}
""")

        st.markdown('</div>', unsafe_allow_html=True)

    # LOGO
    with col3:

        st.markdown('<div class="logo-box">', unsafe_allow_html=True)

        st.image("https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg")

        st.markdown('</div>', unsafe_allow_html=True)
