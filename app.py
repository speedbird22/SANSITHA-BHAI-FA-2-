# app.py
import streamlit as st

# ====================== CONFIG ======================
st.set_page_config(page_title="WaterBuddy", page_icon="Water Drop", layout="wide")

# ====================== CSS ======================
st.markdown("""
<style>
    .stApp {background-color: #FFF8E7 !important; color: #1A1A1A !important;}
    .big-title {font-size: 50px; font-weight: bold; text-align: center; color: #1E90FF; font-family: 'Comic Sans MS', cursive; margin: 30px 0;}
    .age-btn {
        width: 100%; 
        height: 140px; 
        font-size: 28px; 
        font-weight: bold; 
        border-radius: 25px; 
        margin: 20px 0; 
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        color: white !important;
        padding: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .age-btn:hover {transform: scale(1.05); box-shadow: 0 10px 20px rgba(0,0,0,0.2);}
    .slider-label {font-size: 22px; font-weight: bold; color: #2E8B57; text-align: center;}
    .mascot {font-size: 110px; text-align: center; margin: 30px 0;}
    .progress-box {background: #E0F7FA; padding: 20px; border-radius: 18px; text-align: center; font-size: 24px; font-weight: bold; color: #1A1A1A;}
    .water-btn {
        background: linear-gradient(45deg, #4FC3F7, #29B6F6); 
        color: white; 
        font-weight: bold; 
        border-radius: 18px; 
        padding: 20px; 
        font-size: 20px; 
        height: 100px;
    }
    .water-btn:hover {background: #0288D1; transform: scale(1.03);}
    .summary-box {background: #E8F5E9; padding: 25px; border-radius: 18px; font-size: 20px; color: #1A1A1A;}
    .fade-in {animation: fadeIn 1.2s ease-in;}
    @keyframes fadeIn {from {opacity: 0; transform: translateY(30px);} to {opacity: 1; transform: translateY(0);}}
    /* Hide all Streamlit buttons */
    .stButton > button {display: none !important;}
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

# ====================== STEP 1: AGE SELECTION (ONLY CUSTOM BUTTONS) ======================
if st.session_state.step == "age_selection":
    st.markdown("<h1 class='big-title'>WaterBuddy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:24px; color:#1A1A1A; margin-bottom:40px;'>Choose your age group to get started!</p>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    for idx, (age, data) in enumerate(age_data.items()):
        with cols[idx]:
            # Hidden button for action
            if st.button("", key=f"hidden_{age}"):
                st.session_state.age_group = age
                st.session_state.goal = data['ml']
                st.session_state.step = "goal_slider"
                st.rerun()
            
            # Custom clickable div
            st.markdown(f"""
            <div class='age-btn' style='background:{data['color']};' 
                 onclick="document.querySelector('[data-testid=\"stButton\"][key=\"hidden_{age}\"]').click();">
                <strong>{age}</strong><br>
                ~{data['cups']} cups/day
            </div>
            """, unsafe_allow_html=True)

# ====================== REST OF APP (SAME AS BEFORE) ======================
elif st.session_state.step == "goal_slider":
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.markdown("<h2 class='big-title'>Set Your Daily Goal</h2>", unsafe_allow_html=True)
    
    suggested = age_data[st.session_state.age_group]["ml"]
    goal = st.slider("Choose your daily water intake goal", 500, 4000, suggested, 100, "%d ml")
    st.session_state.goal = goal

    zone = "Perfect Zone"
    if goal < suggested * 0.7: zone = "Too Low"
    elif goal < suggested: zone = "A Bit Low"
    elif goal > suggested * 1.3: zone = "Ambitious!"

    st.markdown(f"<pclass='slider-label'>{zone}</p>", unsafe_allow_html=True)
    st.info(f"Recommended: {suggested} ml")

    if st.button("Continue", use_container_width=True):
        st.session_state.step = "name_input"
        st.rerun()

elif st.session_state.step == "name_input":
    st.markdown("<h2 class='big-title'>What should we call you?</h2>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Enter your name...", label_visibility="collapsed")
    if st.button("Let's Go!", disabled=not name.strip()):
        st.session_state.username = name.strip().capitalize()
        st.session_state.step = "dashboard"
        st.rerun()

elif st.session_state.step == "dashboard":
    st.markdown(f"<h1 class='big-title'>Hey {st.session_state.username}!</h1>", unsafe_allow_html=True)
    
    total = st.session_state.total_intake
    goal = st.session_state.goal
    progress = min(100, total / goal * 100) if goal else 0
    remaining = max(0, goal - total)

    st.markdown(f"<div class='progress-box'>{int(total)} ml / {goal} ml → <strong>{int(remaining)} ml</strong> left</div>", unsafe_allow_html=True)
    st.progress(progress / 100)

    msg = "Time to drink up!" if progress == 0 else "Every sip counts!" if progress < 50 else "Great job!" if progress < 75 else "Almost there!" if progress < 100 else "GOAL ACHIEVED!"
    mascot = "Sad" if progress == 0 else "Neutral" if progress < 50 else "Smiling" if progress < 75 else "Happy" if progress < 100 else "Celebrating"

    st.markdown(f"<div class='mascot'>{mascot}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:24px; color:#2E8B57;'><strong>{msg}</strong></p>", unsafe_allow_html=True)

    st.markdown("### Add Water")
    cols = st.columns(4)
    for col, (label, ml) in zip(cols, [("Glass", 250), ("Small Bottle", 500), ("Medium Bottle", 1000), ("Large Bottle", 1500)]):
        with col:
            if st.button(f"{label}\n{ml} ml", use_container_width=True):
                st.session_state.total_intake += ml
                st.success(f"+{ml} ml!")
                st.rerun()

    custom = st.number_input("Custom (ml)", 0, step=50)
    if st.button("Add Custom", use_container_width=True):
        st.session_state.total_intake += custom
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("New Day"):
            st.session_state.total_intake = 0
            st.rerun()
    with col2:
        if st.button("View Summary"):
            st.session_state.step = "summary"
            st.rerun()

elif st.session_state.step == "summary":
    st.markdown(f"<h1 class='big-title'>Summary</h1>", unsafe_allow_html=True)
    progress = st.session_state.total_intake / st.session_state.goal * 100
    title = "GOAL ACHIEVED!" if progress >= 100 else "Great Effort!" if progress >= 75 else "Good Start!"
    st.markdown(f"<div class='summary-box'><strong>{title}</strong><br>You drank {st.session_state.total_intake} ml today!</div>", unsafe_allow_html=True)
    if st.button("Back"):
        st.session_state.step = "dashboard"
        st.rerun()
