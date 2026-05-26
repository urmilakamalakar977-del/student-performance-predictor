import streamlit as st
import pandas as pd
import os
import random

st.set_page_config(
    page_title="Smart Student Dashboard",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Smart Student Dashboard")

st.markdown("---")

# MOTIVATION QUOTES
quotes = [
    "Success is the sum of small efforts repeated daily.",
    "Push yourself because no one else will do it for you.",
    "Dream big and dare to fail.",
    "Consistency is more important than perfection.",
    "Small progress is still progress."
]

st.info(f"💡 Motivation: {random.choice(quotes)}")

# PROFILE SECTION
st.subheader("👤 Student Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input("Student Name")

    roll = st.text_input("Roll Number")

    department = st.selectbox(
        "Department",
        [
            "Computer Engineering",
            "AI & DS",
            "Mechanical",
            "Civil",
            "ENTC"
        ]
    )

with col2:

    semester = st.selectbox(
        "Semester",
        [
            "Sem 1",
            "Sem 2",
            "Sem 3",
            "Sem 4",
            "Sem 5",
            "Sem 6",
            "Sem 7",
            "Sem 8"
        ]
    )

    goal = st.selectbox(
        "Study Goal",
        [
            "Pass Exam",
            "Improve Coding",
            "Increase CGPA",
            "Placement Preparation",
            "Learn AI"
        ]
    )

    study_time = st.selectbox(
        "Preferred Study Time",
        [
            "Morning",
            "Afternoon",
            "Evening",
            "Night"
        ]
    )

st.markdown("---")

# SUBJECT SECTION
st.subheader("📚 Subject Planner")

subjects = st.multiselect(
    "Select Subjects",
    [
        "Mathematics",
        "Python",
        "DBMS",
        "AI",
        "DSA",
        "Physics",
        "OS",
        "Java"
    ]
)

study_hours = st.slider(
    "Daily Study Hours",
    1,
    12,
    4
)

attendance = st.slider(
    "Attendance %",
    0,
    100,
    75
)

mobile_usage = st.slider(
    "Mobile Usage Hours",
    0,
    15,
    5
)

sleep_hours = st.slider(
    "Sleep Hours",
    0,
    12,
    7
)

st.markdown("---")

# MOOD TRACKER
st.subheader("😊 Mood & Focus Tracker")

mood = st.select_slider(
    "Current Mood",
    options=[
        "😞",
        "😐",
        "🙂",
        "😄",
        "🔥"
    ]
)

focus = st.slider(
    "Focus Level",
    1,
    10,
    5
)

# PRODUCTIVITY SCORE
productivity = (
    study_hours * 10
    + sleep_hours * 5
    + focus * 3
    - mobile_usage * 4
)

st.subheader("📈 Productivity Score")

st.metric(
    "Your Score",
    productivity
)

if productivity >= 100:

    st.success("🔥 Excellent Productivity")

elif productivity >= 70:

    st.info("👍 Good Productivity")

else:

    st.warning("⚠️ Improve Your Study Habits")

# AI RECOMMENDATIONS
st.subheader("🤖 AI Recommendations")

if mobile_usage > 6:

    st.warning(
        "Reduce mobile usage for better concentration."
    )

if sleep_hours < 6:

    st.warning(
        "Sleep more to improve learning ability."
    )

if attendance < 75:

    st.warning(
        "Increase attendance to improve performance."
    )

if study_hours < 3:

    st.warning(
        "Increase daily study hours."
    )

st.markdown("---")

# SAVE BUTTON
if st.button("💾 Save Student Data"):

    student_data = {

        "Name": [name],
        "Roll": [roll],
        "Department": [department],
        "Semester": [semester],
        "Goal": [goal],
        "Study Time": [study_time],
        "Subjects": [", ".join(subjects)],
        "Study Hours": [study_hours],
        "Attendance": [attendance],
        "Mobile Usage": [mobile_usage],
        "Sleep Hours": [sleep_hours],
        "Mood": [mood],
        "Focus": [focus],
        "Productivity": [productivity]
    }

    df = pd.DataFrame(student_data)

    os.makedirs("data", exist_ok=True)

    file_path = "data/student_dashboard.csv"

    if os.path.exists(file_path):

        old_df = pd.read_csv(file_path)

        new_df = pd.concat(
            [old_df, df],
            ignore_index=True
        )

        new_df.to_csv(
            file_path,
            index=False
        )

    else:

        df.to_csv(
            file_path,
            index=False
        )

    st.success("✅ Student Data Saved Successfully!")

# SHOW SAVED DATA
if os.path.exists("data/student_dashboard.csv"):

    st.subheader("📋 Saved Student Records")

    saved_df = pd.read_csv(
        "data/student_dashboard.csv"
    )

    st.dataframe(saved_df)