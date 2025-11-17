import streamlit as st
import random

# -------------------------------
# Hydration recommendations by age group (ml)
AGE_GROUPS = {
    "Children (4-8 years)": 1200,
    "Teens (9-13 years)": 1700,
    "Adults (14-64 years)": 2200,
    "Seniors (65+ years)": 1800,
}

HYDRATION_TIPS = [
    "Try drinking a glass of water before meals.",
    "Keep a bottle on your desk as a reminder.",
    "Start your morning with a glass of water.",
    "Set small goals: one cup every hour.",
    "Hydrate after exercise to recover faster."
]

# -------------------------------
# Initialize session state
if "goal" not in st.session_state:
    st.session_state.goal = 0
if "total" not in st.session_state:
    st.session_state.total = 0

# -------------------------------
# App Title
st.title("💧 WaterBuddy: Your Daily Hydration Companion")

st.write("Track your hydration, get friendly feedback, and build healthier habits!")

# -------------------------------
# Age group selection
age_group = st.selectbox("Select your age group:", list(AGE_GROUPS.keys()))
default_goal = AGE_GROUPS[age_group]

# Allow manual adjustment
st.session_state.goal = st.number_input(
    "Your daily water goal (ml):",
    min_value=500,
    max_value=4000,
    value=default_goal,
    step=100
)

# -------------------------------
# Logging intake
col1, col2 = st.columns(2)

with col1:
    if st.button("+250 ml"):
        st.session_state.total += 250

with col2:
    manual_amount = st.number_input("Log custom amount (ml):", min_value=0, step=50)
    if st.button("Add custom amount"):
        st.session_state.total += manual_amount

# -------------------------------
# Reset button
if st.button("🔄 New Day (Reset)"):
    st.session_state.total = 0

# -------------------------------
# Calculations
remaining = max(st.session_state.goal - st.session_state.total, 0)
progress = min(st.session_state.total / st.session_state.goal, 1.0)

# -------------------------------
# Visual feedback
st.progress(progress)

st.write(f"**Total intake so far:** {st.session_state.total} ml")
st.write(f"**Remaining to goal:** {remaining} ml")
st.write(f"**Progress:** {progress*100:.1f}%")

# -------------------------------
# Motivational messages & mascot
if progress == 0:
    st.info("Let's start hydrating! 🚰")
elif progress < 0.5:
    st.info("Good start! Keep sipping 💦")
elif progress < 0.75:
    st.success("Nice! You're halfway there 😃")
elif progress < 1.0:
    st.success("Almost at your goal! 🌊")
else:
    st.balloons()
    st.success("🎉 Congratulations! You hit your hydration goal!")

# -------------------------------
# Random hydration tip
st.write("---")
st.write("💡 Tip of the day:")
st.write(random.choice(HYDRATION_TIPS))
