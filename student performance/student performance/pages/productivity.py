import streamlit as st

st.title("⚡ Productivity Analyzer")

study_hours = st.slider(
    "Study Hours",
    0,
    12,
    4
)

sleep_hours = st.slider(
    "Sleep Hours",
    0,
    12,
    7
)

mobile_usage = st.slider(
    "Mobile Usage Hours",
    0,
    15,
    5
)

productivity_score = (
    study_hours * 10
    + sleep_hours * 5
    - mobile_usage * 4
)

st.subheader("📊 Productivity Score")

st.metric(
    "Score",
    productivity_score
)

if productivity_score >= 80:

    st.success("Excellent Productivity")

elif productivity_score >= 50:

    st.info("Average Productivity")

else:

    st.error("Low Productivity")

st.subheader("AI Suggestion")

if mobile_usage > 6:

    st.warning(
        "Reduce mobile usage for better focus."
    )

if sleep_hours < 6:

    st.warning(
        "Sleep more for better productivity."
    )