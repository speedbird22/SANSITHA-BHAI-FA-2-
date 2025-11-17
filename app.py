import streamlit as st

# ====================== CONFIG ======================
st.set_page_config(page_title="WaterBuddy", page_icon="Water Drop", layout="wide")

# ====================== CSS ======================
st.markdown("""
<style>
    .stApp {background-color: #FFF8E7 !important; color: #1A1A1A !important;}
    .big-title {font-size: 50px; font-weight: bold; text-align: center; color: #1E90FF; font-family: 'Comic Sans MS', cursive; margin: 30px 0;}

    /* CUSTOM BUTTON STYLE FOR AGE SELECTION */
    .age-btn button {
        width: 100% !important;
        height: 150px !important;
        font-size: 28px !important;
        font-weight: bold !important;
        color: white !important;
        border-radius: 25px !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
        border: none !important;
    }
    .age-btn button:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(0,0,0,0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== STATE ======================
if 'step' not in st.session_state:
    st.session_state.step = "age_selection"
if 'age_group' not in st.session_state:
    st.session_state.age_group = None
if 'goal' not in st.session_state:
    st.session_state.goal = 2250
if 'total_intake' not in st.session_state:
    st.session_state.total_intake = 0
if 'username' not in st.session_state:
    st.session_state.username = ""

# Age data
age_data = {
    "4–8 years": {"ml": 1200, "cups": 5, "color": "#FF6B9D"},
    "9–13 years": {"ml": 1700, "cups": 7, "color": "#4DABF7"},
    "14–64 years": {"ml": 2250, "cups": 9, "color": "#51CF66"},
    "65+ years": {"ml": 1850, "cups": 7, "color": "#FFA94D"}
}

# ====================== STEP 1: AGE SELECTION ======================
if st.session_state.step == "age_selection":
    st.markdown("<h1 class='big-title'>WaterBuddy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:24px;'>Choose your age group to get started!</p>", unsafe_allow_html=True)

    cols = st.columns(4)
    for col, (age, data) in zip(cols, age_data.items()):
        with col:
            st.markdown(f"""
            <div class="age-btn">
            """, unsafe_allow_html=True)

            # REAL WORKING BUTTON
            if st.button(f"{age}\n~{data['cups']} cups/day", key=f"btn_{age}", help="", use_container_width=True):
                st.session_state.age_group = age
                st.session_state.goal = data["ml"]
                st.session_state.step = "goal_slider"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

            # set button background color
            st.markdown(
                f"""
                <style>
                    div[data-testid="stButton"][key="btn_{age.replace(" ", "_")}"] button {{
                        background-color: {data['color']} !important;
                    }}
                </style>
                """,
                unsafe_allow_html=True
            )

# ====================== STEP 2: GOAL SLIDER ======================
elif st.session_state.step == "goal_slider":
    st.markdown("<h2 class='big-title'>Set Your Daily Goal</h2>", unsafe_allow_html=True)
    suggested = age_data[st.session_state.age_group]["ml"]

    goal = st.slider("Choose your daily water intake goal", 500, 4000, suggested, 100)
    st.session_state.goal = goal

    if st.button("Continue"):
        st.session_state.step = "name_input"
        st.rerun()

# ====================== STEP 3: NAME INPUT ======================
elif st.session_state.step == "name_input":
    st.markdown("<h2 class='big-title'>What should we call you?</h2>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Your name...")

    if st.button("Let's Go!", disabled=(name.strip() == "")):
        st.session_state.username = name.strip().capitalize()
        st.session_state.step = "dashboard"
        st.rerun()

# ====================== STEP 4: DASHBOARD ======================
elif st.session_state.step == "dashboard":
    st.markdown(f"<h1 class='big-title'>Hey {st.session_state.username}!</h1>", unsafe_allow_html=True)

    total = st.session_state.total_intake
    goal = st.session_state.goal
    progress = min(100, total / goal * 100)
    remaining = max(0, goal - total)

    st.write(f"**{total} ml / {goal} ml → {remaining} ml left**")
    st.progress(progress / 100)

    st.write("### Add Water")
    cols = st.columns(4)

    for col, (label, ml) in zip(cols, [("Glass", 250), ("Small Bottle", 500), ("Medium Bottle", 1000), ("Large Bottle", 1500)]):
        with col:
            if st.button(f"{label}\n{ml} ml"):
                st.session_state.total_intake += ml
                st.rerun()

    custom = st.number_input("Custom amount (ml)", min_value=0, value=0)
    if st.button("Add Custom"):
        st.session_state.total_intake += custom
        st.rerun()

    if st.button("New Day"):
        st.session_state.total_intake = 0
        st.rerun()

    if st.button("View Summary"):
        st.session_state.step = "summary"
        st.rerun()

# ====================== STEP 5: SUMMARY ======================
elif st.session_state.step == "summary":
    st.write(f"## Summary for {st.session_state.username}")
    total = st.session_state.total_intake
    goal = st.session_state.goal

    st.write(f"**Total intake: {total} ml**")
    st.write(f"**Goal: {goal} ml**")
    if st.button("Back"):
        st.session_state.step = "dashboard"
        st.rerun()
