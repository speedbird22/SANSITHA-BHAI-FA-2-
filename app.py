import streamlit as st

st.set_page_config(page_title="WaterBuddy", layout="wide")

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>

body {
    background-color: #F7F0DE;
}

/* Main title */
h1 {
    font-weight: 800 !important;
}

/* AGE BUTTONS */
.age-btn button {
    background-color: #11141C !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 20px 18px !important;
    font-size: 1.15rem !important;
    width: 100% !important;
    border: 2px solid transparent !important;
}

/* Hover effect */
.age-btn button:hover {
    background-color: #1A1E27 !important;
    border: 2px solid #5A5FEE !important;
    color: white !important;
}

/* Center text */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SESSION STATE DEFAULTS
# -------------------------
if "step" not in st.session_state:
    st.session_state.step = "age"

if "age_group" not in st.session_state:
    st.session_state.age_group = None

if "goal" not in st.session_state:
    st.session_state.goal = None


# -------------------------
# AGE DATA
# -------------------------
age_data = {
    "4–8 years":   {"cups": 5, "ml": 1180},
    "9–13 years":  {"cups": 7, "ml": 1650},
    "14–64 years": {"cups": 9, "ml": 2100},
    "65+ years":   {"cups": 7, "ml": 1650},
}


# -------------------------
# STEP 1 — AGE SELECTION
# -------------------------
if st.session_state.step == "age":

    st.markdown("<h1 style='text-align:center;'>WaterBuddy</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Choose your age group to get started!</h3>", unsafe_allow_html=True)
    st.write("")

    cols = st.columns(4)

    for idx, (age, data) in enumerate(age_data.items()):
        with cols[idx]:

            st.markdown('<div class="age-btn">', unsafe_allow_html=True)

            if st.button(f"{age} — {data['cups']} cups/day", key=f"age_{idx}"):
                st.session_state.age_group = age
                st.session_state.goal = data["ml"]
                st.session_state.step = "goal_slider"
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


# -------------------------
# STEP 2 — GOAL SLIDER (placeholder)
# -------------------------
elif st.session_state.step == "goal_slider":
    st.markdown("<h1 style='text-align:center;'>Daily Water Goal</h1>", unsafe_allow_html=True)
    st.write(f"Selected Age Group: **{st.session_state.age_group}**")
    st.write(f"Recommended Goal: **{st.session_state.goal} ml/day**")

    goal = st.slider("Adjust your daily water goal", 1000, 4000, st.session_state.goal)
    
    if st.button("Confirm Goal"):
        st.write("Goal saved!")

