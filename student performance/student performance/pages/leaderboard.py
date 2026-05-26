import streamlit as st
import pandas as pd

st.title("🏆 Student Leaderboard")

data = {
    "Student": [
        "Aarav",
        "Riya",
        "Urmila",
        "Kunal",
        "Sneha"
    ],

    "Study Hours": [
        8,
        7,
        9,
        6,
        5
    ],

    "Consistency": [
        95,
        88,
        99,
        80,
        75
    ]
}

df = pd.DataFrame(data)

st.dataframe(df)

st.bar_chart(
    df.set_index("Student")["Consistency"]
)

st.success("Top Student: Urmila 🔥")