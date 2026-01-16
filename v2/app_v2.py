import sys
import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# -------------------------------
# PATH FIX (important)
# -------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# -------------------------------
# BACKEND IMPORTS
# -------------------------------
from v2 import progress_tracker_v2
from v2.learner_profiler_v2 import LearnerProfiler
from v2.progress_tracker_v2 import ProgressTracker

from content_manager import ContentManager
from adaptive_engine import AdaptiveEngine

from v2.question_generator import QuestionGenerator
from v2.resource_recommender import ResourceRecommender

# -------------------------------
# DATABASE + AUTH
# -------------------------------
from v2.database import init_db
from v2.auth import create_user, authenticate_user

if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_email = None


def auth_screen():
    st.markdown("## 🔐 Welcome to AI Personalized Learning")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        remember_me = st.checkbox("Remember me")

        if st.button("Login"):
            user_id = authenticate_user(email, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.current_student_id = user_id 
                st.session_state.user_email = email
                st.session_state.remember_me = remember_me
                st.rerun()
            else:
                st.error("Invalid email or password")


        st.markdown("---")
        st.button("🔵 Login with Google (Coming Soon)", disabled=True)

    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            if create_user(email, password):
                st.success("Account created! Please login.")
            else:
                st.error("Email already exists")


if not st.session_state.logged_in:
    auth_screen()
    st.stop()


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Personalized Learning System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.container():
    col1, col2 = st.columns([8, 2])
    with col2:
        with st.expander(f"👤 {st.session_state.user_email}", expanded=False):
            st.write("Account")
            st.write(f"Email: {st.session_state.user_email}")
            if st.button("Logout", key="top_logout"):
                st.session_state.show_logout_confirm = True
                st.rerun()

# -------------------------------
# STUDENT READY GUARD
# -------------------------------
if st.session_state.get("current_student_id") is None:
    st.info("Initializing your learning profile...")
    st.stop()


# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>

/* ===============================
   GLOBAL LAYOUT FIX 
   =============================== */

/* Remove Streamlit default top padding */
.stApp {
    padding-top: 0rem;
}

/* Reduce container top spacing */
.block-container {
    padding-top: 1rem !important;
}

/* ===============================
   HEADER FIX
   =============================== */

.main-header {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-top: 0.3rem;
    margin-bottom: 1.5rem;
}

/* ===============================
   METRIC CARDS
   =============================== */

.metric-card {
    background: linear-gradient(135deg,#667eea,#764ba2);
    padding: 1.2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
}

/* ===============================
   SIDEBAR CARDS
   =============================== */

.sidebar-card {
    background: #f7f9fc;
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.sidebar-title {
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.sidebar-muted {
    color: #6b7280;
    font-size: 0.85rem;
}

.divider {
    margin: 0.8rem 0;
    border-top: 1px solid #e5e7eb;
}

/* ===============================
   SIDEBAR ANIMATIONS
   =============================== */

section[data-testid="stSidebar"] {
    transition: all 0.3s ease-in-out;
}

section[data-testid="stSidebar"] button {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

section[data-testid="stSidebar"] button:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.block-container {
    padding-top: 1.2rem;
}
h1, h2, h3 {
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Make dashboard use full width */
.block-container {
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)


if st.session_state.get("large_text", False):
    st.markdown("""
    <style>
    html, body, p, span, label, div, button {
        font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)


# -------------------------------
# SESSION INIT
# -------------------------------
if "v2_init" not in st.session_state:
    st.session_state.v2_init = True
    st.session_state.progress_tracker = ProgressTracker()
    st.session_state.learner_profiler = LearnerProfiler()
    st.session_state.content_manager = ContentManager()
    st.session_state.adaptive_engine = AdaptiveEngine()

    st.session_state.current_topic = None
    st.session_state.quiz_active = False
    st.session_state.quiz_questions = []
    st.session_state.current_q = 0
    st.session_state.quiz_answers = []

student_id = st.session_state.user_id
legacy_student_id = f"student_{student_id}"  # For backward compatibility

# -------------------------------
# SESSION STATE SAFETY INIT
# -------------------------------
if "current_student_id" not in st.session_state:
    st.session_state.current_student_id = None


# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1 style='text-align:center;'>🎓 AI Personalized Learning </h1>", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR USER CARD
# -------------------------------
user_email = st.session_state.get("user_email", "user")

avatar_url = f"https://ui-avatars.com/api/?name={user_email}&background=667eea&color=fff&rounded=true"

st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        gap:12px;
        padding:12px;
        border-radius:12px;
        background:linear-gradient(135deg,#667eea,#764ba2);
        color:white;
        margin-bottom:15px;
    ">
        <img src="{avatar_url}" width="42" style="border-radius:50%;">
        <div>
            <div style="font-weight:600;">Logged in</div>
            <div style="font-size:0.85rem;opacity:0.9;">{user_email}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =============================
# SESSION STATE INITIALIZATION
# =============================

if "learning_stage" not in st.session_state:
    st.session_state.learning_stage = "topics"

if "current_topic" not in st.session_state:
    st.session_state.current_topic = None

if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []


# =============================
# APP OBJECTS
# =============================

if "adaptive_engine" not in st.session_state:
    st.session_state.adaptive_engine = AdaptiveEngine()

if "content_manager" not in st.session_state:
    st.session_state.content_manager = ContentManager()

if "progress_tracker" not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()

if "learner_profiler" not in st.session_state:
    st.session_state.learner_profiler = LearnerProfiler()

if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = None

if "question_generator" not in st.session_state:
    st.session_state.question_generator = QuestionGenerator()

if "resource_recommender" not in st.session_state:
    st.session_state.resource_recommender = ResourceRecommender()

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"

if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = "Short"   # default

if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = True

if "ai_questions" not in st.session_state:
    st.session_state.ai_questions = False   # default OFF

if "total_attempts" not in st.session_state:
    st.session_state.total_attempts = 0

if "show_hints" not in st.session_state:
    st.session_state.show_hints = True      # default ON

if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_certificate(name, topic, score):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(300, 770, "Certificate of Achievement")

    c.setFont("Helvetica", 16)
    c.drawCentredString(
        300, 700,
        f"This certifies that {name}"
    )

    c.drawCentredString(
        300, 660,
        f"has successfully completed {topic}"
    )

    c.drawCentredString(
        300, 620,
        f"with a score of {score:.1f}%"
    )

    c.drawCentredString(
        300, 560,
        "AI Personalized Learning System"
    )

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:

    # -----------------------------
    # BRANDING
    # -----------------------------
    st.markdown("""
    <div class="sidebar-card" style="text-align:center;">
        <h2>🎓 AI Learning</h2>
        <div class="sidebar-muted">Personalized Education System</div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # USER INFO
    # -----------------------------
    st.markdown(f"""
    <div class="sidebar-card">
        <div class="sidebar-title">👤 Logged in as</div>
        <div>{st.session_state.user_email}</div>
        <div class="sidebar-muted">User ID: {st.session_state.user_id}</div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # QUICK STATS
    # -----------------------------
    progress = st.session_state.progress_tracker.get_student_progress(
        st.session_state.current_student_id
    )

    st.markdown(f"""
    <div class="sidebar-card">
        <div class="sidebar-title">📊 Quick Stats</div>
        <div>🎯 Accuracy: <b>{progress.get("average_accuracy", 0):.1f}%</b></div>
        <div>📚 Activities: <b>{progress.get("total_activities", 0)}</b></div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # NAVIGATION
    # -----------------------------
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-title">🧭 Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        ["🏠 Dashboard", "📚 Start Learning", "📊 Progress Analytics", "👤 Learner Profile", "⚙️ Settings"]
    )


    # -----------------------------
    # ACTIONS
    # -----------------------------
    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-title">⚙️ Actions</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state.show_logout_confirm = True

    # -----------------------------
    # FOOTER
    # -----------------------------
    st.markdown("""
    <div class="sidebar-card sidebar-muted" style="text-align:center;">
        Need help? <br>
        📧 support@ailearning.app
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# LOGOUT CONFIRMATION
# -------------------------------
if st.session_state.get("show_logout_confirm"):

    st.markdown("""
    <div style="
        background:#fff3cd;
        padding:16px;
        border-radius:12px;
        border-left:6px solid #f59e0b;
        margin:12px 0;
    ">
        <h4>⚠️ Confirm Logout</h4>
        <p>Are you sure you want to logout?</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, Logout", key="confirm_logout"):
            for key in list(st.session_state.keys()):
                if key not in ["db_initialized"]:
                    del st.session_state[key]
            st.rerun()

    with col2:
        if st.button("Cancel", key="cancel_logout"):
            st.session_state.show_logout_confirm = False


# ======================================================
# 🏠 DASHBOARD
# ======================================================
if page == "🏠 Dashboard":

    progress = st.session_state.progress_tracker.get_student_progress(student_id)
    profile = st.session_state.learner_profiler.get_profile(student_id)

    overall = st.session_state.progress_tracker.compute_overall_score(student_id)
    accuracy = progress["average_accuracy"]
    topics = progress["topics_completed"]
    pace = profile["pace"]

    # ================= KPI CARDS =================
    st.markdown("""
    <style>
    .kpi {
        padding:20px;
        border-radius:16px;
        color:white;
        text-align:center;
        font-weight:600;
    }
    .kpi h1 { margin:0; font-size:36px; }
    .kpi p { margin:4px 0 0; opacity:0.85; }
    </style>
    """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f"""
        <div class="kpi" style="background:linear-gradient(135deg,#667eea,#764ba2)">
            <h1>{overall:.1f}%</h1>
            <p>🏆 Overall Score</p>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi" style="background:linear-gradient(135deg,#43cea2,#185a9d)">
            <h1>{accuracy:.1f}%</h1>
            <p>🎯 Accuracy</p>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi" style="background:linear-gradient(135deg,#ff9a9e,#fad0c4)">
            <h1>{topics}</h1>
            <p>📚 Topics Completed</p>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi" style="background:linear-gradient(135deg,#f7971e,#ffd200)">
            <h1>{pace}</h1>
            <p>⚡ Learning Pace</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ================= RECENT ACTIVITY + RECOMMENDATIONS =================
    left_col, right_col = st.columns([2, 1])

    # -------- LEFT SIDE: RECENT ACTIVITY --------
    with left_col:
        st.markdown("### 🕒 Recent Activity")
        recent = st.session_state.progress_tracker.get_recent_activity(
            student_id, limit=5
        )

        if recent:
            for r in recent:
                icon = "✅" if r["is_correct"] else "❌"
                st.markdown(
                    f"""
                    <div style="
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:10px;
                        background:#f8fafc;
                        border-left:5px solid {'#22c55e' if r['is_correct'] else '#ef4444'};
                    ">
                        <b>{icon} {r['topic']}</b><br>
                        <small>{r['description']} • {r['date']}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No recent activity yet.")

    # -------- RIGHT SIDE: RECOMMENDATIONS --------
    with right_col:
        st.markdown("### 🎯 Personalized Recommendations")

        recs = st.session_state.adaptive_engine.get_recommendations(
            legacy_student_id
        )

        if not recs:
            st.success("🎉 You're doing great! No immediate recommendations.")
        else:
            for i, rec in enumerate(recs[:3]):
                with st.container(border=True):
                    st.markdown(f"#### 🧠 {rec['title']}")
                    st.write(rec["description"])

                    if st.button(
                        f"🚀 Start {rec['topic']}",
                        key=f"rec_{i}",
                        use_container_width=True
                    ):
                        st.session_state.current_topic = rec["topic"]
                        st.session_state.learning_stage = "topic"
                        st.rerun()


# ======================================================
# 📚 START LEARNING + QUIZ FLOW
# ======================================================
elif page == "📚 Start Learning":

    # =====================================================
    # 🎯 HEADER
    # =====================================================
    st.markdown("## 🚀 Start Learning")
    st.caption("Personalized • Adaptive • Quiz-based learning")
    st.markdown("---")

    # =====================================================
    # 🟢 STAGE 1 — TOPIC LIST
    # =====================================================
    if st.session_state.learning_stage == "topics":

        topics = st.session_state.content_manager.get_available_topics()
        cols = st.columns(3)

        for i, topic in enumerate(topics):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### 📘 {topic}")
                    st.caption("Practice • Master • Advance")

                    st.write(
                        "Build strong fundamentals with adaptive quizzes."
                    )

                    if st.button("▶ Start Learning", key=f"topic_{topic}", use_container_width=True):
                        st.session_state.current_topic = topic
                        st.session_state.learning_stage = "topic"
                        st.rerun()

    # =====================================================
    # 🟡 STAGE 2 — TOPIC OVERVIEW
    # =====================================================
    elif st.session_state.learning_stage == "topic":

        topic = st.session_state.current_topic
        content = st.session_state.content_manager.get_topic_content(topic, student_id)

        st.markdown(f"## 📚 {content['title']}")
        st.write(content["description"])

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Back to Topics", use_container_width=True):
                st.session_state.learning_stage = "topics"
                st.session_state.current_topic = None
                st.rerun()

        with col2:
            if st.button("🎯 Start Quiz", type="primary", use_container_width=True):
                difficulty = st.session_state.adaptive_engine.adapt_difficulty(
                    student_id, topic
                )

                st.session_state.quiz_questions = (
                    st.session_state.content_manager.generate_quiz(
                        topic, student_id, difficulty=difficulty
                    )
                )

                st.caption(f"🎯 Difficulty: {difficulty}")

                st.session_state.quiz_active = True
                st.session_state.quiz_topic = topic
                st.session_state.current_q = 0
                st.session_state.quiz_answers = []
                st.session_state.question_start_time = datetime.now()
                st.session_state.learning_stage = "quiz"
                st.session_state.asked_questions = set()
                st.rerun()


    # =====================================================
    # 🔵 STAGE 3 — QUIZ FLOW
    # =====================================================
    elif st.session_state.learning_stage == "quiz":

        # ---------------------------------
        # SAFE INITIALIZATION
        # ---------------------------------
        if "question_count" not in st.session_state:
            st.session_state.question_count = 0

        if "score" not in st.session_state:
            st.session_state.score = 0

        if "difficulty" not in st.session_state:
            st.session_state.difficulty = "Easy"

        # ---------------------------------
        # GENERATE QUESTION ONLY ONCE
        # ---------------------------------
        if "current_question" not in st.session_state:

            if st.session_state.get("ai_questions", False):
                q = st.session_state.question_generator.generate_ai_question(
                    st.session_state.current_topic,
                    st.session_state.difficulty
                )
            else:
                q = st.session_state.question_generator.generate_question(
                    st.session_state.current_topic,
                    st.session_state.difficulty
                )

            # 🔐 HARD VALIDATION
            if (
                not q
                or "question" not in q
                or "options" not in q
                or not isinstance(q["options"], list)
                or len([o for o in q["options"] if str(o).strip()]) < 2
            ):
                st.warning("⚠️ Invalid question skipped")
                st.session_state.question_count += 1
                st.session_state.question_start_time = datetime.now()
                st.rerun()

            st.session_state.current_question = q
            st.session_state.question_start_time = datetime.now()

        q = st.session_state.current_question

        # ---------------------------------
        # CLEAN OPTIONS
        # ---------------------------------
        def clean_options(options):
            return [str(o).strip() for o in options if o and str(o).strip()]

        cleaned_options = clean_options(q["options"])

        if len(cleaned_options) < 2:
            st.warning("⚠️ Question skipped due to invalid options")
            del st.session_state.current_question
            st.rerun()

        # ---------------------------------
        # UI
        # ---------------------------------
        st.markdown(
            f"### ❓ Question {st.session_state.question_count + 1} "
            f"({st.session_state.difficulty})"
        )
        st.markdown(f"**{q['question']}**")

        # ---------------------------------
        # FORM (PREVENTS AUTO RERUN)
        # ---------------------------------
        with st.form(key=f"quiz_form_{st.session_state.question_count}"):

            answer = st.radio(
                "Choose an answer:",
                cleaned_options,
                key=f"q_{st.session_state.question_count}_radio"
            )

            col1, col2 = st.columns(2)
            skip = col1.form_submit_button("⏭ Skip")
            submit = col2.form_submit_button("✅ Submit", type="primary")

        # ---------------------------------
        # ⏭ SKIP LOGIC
        # ---------------------------------
        if skip:
            st.session_state.question_count += 1
            del st.session_state.current_question
            st.session_state.question_start_time = datetime.now()
            st.rerun()

        # ---------------------------------
        # ✅ SUBMIT LOGIC
        # ---------------------------------
        if submit:
            correct = answer == q["correct_answer"]

            response_time = (
                datetime.now() - st.session_state.question_start_time
            ).total_seconds()

            # SAVE RESULT
            st.session_state.progress_tracker.record_quiz_response(
                student_id,
                st.session_state.current_topic,
                correct,
                response_time
            )

            st.session_state.total_attempts += 1
            st.session_state.question_count += 1

            if correct:
                st.session_state.score += 1
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Correct answer: {q['correct_answer']}")

            # AUTO DIFFICULTY
            accuracy = (
                st.session_state.score /
                max(1, st.session_state.question_count)
            ) * 100

            if accuracy >= 80:
                st.session_state.difficulty = "Hard"
            elif accuracy >= 50:
                st.session_state.difficulty = "Medium"
            else:
                st.session_state.difficulty = "Easy"

            del st.session_state.current_question
            st.session_state.question_start_time = datetime.now()

            if st.session_state.question_count >= 10:
                st.session_state.learning_stage = "result"

            st.rerun()


    # =====================================================
    # 🟣 STAGE 4 — QUIZ RESULT PAGE
    # =====================================================
    elif st.session_state.learning_stage == "result":

        # ----------------------------------
        # SAFE ACCURACY CALCULATION
        # ----------------------------------
        total_questions = max(1, st.session_state.question_count)
        accuracy = (st.session_state.score / total_questions) * 100

        if not st.session_state.get("reduce_animations", False):
            st.balloons()


        # ----------------------------------
        # 🎉 CENTERED COMPLETION PANEL
        # ----------------------------------
        st.markdown(
            f"""
            <div style="
                max-width:650px;
                margin:auto;
                padding:32px;
                border-radius:18px;
                background:linear-gradient(135deg,#667eea,#764ba2);
                color:white;
                text-align:center;
                box-shadow:0 10px 30px rgba(0,0,0,0.2);
            ">
                <h1>🏆 Quiz Completed</h1>
                <h2>{accuracy:.1f}% Accuracy</h2>
                <p style="font-size:16px;">
                    You answered <b>{st.session_state.score}</b> out of
                    <b>{total_questions}</b> questions correctly.
                </p>
                <p>Keep pushing forward 🚀</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # ----------------------------------
        # 📊 TOPIC MASTERY RING
        # ----------------------------------
        topic_progress = st.session_state.progress_tracker.get_topic_progress(
            student_id,
            st.session_state.current_topic
        )

        mastery = topic_progress.get("accuracy", accuracy)

        fig = px.pie(
            values=[mastery, 100 - mastery],
            names=["Mastered", "Remaining"],
            hole=0.65,
            color_discrete_sequence=["#667eea", "#e0e0e0"]
        )

        fig.update_layout(
            showlegend=False,
            annotations=[dict(
                text=f"{mastery:.1f}%",
                font_size=26,
                showarrow=False
            )]
        )

        st.markdown("### 📊 Topic Mastery")
        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------------
        # 🚀 ADAPTIVE NEXT STEPS
        # ----------------------------------
        next_steps = st.session_state.adaptive_engine.get_next_steps(
            legacy_student_id,
            st.session_state.current_topic,
            accuracy
        )

        with st.container(border=True):
            st.markdown("### 🚀 What’s Next?")
            st.write(next_steps["message"])

        # ----------------------------------
        # 📚 LEARNING RESOURCES (IF NEEDED)
        # ----------------------------------
        if accuracy < 70:
            st.markdown("### 📘 Recommended Resources")

            resources = st.session_state.resource_recommender.recommend(
                st.session_state.current_topic
            )

            for link in resources:
                st.write(f"🔗 {link}")

        # ----------------------------------
        # 🎓 CERTIFICATE GENERATION
        # ----------------------------------
        cert_pdf = generate_certificate(
            st.session_state.user_email,
            st.session_state.current_topic,
            accuracy
        )

        st.download_button(
            "🎓 Download Certificate",
            cert_pdf,
            file_name="certificate.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.markdown("---")

        # ----------------------------------
        # 🔁 NAVIGATION BUTTONS
        # ----------------------------------
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📘 Learn Another Topic", use_container_width=True):
                st.session_state.learning_stage = "topics"
                st.session_state.current_topic = None
                st.session_state.question_count = 0
                st.session_state.score = 0
                st.session_state.difficulty = "Easy"
                st.rerun()

        with col2:
            if st.button("🔁 Retry Quiz", use_container_width=True):
                st.session_state.learning_stage = "quiz"
                st.session_state.question_count = 0
                st.session_state.score = 0
                st.session_state.difficulty = "Easy"
                st.session_state.asked_questions.clear()
                st.rerun()


# ======================================================
# 📊 ANALYTICS
# ======================================================
elif page == "📊 Progress Analytics":
    st.markdown("## 📊 Learning Analytics Dashboard")

    history = st.session_state.progress_tracker.get_learning_history(student_id)

    if not history:
        st.info("No learning data yet. Start learning to see analytics!")
        st.stop()

    df = pd.DataFrame(history)
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.date

    # -------------------------------
    # KPI METRICS
    # -------------------------------
    st.markdown("### 📌 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🎯 Avg Accuracy",
        f"{df['accuracy'].mean():.1f}%"
    )

    col2.metric(
        "🧠 Total Attempts",
        len(df)
    )

    col3.metric(
        "⏱ Avg Response Time",
        f"{df['response_time'].mean():.1f}s"
    )

    col4.metric(
        "📚 Topics Practiced",
        df["topic"].nunique()
    )

    st.markdown("---")

    # -------------------------------
    # ACCURACY OVER TIME
    # -------------------------------
    st.markdown("### 📈 Accuracy Over Time")

    acc_time = df.groupby("date")["accuracy"].mean().reset_index()

    fig1 = px.line(
        acc_time,
        x="date",
        y="accuracy",
        markers=True,
        title="Accuracy Trend",
        labels={"accuracy": "Accuracy (%)", "date": "Time"},
        template="plotly_white"
    )

    fig1.update_traces(line=dict(width=3))
    st.plotly_chart(fig1, use_container_width=True)

    # -------------------------------
    # TOPIC PERFORMANCE
    # -------------------------------
    st.markdown("### 📊 Topic-wise Performance")

    topic_perf = df.groupby("topic")["accuracy"].mean().reset_index()

    fig2 = px.bar(
        topic_perf,
        x="topic",
        y="accuracy",
        text_auto=".1f",
        labels={"accuracy": "Accuracy (%)", "topic": "Topic"},
        template="plotly_white"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------
    # ACTIVITY FREQUENCY
    # -------------------------------
    st.markdown("### 📅 Learning Activity Frequency")

    activity = df.groupby("day").size().reset_index(name="Attempts")

    fig3 = px.bar(
        activity,
        x="day",
        y="Attempts",
        labels={"day": "Date"},
        template="plotly_white"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -------------------------------
    # AI INSIGHTS
    # -------------------------------
    st.markdown("### 🤖 AI Insights")

    best_topic = topic_perf.sort_values("accuracy", ascending=False).iloc[0]

    insight_text = f"""
    ✅ **Strongest Topic:** {best_topic['topic']} ({best_topic['accuracy']:.1f}% accuracy)  
    📈 **Overall Trend:** {'Improving' if acc_time['accuracy'].iloc[-1] >= acc_time['accuracy'].iloc[0] else 'Needs Attention'}  
    💡 **Suggestion:** Practice weaker topics to balance performance.
    """

    st.success(insight_text)

    # ==================================================
    # 🔥 ADVANCED ANALYTICS
    # ==================================================

    st.markdown("---")
    st.markdown("## 🚀 Advanced Learning Insights")

    # -------------------------------
    # 1️⃣ ACCURACY vs TIME HEATMAP
    # -------------------------------
    st.markdown("### 🔥 Accuracy vs Time Heatmap")

    heatmap_df = df.copy()
    heatmap_df["time_bucket"] = pd.cut(
        heatmap_df["response_time"],
        bins=[0, 30, 60, 90, 200],
        labels=["Fast", "Medium", "Slow", "Very Slow"]
    )

    heatmap_data = heatmap_df.groupby(
        ["topic", "time_bucket"]
    )["accuracy"].mean().reset_index()

    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="time_bucket",
        y="topic",
        z="accuracy",
        color_continuous_scale="Blues",
        title="Accuracy vs Response Time"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    # -------------------------------
    # 2️⃣ DIFFICULTY-WISE ANALYTICS
    # -------------------------------
    st.markdown("### 🎚 Difficulty-wise Performance")

    difficulty_map = {
        "Easy": ["Basics", "Introduction"],
        "Medium": ["Intermediate"],
        "Hard": ["Advanced"]
    }

    def infer_difficulty(topic):
        for level, keywords in difficulty_map.items():
            for k in keywords:
                if k.lower() in topic.lower():
                    return level
        return "Medium"

    df["difficulty"] = df["topic"].apply(infer_difficulty)

    diff_perf = df.groupby("difficulty")["accuracy"].mean().reset_index()

    fig_diff = px.bar(
        diff_perf,
        x="difficulty",
        y="accuracy",
        text_auto=".1f",
        title="Accuracy by Difficulty Level",
        template="plotly_white"
    )

    st.plotly_chart(fig_diff, use_container_width=True)

    # -------------------------------
    # 3️⃣ WEEKLY STREAK COUNTER
    # -------------------------------
    st.markdown("### 🔥 Weekly Learning Streak")

    df["day"] = df["date"].dt.date
    unique_days = sorted(df["day"].unique())

    streak = 1
    max_streak = 1

    for i in range(1, len(unique_days)):
        if (unique_days[i] - unique_days[i - 1]).days == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    st.metric(
        "📅 Longest Learning Streak",
        f"{max_streak} days"
    )

    # -------------------------------
    # 4️⃣ DOWNLOAD ANALYTICS AS PDF
    # -------------------------------
    st.markdown("### 📥 Download Your Analytics")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 Download Analytics (CSV)",
        data=csv,
        file_name="learning_analytics.csv",
        mime="text/csv"
    )

    # -------------------------------
    # 5️⃣ COMPARISON vs AVERAGE LEARNER
    # -------------------------------
    st.markdown("### 🆚 You vs Average Learner")

    avg_accuracy = 65  # baseline assumption
    user_accuracy = df["accuracy"].mean()

    comp_df = pd.DataFrame({
        "Category": ["You", "Average Learner"],
        "Accuracy": [user_accuracy, avg_accuracy]
    })

    fig_comp = px.bar(
        comp_df,
        x="Category",
        y="Accuracy",
        text_auto=".1f",
        title="Performance Comparison",
        template="plotly_white"
    )

    st.plotly_chart(fig_comp, use_container_width=True)


# ======================================================
# 👤 LEARNER PROFILE
# ======================================================
elif page == "👤 Learner Profile":
    profile = st.session_state.learner_profiler.update_profile(student_id)

    topic_progress = st.session_state.progress_tracker.get_all_topic_progress(student_id)

    areas_to_improve = []

    for topic, data in topic_progress.items():
        if data["attempts"] >= 3 and data["accuracy"] < 60:
            areas_to_improve.append({
                "topic": topic,
                "accuracy": data["accuracy"]
            })


    st.markdown("## 🧠 Learner Profile")

    # -------------------------
    # TOP CARDS
    # -------------------------
    c1, c2, c3, c4 = st.columns(4)

    overall = st.session_state.progress_tracker.compute_overall_score(student_id)

    c1.metric("🎯 Overall Score", f"{overall:.1f}%")
    c2.metric("📊 Accuracy", f"{profile['average_accuracy']}%")
    c3.metric("🏆 Level", profile["level"])
    c4.metric("🏅 Badge", profile["badge"])

    st.divider()

    # -------------------------
    # TRAITS SECTION
    # -------------------------
    t1, t2, t3, t4 = st.columns(4)

    t1.progress(
        {"Low": 0.3, "Medium": 0.6, "High": 1}[profile["engagement"]],
        text=f"Engagement: {profile['engagement']}"
    )

    t2.progress(
        {"Slow": 0.3, "Moderate": 0.6, "Fast": 1}[profile["pace"]],
        text=f"Pace: {profile['pace']}"
    )

    t3.progress(
        {"Low": 0.3, "Medium": 0.6, "High": 1}[profile["confidence"]],
        text=f"Confidence: {profile['confidence']}"
    )

    t4.progress(
        {"Easy": 0.3, "Medium": 0.6, "Hard": 1}[profile["preferred_difficulty"]],
        text=f"Preferred Difficulty: {profile['preferred_difficulty']}"
    )

    st.divider()

    # -------------------------
    # STRENGTHS & WEAKNESSES
    # -------------------------
    s1, s2 = st.columns(2)

    # -------------------------
    # DERIVED STRENGTHS
    # -------------------------
    derived_strengths = []

    if profile["confidence"] in ["High", "Medium"]:
        derived_strengths.append(("Confidence", profile["confidence"]))

    if profile["pace"] in ["Fast", "Moderate"]:
        derived_strengths.append(("Learning Pace", profile["pace"]))

    if profile["engagement"] in ["High", "Medium"]:
        derived_strengths.append(("Engagement", profile["engagement"]))

    if profile["average_accuracy"] >= 70:
        derived_strengths.append(("Accuracy", f"{profile['average_accuracy']}%"))

    # Fallback (never empty)
    if not derived_strengths:
        derived_strengths = [
            ("Consistency", "Building"),
            ("Focus", "Improving"),
        ]

    MIN_STRENGTH_CARDS = 6
    with s1:
        st.subheader("💪 Strengths")

        strengths = profile.get("strengths", [])

        # ---- Pad with placeholders if few strengths ----
        while len(strengths) < MIN_STRENGTH_CARDS:
            strengths.append("Emerging skill")

        cols = st.columns(3)

        for i, s in enumerate(strengths[:MIN_STRENGTH_CARDS]):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div style="
                        padding:16px;
                        border-radius:14px;
                        background:linear-gradient(135deg,#43cea2,#185a9d);
                        color:white;
                        margin-bottom:14px;
                        box-shadow:0 4px 12px rgba(0,0,0,0.15);
                    ">
                        <div style="font-size:14px; opacity:0.85;">Strength</div>
                        <div style="font-size:18px; font-weight:700;">
                            {s if s != "Emerging skill" else "✨ Emerging skill"}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.caption("✨ Strengths evolve as you practice more quizzes")

    with s2:
        st.markdown("### ⚠️ Areas to Improve")

        if len(areas_to_improve) == 0:
            st.success("🎉 No major weak areas detected. Keep practicing to maintain consistency!")
        else:
            for area in areas_to_improve:
                st.markdown(
                    f"""
                    <div style="
                        padding:12px;
                        border-radius:10px;
                        margin-bottom:10px;
                        background:#fff3cd;
                        border-left:6px solid #ff9800;
                    ">
                        <b>📌 {area['topic']}</b><br>
                        Accuracy: {area['accuracy']:.1f}%<br>
                        <i>Recommended: Revise basics & practice more questions</i>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.divider()

    # -------------------------
    # AI SUMMARY
    # -------------------------
    st.subheader("🤖 AI Insight")
    st.info(
        f"You are a **{profile['level']}** learner with **{profile['engagement']} engagement** "
        f"and **{profile['confidence']} confidence**. "
        f"Focus on improving weaker areas to unlock the next badge 🚀"
    )

# ======================================================
# ⚙️ SETTINGS
# ======================================================
elif page == "⚙️ Settings":

    st.markdown("## ⚙️ Settings")
    st.caption("Customize your learning experience")

    # --------------------------------------------------
    # SAFE PROFILE LOAD
    # --------------------------------------------------
    profile = st.session_state.learner_profiler.get_profile(student_id)

    # --------------------------------------------------
    # SESSION DEFAULTS (VERY IMPORTANT)
    # --------------------------------------------------
    if "auto_difficulty" not in st.session_state:
        st.session_state.auto_difficulty = True

    if "show_hints" not in st.session_state:
        st.session_state.show_hints = True

    if "shuffle_options" not in st.session_state:
        st.session_state.shuffle_options = True

    if "daily_goal" not in st.session_state:
        st.session_state.daily_goal = 30

    if "ai_questions" not in st.session_state:
        st.session_state.ai_questions = False

    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    # --------------------------------------------------
    # 👤 PROFILE CARD
    # --------------------------------------------------
    with st.container(border=True):
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(
                f"""
                <div style="
                    width:80px;
                    height:80px;
                    border-radius:50%;
                    background:linear-gradient(135deg,#667eea,#764ba2);
                    color:white;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:32px;
                    font-weight:bold;
                ">
                    {st.session_state.user_email[0].upper()}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(f"**👤 User:** {st.session_state.user_email}")
            st.markdown("🎓 Role: Learner")
            st.markdown("📊 Learning Mode: Adaptive")

    st.markdown("---")

    # --------------------------------------------------
    # 🎯 LEARNING PREFERENCES
    # --------------------------------------------------
    st.markdown("### 🎯 Learning Preferences")

    preferred_difficulty = st.select_slider(
        "Preferred Difficulty",
        options=["Easy", "Medium", "Hard"],
        value=profile.get("preferred_difficulty", "Medium")
    )

    # Learning style is stored for future personalization
    # (content format, hints, explanations)
    learning_style = st.selectbox(
        "Learning Style",
        ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
        index=["Visual", "Auditory", "Reading/Writing", "Kinesthetic"]
        .index(profile.get("style", "Visual"))
    )

    daily_goal = st.slider(
        "Daily Study Goal (minutes)",
        min_value=10,
        max_value=120,
        step=10,
        value=st.session_state.daily_goal
    )

    st.markdown("---")

    # --------------------------------------------------
    # 🧠 QUIZ BEHAVIOR
    # --------------------------------------------------
    st.markdown("### 🧠 Quiz Behavior")

    auto_difficulty = st.toggle(
        "Auto-adjust difficulty based on performance",
        value=st.session_state.auto_difficulty
    )

    show_hints = st.toggle(
        "Show AI hints when struggling",
        value=st.session_state.show_hints
    )

    shuffle_options = st.toggle(
        "Shuffle answer options",
        value=st.session_state.shuffle_options
    )

    st.info(
        "💡 Turning OFF shuffle will prevent option re-ordering during quiz attempts."
    )

    st.markdown("---")

    # --------------------------------------------------
    # 🤖 AI FEATURES
    # --------------------------------------------------
    st.markdown("### 🤖 AI Features")

    ai_questions = st.toggle(
        "Enable AI-generated questions (beta)",
        value=st.session_state.get("ai_questions", False)
    )

    st.session_state.ai_questions = ai_questions


    ai_feedback = st.radio(
        "AI Feedback Style",
        ["Short", "Detailed"],
        index=["Short", "Detailed"].index(
            st.session_state.get("ai_feedback", "Short")
        ),
        horizontal=True
    )

    st.session_state.ai_feedback = ai_feedback


    st.markdown("---")

    # --------------------------------------------------
    # ♿ ACCESSIBILITY
    # --------------------------------------------------
    st.markdown("### ♿ Accessibility")

    large_text = st.toggle(
        "Large Text Mode",
        value=st.session_state.get("large_text", False)
    )
    st.session_state.large_text = large_text

    reduce_animations = st.toggle(
        "Reduce Animations",
        value=st.session_state.get("reduce_animations", False)
    )
    st.session_state.reduce_animations = reduce_animations


    st.markdown("---")

    # --------------------------------------------------
    # 💾 SAVE SETTINGS
    # --------------------------------------------------
    if st.button("💾 Save Preferences", use_container_width=True):

        st.session_state.daily_goal = daily_goal
        st.session_state.auto_difficulty = auto_difficulty
        st.session_state.show_hints = show_hints
        st.session_state.shuffle_options = shuffle_options
        st.session_state.ai_questions = ai_questions

        st.session_state.learner_profiler.update_preferences(
            student_id,
            {
                "preferred_difficulty": preferred_difficulty,
                "style": learning_style,
                "daily_goal": daily_goal,
                "auto_difficulty": auto_difficulty,
                "show_hints": show_hints,
                "shuffle_options": shuffle_options,
                "ai_questions": ai_questions,
            }
        )

        st.success("✅ Preferences saved successfully!")

    # --------------------------------------------------
    # ⚠️ DANGER ZONE
    # --------------------------------------------------
    with st.expander("⚠️ Danger Zone"):
        if st.button("🗑 Reset Learning Progress", type="secondary"):
            st.session_state.progress_tracker.reset_student_progress(student_id)
            st.warning("Progress reset. Restart app for clean state.")
