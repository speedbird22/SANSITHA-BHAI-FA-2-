# app.py
import streamlit as st
import time
import random

# ====================== CONFIG ======================
st.set_page_config(page_title="WaterBuddy", page_icon="💧", layout="centered")

# Custom CSS for FUN & COLORFUL UI
st.markdown("""
<style>
    .big-font {font-size: 50px !important; font-weight: bold; color: #1E90FF;}
    .water-drop {font-size: 40px; animation: splash 1.5s infinite;}
    @keyframes splash {0%,100%{transform:scale(1)} 50%{transform:scale(1.3)}}
    .bottle {font-size: 80px; text-align: center;}
    .progress-container {background: #E3F2FD; padding: 10px; border-radius: 15px; border: 3px solid #2196F3;}
    .tip-box {background: linear-gradient(45deg, #FF9800, #FFC107); padding: 15px; border-radius: 15px; color: white; font-weight: bold;}
    .mascot {font-size: 70px; text-align: center; transition: all 0.3s;}
    .goal-box {background: #E8F5E9; padding: 15px; border-radius: 12px; border-left: 6px solid #4CAF50;}
    .header {text-align: center; font-family: 'Comic Sans MS', cursive, sans-serif;}
    .stButton>button {background: #FF5722; color: white; font-weight: bold; border-radius: 12px; padding: 10px 20px;}
    .stButton>button:hover {background: #F44336; transform: scale(1.05);}
</style>
""", unsafe_allow_html=True)

# ====================== STATE ======================
if 'total_intake' not in st.session_state:
    st.session_state.total_intake = 0
if 'goal' not in st.session_state:
    st.session_state.goal = 2250
if 'age_group' not in st.session_state:
    st.session_state.age_group = "14–64 years"
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# ====================== DATA ======================
age_groups = {
    "4–8 years": 1200,
    "9–13 years": 1700,
    "14–64 years": 2250,
    "65+ years": 1850
}

tips = [
    "💦 Sip before every meal!",
    "🌟 Keep your bottle on your desk!",
    "⏰ Set a reminder every 2 hours!",
    "🍋 Add lemon or mint for flavor!",
    "🏃 Drink after exercise!",
    "😴 Hydrate before bed too!"
]

mascot_reactions = {
    0: "😴", 50: "😊", 75: "😄", 100: "🥳🎉"
}

# ====================== DARK MODE ======================
dark = st.sidebar.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
if dark:
    st.markdown("<style>body{background:#121212;color:#eee;} .stApp{background:#121212;}</style>", unsafe_allow_html=True)
    st.session_state.dark_mode = True
else:
    st.markdown("<style>body{background:#E3F2FD;}</style>", unsafe_allow_html=True)
    st.session_state.dark_mode = False

# ====================== HEADER ======================
st.markdown("<h1 class='header'>💧 WaterBuddy</h1>", unsafe_allow_html=True)
st.markdown("<p class='header' style='font-size:20px; color:#555;'>Your Fun Hydration Friend!</p>", unsafe_allow_html=True)

# ====================== AGE & GOAL ======================
col1, col2 = st.columns([1, 1])
with col1:
    st.selectbox("🎂 Your Age Group", options=list(age_groups.keys()), key="age_group")
with col2:
    suggested = age_groups[st.session_state.age_group]
    st.number_input("🎯 Daily Goal (ml)", min_value=500, value=suggested, step=100, key="goal")

# Show standard vs goal
standard = age_groups[st.session_state.age_group]
st.markdown(f"""
<div class="goal-box">
<strong>Standard Goal:</strong> {standard} ml<br>
<strong>Your Goal:</strong> {st.session_state.goal} ml
</div>
""", unsafe_allow_html=True)

# ====================== LOG WATER ======================
st.markdown("### 💦 Log Your Water")
col_log1, col_log2 = st.columns([1, 1])
with col_log1:
    if st.button("🚰 +250 ml", use_container_width=True):
        st.session_state.total_intake += 250
        st.success("✅ +250 ml logged!")
with col_log2:
    custom = st.number_input("Or enter amount (ml)", min_value=0, value=0, step=50, key="custom_log")
    if st.button("➕ Log Custom", use_container_width=True):
        st.session_state.total_intake += custom
        st.success(f"✅ +{custom} ml logged!")

# Reset Button
if st.button("🔄 New Day – Reset Progress", use_container_width=True):
    st.session_state.total_intake = 0
    st.success("🌅 New day started! Fresh goals!")

# ====================== CALCULATIONS ======================
total = st.session_state.total_intake
goal = st.session_state.goal
remaining = max(0, goal - total)
progress = min(100, (total / goal) * 100) if goal > 0 else 0
cups = total / 250

# ====================== ANIMATED BOTTLE ======================
st.markdown("<div class='progress-container'>", unsafe_allow_html=True)
st.markdown(f"<div class='bottle'>{'🍼' if progress < 50 else '🥛' if progress < 100 else '🏆'}</div>", unsafe_allow_html=True)

# Progress bar with water fill effect
st.progress(progress / 100)
st.markdown(f"""
<p style='text-align:center; font-size:18px;'>
<strong>{int(total)} ml</strong> / {goal} ml → <strong>{int(remaining)} ml</strong> left<br>
≈ <strong>{cups:.1f} cups</strong> 🍵
</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ====================== MASCOT & MESSAGE ======================
mascot = "😴"
message = "Start drinking! 💧"

if progress >= 100:
    mascot = "🥳🎉"
    message = "GOAL SMASHED! You're a hydration hero! 🎉"
    st.balloons()
elif progress >= 75:
    mascot = "😄"
    message = "Almost there! Keep going! 🚀"
elif progress >= 50:
    mascot = "😊"
    message = "Great job! Over halfway! 🌟"
elif progress > 0:
    mascot = "😉"
    message = "Nice start! Every drop counts! 💧"

st.markdown(f"<div class='mascot'>{mascot}</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:22px; font-weight:bold; color:#1E90FF;'>{message}</p>", unsafe_allow_html=True)

# ====================== DAILY TIP ======================
tip = random.choice(tips)
st.markdown(f"<div class='tip-box'>💡 <strong>Pro Tip:</strong> {tip}</div>", unsafe_allow_html=True)

# ====================== SIDEBAR STATS ======================
with st.sidebar:
    st.header("📊 Your Stats")
    st.metric("Total Intake", f"{total} ml")
    st.metric("Goal", f"{goal} ml")
    st.metric("Progress", f"{progress:.1f}%")
    st.metric("Cups", f"{cups:.1f}")
    
    st.markdown("---")
    st.markdown("### 🎨 Fun Mode")
    if st.button("🎊 Surprise!"):
        st.toast("You're awesome! Keep hydrating! 🌊", icon="🎉")

# ====================== FOOTER ======================
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888; font-size:14px;'>Made with ❤️ using Streamlit | Stay Hydrated!</p>", unsafe_allow_html=True)
