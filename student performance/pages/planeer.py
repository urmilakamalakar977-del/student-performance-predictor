import streamlit as st
import pandas as pd
import os

st.title("📅 Smart Study Planner")

st.write("Create your personalized study timetable")

subjects = st.multiselect(
    "Select Subjects",
    [
        "Mathematics",
        "Physics",
        "Chemistry",
        "Python",
        "DBMS",
        "AI",
        "DSA",
        "OS"
    ]
)

study_time = st.slider(
    "Study Hours Per Day",
    1,
    12,
    4
)

exam_days = st.slider(
    "Days Left For Exam",
    1,
    60,
    15
)

difficulty = st.selectbox(
    "Difficulty Level",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

if st.button("Generate Study Plan"):

    timetable = []

    for subject in subjects:

        timetable.append({
            "Subject": subject,
            "Hours Per Day": round(
                study_time / len(subjects),
                1
            ),
            "Difficulty": difficulty
        })

    df = pd.DataFrame(timetable)

    st.subheader("📚 Your Study Timetable")

    st.dataframe(df)

    st.success("Study Plan Generated!")