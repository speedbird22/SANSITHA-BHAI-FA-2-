# app.py
import streamlit as st

# ====================== CONFIG ======================
st.set_page_config(page_title="WaterBuddy", page_icon="💧", layout="wide")

# ====================== CSS: CREAM WHITE + DARK TEXT + FULL SCREEN ======================
st.markdown("""
<style>
    .stApp {background-color: #FFF8E7 !important; color: #1A1A1A !important;}
    .big-title {font-size: 46px; font-weight: bold; text-align: center; color: #1E90FF; font-family: 'Comic Sans MS', cursive; margin: 20px 0;}
    .age-btn {width: 100%; height: 120px; font-size: 22px; font-weight: bold; border-radius: 18px; margin: 15px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);}
    .slider-label {font-size: 20px; font-weight: bold; color: #2E8B57; text-align: center;}
    .mascot {font-size: 100px; text-align: center; margin: 25px 0;}
    .progress-box {background: #E0F7FA; padding: 18px; border-radius: 15px; text-align: center; font-size: 22px; font-weight: bold; color: #1A1A1A;}
    .water-btn {background: linear-gradient(45deg, #4FC3F7, #29B6F6); color: white; font-weight: bold; border-radius: 15px; padding: 18px; font-size: 18px; height: 90px;}
    .water-btn:hover {background: #0288D1; transform: scale(1.03);}
    .summary-box {background: #E8F5E9; padding: 20px; border-radius: 15px; font-size: 19px; color: #1A1A1A;}
    .fade-in {animation: fadeIn 1.2s ease-in;}
    .fade-out {animation: fadeOut 0.8s ease-out forwards;}
    @keyframes fadeIn {from {opacity: 0; transform: translateY(20px);} to {opacity: 1; transform: translateY(0);}}
    @keyframes fadeOut {from {opacity: 1;} to {opacity: 0; transform: translateY(-20px);}}
    .stButton > button {width: 100%; margin: 10px 0;}
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
    "4–8 years": {"ml": 1200, "cups": 5, "color": "#FF9999"},
    "9–13 years": {"ml": 1700, "cups": 7, "color": "#66B2FF"},
    "14–64 years": {"ml": 2250, "cups": 9, "color": "#99FF99"},
    "65+ years": {"ml": 1850, "cups": 7, "color": "#FFCC99"}
}

# ====================== STEP 1: AGE SELECTION ======================
if st.session_state.step == "age_selection":
    st.markdown("<h1 class='big-title'>WaterBuddy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:22px; color:#1A1A1A;'>Choose your age group to get started!</p>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    for idx, (age, data) in enumerate(age_data.items()):
        with cols[idx]:
            if st.button(
                f"**{age}**\n💧 ~{data['cups']} cups/day",
                key=age,
                help=f"Recommended: {data['ml']} ml",
                use_container_width=True
            ):
                st.session_state.age_group = age
                st.session_state.goal = data['ml']
                st.session_state.step = "goal_slider"
                st.rerun()
        # NO COLOR LINES — REMOVED

# ====================== STEP 2: GOAL SLIDER ======================
elif st.session_state.step == "goal_slider":
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    st.markdown("<h2 class='big-title'>Set Your Daily Goal</h2>", unsafe_allow_html=True)
    
    min_ml = 500
    max_ml = 4000
    suggested = age_data[st.session_state.age_group]["ml"]
    
    goal = st.slider(
        "Choose your daily water intake goal",
        min_value=min_ml,
        max_value=max_ml,
        value=suggested,
        step=100,
        format="%d ml"
    )
    st.session_state.goal = goal
    
    # Zone feedback
    if goal < suggested * 0.7:
        zone = "Too Low"
        tip = "Try to drink at least 70% of recommended!"
    elif goal < suggested:
        zone = "A Bit Low"
        tip = "You're close! A little more would be ideal."
    elif goal <= suggested * 1.3:
        zone = "Perfect Zone"
        tip = "Great choice! This is healthy and achievable."
    else:
        zone = "Ambitious!"
        tip = "Awesome! Challenge accepted!"
    
    st.markdown(f"<p class='slider-label'>{zone}</p>", unsafe_allow_html=True)
    st.info(f"{tip}")
    
    if st.button("Continue", use_container_width=True):
        st.session_state.step = "name_input"
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ====================== STEP 3: NAME INPUT ======================
elif st.session_state.step == "name_input":
    st.markdown("<h2 class='big-title'>What should we call you?</h2>", unsafe_allow_html=True)
    name = st.text_input("", placeholder="Enter your name...", label_visibility="collapsed")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Let's Go!", disabled=not name.strip()):
            st.session_state.username = name.strip().capitalize()
            st.session_state.step = "dashboard"
            st.rerun()

# ====================== STEP 4: DASHBOARD ======================
elif st.session_state.step == "dashboard":
    st.markdown(f"<h1 class='big-title'>Hey {st.session_state.username}!</h1>", unsafe_allow_html=True)
    
    total = st.session_state.total_intake
    goal = st.session_state.goal
    progress = min(100, (total / goal) * 100) if goal > 0 else 0
    remaining = max(0, goal - total)
    
    st.markdown(f"""
    <div class='progress-box'>
        {int(total)} ml / {goal} ml → <strong>{int(remaining)} ml</strong> left
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress / 100)
    
    # Mascot
    if progress >= 100:
        mascot = "🎉"
        msg = "GOAL ACHIEVED! You're a hydration superstar!"
    elif progress >= 75:
        mascot = ""
        msg = "Amazing! Almost there!"
    elif progress >= 50:
        mascot = ""
        msg = "Great job! Over halfway!"
    elif progress > 0:
        mascot = ""
        msg = "Every sip counts! Keep going!"
    else:
        mascot = ""
        msg = "Time to drink up! Your body needs it!"
    
    st.markdown(f"<div class='mascot'>{mascot}</div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:22px; color:#2E8B57;'><strong>{msg}</strong></p>", unsafe_allow_html=True)
    
    # Water buttons
    st.markdown("### Add Water")
    cols = st.columns(4)
    amounts = [
        ("Glass", 250),
        ("Small Bottle", 500),
        ("Medium Bottle", 1000),
        ("Large Bottle", 1500)
    ]
    for col, (label, ml) in zip(cols, amounts):
        with col:
            if st.button(f"{label}\n{ml} ml", key=label, use_container_width=True):
                st.session_state.total_intake += ml
                st.success(f"+{ml} ml added!")
                st.rerun()
    
    # Custom
    custom = st.number_input("Custom amount (ml)", min_value=0, value=0, step=50)
    if st.button("Add Custom", use_container_width=True):
        st.session_state.total_intake += custom
        st.success(f"+{custom} ml added!")
        st.rerun()
    
    # Reset + Summary
    col1, col2 = st.columns(2)
    with col1:
        if st.button("New Day", use_container_width=True):
            st.session_state.total_intake = 0
            st.success("New day started!")
            st.rerun()
    with col2:
        if st.button("View Full Summary", use_container_width=True):
            st.session_state.step = "summary"
            st.rerun()

# ====================== STEP 5: SUMMARY ======================
elif st.session_state.step == "summary":
    st.markdown(f"<h1 class='big-title'>Summary for {st.session_state.username}</h1>", unsafe_allow_html=True)
    
    total = st.session_state.total_intake
    goal = st.session_state.goal
    progress = (total / goal) * 100 if goal > 0 else 0
    
    if progress >= 100:
        title = "GOAL ACHIEVED!"
        text = f"Amazing job, {st.session_state.username}! You drank {total} ml — that's {progress:.0f}% of your goal! You're properly hydrated and full of energy! Keep this up every day!"
    elif progress >= 75:
        title = "Great Effort!"
        text = f"Well done! You reached {progress:.0f}% of your {goal} ml goal. Just a little more next time!"
    elif progress >= 50:
        title = "Good Start!"
        text = f"You're halfway there with {total} ml! Try to finish strong tomorrow."
    else:
        title = "Let's Try Harder"
        text = f"You drank {total} ml today. Tomorrow, aim for at least {goal} ml to stay healthy and focused!"
    
    st.markdown(f"<div class='summary-box'><strong>{title}</strong><br><br>{text}</div>", unsafe_allow_html=True)
    
    if st.button("Back to Dashboard"):
        st.session_state.step = "dashboard"
        st.rerun()
