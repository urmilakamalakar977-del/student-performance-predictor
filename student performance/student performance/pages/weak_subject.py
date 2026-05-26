import streamlit as st
import pandas as pd

st.title("📉 Weak Subject Analyzer")

math = st.slider("Math Marks", 0, 100, 60)
physics = st.slider("Physics Marks", 0, 100, 70)
python_marks = st.slider("Python Marks", 0, 100, 80)
dbms = st.slider("DBMS Marks", 0, 100, 65)

marks = {
    "Mathematics": math,
    "Physics": physics,
    "Python": python_marks,
    "DBMS": dbms
}

weak_subject = min(
    marks,
    key=marks.get
)

strong_subject = max(
    marks,
    key=marks.get
)

st.error(f"Weak Subject: {weak_subject}")

st.success(f"Strong Subject: {strong_subject}")

st.subheader("AI Recommendation")

st.info(
    f"Focus more on {weak_subject} and practice daily."
)

df = pd.DataFrame(
    list(marks.items()),
    columns=["Subject", "Marks"]
)

st.bar_chart(df.set_index("Subject"))