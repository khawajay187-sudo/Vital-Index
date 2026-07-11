import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="VitalIndex | Obesity Risk Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, .hero-title {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #F0FDF9 0%, #E8F9F5 100%);
}

.hero-banner {
    background: linear-gradient(135deg, #0F766E 0%, #14B8A6 50%, #2DD4BF 100%);
    padding: 48px 40px;
    border-radius: 24px;
    color: white;
    margin-bottom: 32px;
    box-shadow: 0 20px 40px rgba(15, 118, 110, 0.25);
}
.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
}
.hero-subtitle {
    font-size: 18px;
    font-weight: 400;
    opacity: 0.92;
}

/* ===== GRID LAYOUT (DO NOT CHANGE - working perfectly) ===== */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 32px;
}
.step-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
@media (max-width: 900px) {
    .stat-grid { grid-template-columns: repeat(2, 1fr); }
    .step-grid { grid-template-columns: 1fr; }
}

.material-card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    border: 1px solid rgba(15, 118, 110, 0.08);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.material-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(15, 118, 110, 0.18);
}
.stat-number {
    font-size: 34px;
    font-weight: 800;
    color: #0F766E;
    font-family: 'Poppins', sans-serif;
}
.stat-label {
    font-size: 14px;
    color: #64748B;
    font-weight: 500;
}

.step-card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(15, 118, 110, 0.08);
    height: 100%;
    display: flex;
    flex-direction: column;
}
.step-card h4 { margin: 8px 0; }
.step-card p { color: #64748B; flex-grow: 1; margin: 0; }

/* Risk badges */
.badge-healthy { background: #DCFCE7; color: #166534; padding: 6px 16px; border-radius: 999px; font-weight: 600; display: inline-block; }
.badge-warning { background: #FEF3C7; color: #92400E; padding: 6px 16px; border-radius: 999px; font-weight: 600; display: inline-block; }
.badge-danger { background: #FEE2E2; color: #991B1B; padding: 6px 16px; border-radius: 999px; font-weight: 600; display: inline-block; }

/* Tip cards */
.tip-card {
    background: white;
    border-left: 5px solid #0F766E;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* ===== SIDEBAR BASE ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F766E 0%, #0B5C55 100%);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebarUserContent"] {
    padding-top: 8px !important;
}

/* ===== Sidebar Header - Logo Card ===== */
.sidebar-header-card {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 16px;
    padding: 14px 16px;
    margin: 4px 4px 20px 4px;
    transition: all 0.25s ease;
}
.sidebar-header-card:hover {
    background: rgba(255, 255, 255, 0.14);
    transform: translateY(-2px);
}
.sidebar-logo-badge {
    background: linear-gradient(135deg, #2DD4BF, #0F766E);
    width: 44px;
    height: 44px;
    min-width: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 12px rgba(45, 212, 191, 0.4);
    animation: pulse-glow 3s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 4px 12px rgba(45, 212, 191, 0.4); }
    50% { box-shadow: 0 4px 20px rgba(45, 212, 191, 0.7); }
}
.sidebar-header-text {
    display: flex;
    flex-direction: column;
    line-height: 1.2;
}
.sidebar-header-title {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.3px;
}
.sidebar-header-subtitle {
    font-size: 11px;
    opacity: 0.75;
    font-weight: 500;
    margin-top: 2px;
}
/* ===== NAV -> built with st.button (stable, no fragile DOM hacking) ===== */
[data-testid="stSidebar"] .stButton {
    margin: 0 !important;
    padding: 0 4px !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    box-sizing: border-box !important;
    display: flex !important;
    justify-content: flex-start !important;
    align-items: center !important;
    text-align: left !important;
    border-radius: 999px !important;
    padding: 12px 18px !important;
    margin: 0 !important;
    font-weight: 600 !important;
    font-size: 14.5px !important;
    box-shadow: none !important;
    transform: none !important;
    transition: background 0.2s ease !important;
}

/* inactive nav item */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: transparent !important;
    color: rgba(255,255,255,0.9) !important;
    border: none !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.10) !important;
    color: white !important;
}

/* active nav item = white capsule, teal text */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: #FFFFFF !important;
    color: #0F766E !important;
    border: none !important;
}
/* the universal white-text rule above wins over the button's own color for its
   inner text node, so force teal explicitly on every descendant of the active button */
[data-testid="stSidebar"] .stButton > button[kind="primary"] * {
    color: #0F766E !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: #F8FAFC !important;
    color: #0F766E !important;
}

/* thin divider line between nav items */
.nav-divider {
    border-bottom: 1px solid rgba(255,255,255,0.14);
    margin: 6px 20px;
}

/* ===== Global teal accent for form widgets (radio dot, slider thumb, etc) ===== */
:root {
    --primary-color: #0F766E;
}

/* ===== Predict wizard ===== */
.progress-step-label {
    font-size: 13px;
    color: #64748B;
    font-weight: 600;
    margin-bottom: 8px;
}
.progress-track {
    background: rgba(15, 118, 110, 0.12);
    border-radius: 999px;
    height: 8px;
    width: 100%;
    overflow: hidden;
    margin-bottom: 28px;
}
.progress-fill {
    background: linear-gradient(135deg, #0F766E, #14B8A6);
    height: 100%;
    border-radius: 999px;
    transition: width 0.3s ease;
}
.question-card {
    background: white;
    border-radius: 20px;
    padding: 40px 44px;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(15, 118, 110, 0.08);
    margin-bottom: 22px;
}
.question-text {
    font-family: 'Poppins', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 22px;
}
.result-hero {
    background: linear-gradient(135deg, #0F766E 0%, #14B8A6 50%, #2DD4BF 100%);
    border-radius: 24px;
    padding: 40px;
    color: white;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 20px 40px rgba(15, 118, 110, 0.25);
}
.result-category {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 800;
    margin: 10px 0 6px 0;
}
.result-confidence {
    font-size: 15px;
    opacity: 0.9;
}

/* Habit tracker */
.habit-progress-wrap {
    background: white;
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(15, 118, 110, 0.08);
    margin-bottom: 18px;
}

/* Small info pill used inside tabs / calculators */
.info-pill {
    display: inline-block;
    background: rgba(15, 118, 110, 0.08);
    color: #0F766E;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}

.calc-result-box {
    background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%);
    border-radius: 16px;
    padding: 24px;
    color: white;
    text-align: center;
}
.calc-result-box .num {
    font-family: 'Poppins', sans-serif;
    font-size: 32px;
    font-weight: 800;
}
.calc-result-box .lbl {
    font-size: 13px;
    opacity: 0.9;
}

/* Regular action buttons in main content (e.g. Predict button) - NOT sidebar nav */
[data-testid="stAppViewContainer"] .main .stButton > button {
    background: linear-gradient(135deg, #0F766E, #14B8A6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    box-shadow: 0 6px 16px rgba(15, 118, 110, 0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stAppViewContainer"] .main .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px rgba(15, 118, 110, 0.4) !important;
}
            
.stSlider > div {
    padding: 16px 0;
}
.stRadio > div {
    gap: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL ARTIFACTS
# -----------------------------
@st.cache_resource
def load_artifacts():
    model = joblib.load(r'C:\AC Office Chakwal\Python\obesitychecker project\dataset\obesity_rf_model.pkl')
    scaler = joblib.load(r'C:\AC Office Chakwal\Python\obesitychecker project\dataset\scaler.pkl')
    mappings = joblib.load(r'C:\AC Office Chakwal\Python\obesitychecker project\dataset\encoding_mappings.pkl')
    return model, scaler, mappings

model, scaler, mappings = load_artifacts()

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
NAV_ITEMS = ["Dashboard", "Predict My Risk", "Health Info", "Weight Loss Tips", "About"]

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

with st.sidebar:
    st.markdown("""
<div class="sidebar-header-card">
    <div class="sidebar-logo-badge">🩺</div>
    <div class="sidebar-header-text">
        <div class="sidebar-header-title">VitalIndex</div>
        <div class="sidebar-header-subtitle">AI Health Dashboard</div>
    </div>
</div>
""", unsafe_allow_html=True)

    for i, name in enumerate(NAV_ITEMS):
        is_active = st.session_state.page == name
        if st.button(
            name,
            key=f"nav_{name}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state.page = name
            st.rerun()
        if i < len(NAV_ITEMS) - 1:
            st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

page = st.session_state.page

# -----------------------------
# PAGE: DASHBOARD (HOME)
# -----------------------------
if page == "Dashboard":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Know Your Body. Own Your Health.</div>
        <div class="hero-subtitle">AI-powered obesity risk assessment based on your lifestyle, diet, and habits — get personalized insights in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-grid">
        <div class="material-card">
            <div class="stat-number">1B+</div>
            <div class="stat-label">People living with obesity worldwide</div>
        </div>
        <div class="material-card">
            <div class="stat-number">43%</div>
            <div class="stat-label">Of adults globally are overweight</div>
        </div>
        <div class="material-card">
            <div class="stat-number">99.5%</div>
            <div class="stat-label">Our model's prediction accuracy</div>
        </div>
        <div class="material-card">
            <div class="stat-number">7</div>
            <div class="stat-label">Obesity categories analyzed</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### How It Works")
    st.markdown("""
    <div class="step-grid">
        <div class="step-card">
            <div style="font-size: 36px;">📋</div>
            <h4>1. Enter Your Details</h4>
            <p>Age, height, weight, eating habits, and activity level.</p>
        </div>
        <div class="step-card">
            <div style="font-size: 36px;">🤖</div>
            <h4>2. AI Analyzes Patterns</h4>
            <p>Our Random Forest model compares you against thousands of data points.</p>
        </div>
        <div class="step-card">
            <div style="font-size: 36px;">📈</div>
            <h4>3. Get Your Result</h4>
            <p>Receive your obesity category with a visual BMI compass and personalized tips.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# PAGE: PREDICT MY RISK (step-by-step wizard)
# -----------------------------
elif page == "Predict My Risk":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">Predict Your Obesity Risk</div>
        <div class="hero-subtitle">Answer a few quick questions about your lifestyle, and our AI will assess your obesity risk category.</div>
    </div>
    """, unsafe_allow_html=True)

    # Session state for form steps
    if 'predict_step' not in st.session_state:
        st.session_state.predict_step = 1
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
          'Age': 25, 'Height': 1.70, 'Weight': 70,
          'Gender': 'Male', 'FAVC': 'no', 'FCVC': 2.0, 'NCP': 3.0,
          'SMOKE': 'no', 'CH2O': 2.0, 'SCC': 'no',
          'family_history_with_overweight': 'no', 'FAF': 1.0, 'TUE': 1.0,
          'CALC': 'no', 'CAEC': 'Sometimes', 'MTRANS': 'Public_Transportation'
        }

    total_steps = 5
    progress = st.session_state.predict_step / total_steps

    # Progress bar with step indicator
    st.markdown(f"""
    <div style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #0F766E;">Step {st.session_state.predict_step} of {total_steps}</span>
            <span style="font-weight: 600; color: #64748B;">{int(progress * 100)}% Complete</span>
        </div>
        <div style="background: #E0F2F1; border-radius: 999px; height: 8px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, #0F766E, #14B8A6); height: 100%; width: {progress * 100}%; border-radius: 999px; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ===== STEP 1: Basic Info (Age, Gender, Height, Weight) =====
    if st.session_state.predict_step == 1:
        st.markdown("""
        <div class="material-card" style="padding: 32px; margin-bottom: 24px;">
            <h3 style="color: #0F766E; margin-bottom: 24px; font-family: Poppins;">📋 Basic Information</h3>
            <p style="color: #64748B; margin-bottom: 20px;">Let's start with your basic details.</p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            age = st.slider("Age (years)", 14, 80, st.session_state.form_data['Age'],
                           help="Your current age in years")
            st.session_state.form_data['Age'] = age

        with col2:
            gender = st.radio("Gender", ["Male", "Female"], 
                            index=0 if st.session_state.form_data['Gender'] == 'Male' else 1,
                            horizontal=True)
            st.session_state.form_data['Gender'] = gender

        col3, col4 = st.columns(2)
        with col3:
            height = st.slider("Height (meters)", 1.4, 2.1, st.session_state.form_data['Height'], 0.01,
                             help="Your height in meters (e.g., 1.70)")
            st.session_state.form_data['Height'] = height

        with col4:
            weight = st.slider("Weight (kg)", 30, 200, st.session_state.form_data['Weight'],
                             help="Your weight in kilograms")
            st.session_state.form_data['Weight'] = weight

        # Live BMI calculation
        bmi = weight / (height ** 2)
        bmi_color = "#22C55E" if bmi < 25 else ("#FFA500" if bmi < 30 else "#EF4444")
        st.markdown(f"""
        <div style="background: {bmi_color}15; border-left: 4px solid {bmi_color}; border-radius: 8px; padding: 16px; margin-top: 20px;">
            <strong style="color: {bmi_color}; font-size: 18px;">Your BMI: {bmi:.1f}</strong>
            <p style="color: #64748B; margin: 8px 0 0 0; font-size: 14px;">
                {'Healthy weight' if bmi < 25 else ('Overweight' if bmi < 30 else 'Obese')}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 2: Eating Habits =====
    elif st.session_state.predict_step == 2:
        st.markdown("""
        <div class="material-card" style="padding: 32px; margin-bottom: 24px;">
            <h3 style="color: #0F766E; margin-bottom: 24px; font-family: Poppins;">🍽️ Eating Habits</h3>
            <p style="color: #64748B; margin-bottom: 20px;">Tell us about your daily eating patterns.</p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            favc = st.radio("Do you eat frequent high caloric food?", ["yes", "no"],
                          index=0 if st.session_state.form_data['FAVC'] == 'yes' else 1)
            st.session_state.form_data['FAVC'] = favc

        with col2:
            fcvc_options = {"Never": 1.0, "Sometimes": 2.0, "Frequently": 3.0, "Always": 4.0}
            fcvc_labels = list(fcvc_options.keys())
            current_fcvc_label = fcvc_labels[int(st.session_state.form_data['FCVC']) - 1]
            fcvc_choice = st.radio("Frequency of vegetable consumption", fcvc_labels,
                                  index=fcvc_labels.index(current_fcvc_label))
            st.session_state.form_data['FCVC'] = fcvc_options[fcvc_choice]

        col3, col4 = st.columns(2)
        with col3:
            ncp_options = {"1 meal": 1.0, "2 meals": 2.0, "3 meals": 3.0, "4+ meals": 4.0}
            ncp_labels = list(ncp_options.keys())
            current_ncp_label = ncp_labels[int(st.session_state.form_data['NCP']) - 1]
            ncp_choice = st.radio("Number of meals per day", ncp_labels,
                                index=ncp_labels.index(current_ncp_label))
            st.session_state.form_data['NCP'] = ncp_options[ncp_choice]

        with col4:
            scc = st.radio("Do you eat snacks between meals?", ["yes", "no"],
                         index=0 if st.session_state.form_data['SCC'] == 'yes' else 1)
            st.session_state.form_data['SCC'] = scc

        caec = st.radio("What do you eat when bored?", ["no", "Sometimes", "Frequently", "Always"],
                       index=["no", "Sometimes", "Frequently", "Always"].index(st.session_state.form_data['CAEC']))
        st.session_state.form_data['CAEC'] = caec

        calc = st.radio("Do you drink alcohol?", ["no", "Sometimes", "Frequently", "Always"],
                       index=["no", "Sometimes", "Frequently", "Always"].index(st.session_state.form_data['CALC']))
        st.session_state.form_data['CALC'] = calc

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 3: Hydration & Lifestyle =====
    elif st.session_state.predict_step == 3:
        st.markdown("""
        <div class="material-card" style="padding: 32px; margin-bottom: 24px;">
            <h3 style="color: #0F766E; margin-bottom: 24px; font-family: Poppins;">💧 Hydration & Lifestyle</h3>
            <p style="color: #64748B; margin-bottom: 20px;">How healthy is your daily routine?</p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ch2o = st.slider("Daily water intake (liters)", 1.0, 4.0,
                           st.session_state.form_data['CH2O'], 0.1,
                           help="How many liters of water per day")
            st.session_state.form_data['CH2O'] = ch2o

        with col2:
            faf = st.slider("Frequency of physical activity (hrs/week)", 0.0, 3.0,
                          st.session_state.form_data['FAF'], 0.1,
                          help="Hours of exercise per week")
            st.session_state.form_data['FAF'] = faf

        col3, col4 = st.columns(2)
        with col3:
            smoke = st.radio("Do you smoke?", ["yes", "no"],
                           index=0 if st.session_state.form_data['SMOKE'] == 'yes' else 1)
            st.session_state.form_data['SMOKE'] = smoke

        with col4:
            tue = st.slider("Time using technology (hrs/day)", 0.0, 2.0,
                          st.session_state.form_data['TUE'], 0.1)
            st.session_state.form_data['TUE'] = tue

        family_history = st.radio("Family history of overweight?", ["yes", "no"],
                                 index=0 if st.session_state.form_data['family_history_with_overweight'] == 'yes' else 1)
        st.session_state.form_data['family_history_with_overweight'] = family_history

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 4: Transportation =====
    elif st.session_state.predict_step == 4:
        st.markdown("""
        <div class="material-card" style="padding: 32px; margin-bottom: 24px;">
            <h3 style="color: #0F766E; margin-bottom: 24px; font-family: Poppins;">🚗 Transportation & Summary</h3>
            <p style="color: #64748B; margin-bottom: 20px;">How do you usually get around?</p>
        """, unsafe_allow_html=True)

        mtrans = st.radio("Primary transportation mode",
                         ["Walking", "Bike", "Motorbike", "Public_Transportation", "Automobile"],
                         index=["Walking", "Bike", "Motorbike", "Public_Transportation", "Automobile"].index(st.session_state.form_data['MTRANS']))
        st.session_state.form_data['MTRANS'] = mtrans

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: #E0F2F1; border-radius: 14px; padding: 20px; border-left: 4px solid #0F766E;">
            <h4 style="color: #0F766E; margin-top: 0;">📊 Your Summary</h4>
            <ul style="color: #475569; line-height: 1.8;">
                <li><strong>Age:</strong> {} years</li>
                <li><strong>Height:</strong> {} m | <strong>Weight:</strong> {} kg</li>
                <li><strong>Water intake:</strong> {} L/day</li>
                <li><strong>Physical activity:</strong> {} hrs/week</li>
                <li><strong>Transport mode:</strong> {}</li>
            </ul>
        </div>
        """.format(
            st.session_state.form_data['Age'],
            st.session_state.form_data['Height'],
            st.session_state.form_data['Weight'],
            st.session_state.form_data['CH2O'],
            st.session_state.form_data['FAF'],
            st.session_state.form_data['MTRANS']
        ), unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ===== STEP 5: Review & Predict =====
    elif st.session_state.predict_step == 5:
        st.markdown("""
        <div class="material-card" style="padding: 32px; margin-bottom: 24px;">
            <h3 style="color: #0F766E; margin-bottom: 24px; font-family: Poppins;">✅ Ready to Predict?</h3>
            <p style="color: #64748B; margin-bottom: 20px;">Review your information and get your obesity risk assessment.</p>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px;">
            <div style="background: #F0FDF9; border-radius: 12px; padding: 16px; border-left: 4px solid #0F766E;">
                <div style="font-size: 12px; opacity: 0.7; color: #64748B;">AGE & GENDER</div>
                <div style="font-size: 18px; font-weight: 700; color: #0F766E;">{st.session_state.form_data['Age']} yrs, {st.session_state.form_data['Gender']}</div>
            </div>
            <div style="background: #F0FDF9; border-radius: 12px; padding: 16px; border-left: 4px solid #0F766E;">
                <div style="font-size: 12px; opacity: 0.7; color: #64748B;">BMI</div>
                <div style="font-size: 18px; font-weight: 700; color: #0F766E;">{st.session_state.form_data['Weight'] / (st.session_state.form_data['Height'] ** 2):.1f}</div>
            </div>
            <div style="background: #F0FDF9; border-radius: 12px; padding: 16px; border-left: 4px solid #0F766E;">
                <div style="font-size: 12px; opacity: 0.7; color: #64748B;">WATER INTAKE</div>
                <div style="font-size: 18px; font-weight: 700; color: #0F766E;">{st.session_state.form_data['CH2O']:.1f} L/day</div>
            </div>
            <div style="background: #F0FDF9; border-radius: 12px; padding: 16px; border-left: 4px solid #0F766E;">
                <div style="font-size: 12px; opacity: 0.7; color: #64748B;">ACTIVITY LEVEL</div>
                <div style="font-size: 18px; font-weight: 700; color: #0F766E;">{st.session_state.form_data['FAF']:.1f} hrs/wk</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🚀 Get My Prediction", use_container_width=True, key="predict_btn"):
            st.session_state.predict_step = 6
            st.rerun()

    # ===== STEP 6: Results =====
    elif st.session_state.predict_step == 6:
        # Prepare data for model prediction
        data_dict = {
            'Age': [st.session_state.form_data['Age']],
            'Height': [st.session_state.form_data['Height']],
            'Weight': [st.session_state.form_data['Weight']],
            'FCVC': [st.session_state.form_data['FCVC']],
            'NCP': [st.session_state.form_data['NCP']],
            'CH2O': [st.session_state.form_data['CH2O']],
            'FAF': [st.session_state.form_data['FAF']],
            'TUE': [st.session_state.form_data['TUE']],
            'Gender': [1 if st.session_state.form_data['Gender'] == 'Male' else 0],
            'FAVC': [1 if st.session_state.form_data['FAVC'] == 'yes' else 0],
            'SCC': [1 if st.session_state.form_data['SCC'] == 'yes' else 0],
            'SMOKE': [1 if st.session_state.form_data['SMOKE'] == 'yes' else 0],
            'family_history_with_overweight': [1 if st.session_state.form_data['family_history_with_overweight'] == 'yes' else 0],
            'CALC': [['no', 'Sometimes', 'Frequently', 'Always'].index(st.session_state.form_data['CALC'])],
            'CAEC': [['no', 'Sometimes', 'Frequently', 'Always'].index(st.session_state.form_data['CAEC'])],
            'MTRANS_Walking': [1 if st.session_state.form_data['MTRANS'] == 'Walking' else 0],
            'MTRANS_Bike': [1 if st.session_state.form_data['MTRANS'] == 'Bike' else 0],
            'MTRANS_Motorbike': [1 if st.session_state.form_data['MTRANS'] == 'Motorbike' else 0],
            'MTRANS_Public_Transportation': [1 if st.session_state.form_data['MTRANS'] == 'Public_Transportation' else 0],
            'MTRANS_Automobile': [1 if st.session_state.form_data['MTRANS'] == 'Automobile' else 0],
        }

        # Add BMI
        bmi = st.session_state.form_data['Weight'] / (st.session_state.form_data['Height'] ** 2)
        data_dict['BMI'] = [bmi]

        df_input = pd.DataFrame(data_dict)

        # Scale the numerical features
        scaled_cols = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE', 'BMI']
        df_input[scaled_cols] = scaler.transform(df_input[scaled_cols])

        # Reorder columns to match training
        feature_order = mappings['feature_columns']
        df_input = df_input[feature_order]

        # Predict
        prediction = model.predict(df_input)[0]
        prob = model.predict_proba(df_input)[0]

        # Get class name
        class_names = {0: 'Insufficient_Weight', 1: 'Normal_Weight', 2: 'Overweight_Level_I',
                      3: 'Overweight_Level_II', 4: 'Obesity_Type_I', 5: 'Obesity_Type_II', 6: 'Obesity_Type_III'}
        predicted_class = class_names[prediction]

        # Color coding
        colors = ['#22C55E', '#10B981', '#F59E0B', '#FB923C', '#EF4444', '#DC2626', '#991B1B']
        color = colors[prediction]

        st.markdown(f"""
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 48px; margin-bottom: 16px;">✨</div>
            <h1 style="color: #0F766E; font-size: 36px; margin-bottom: 8px;">Your Prediction</h1>
            <div style="background: {color}20; border: 2px solid {color}; border-radius: 20px; padding: 30px; margin: 20px 0;">
                <div style="font-size: 14px; opacity: 0.75; color: {color}; font-weight: 600; margin-bottom: 8px;">OBESITY CATEGORY</div>
                <div style="font-size: 42px; font-weight: 800; color: {color};">{predicted_class.replace('_', ' ')}</div>
                <div style="font-size: 16px; color: #64748B; margin-top: 12px;">
                    Confidence: <strong>{max(prob)*100:.1f}%</strong>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Probability gauge
        st.markdown("### Prediction Confidence")
        cols = st.columns(7)
        for i, (col, prob_val) in enumerate(zip(cols, prob)):
            with col:
                st.metric(class_names[i].split('_')[0], f"{prob_val*100:.0f}%")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Form", use_container_width=True):
                st.session_state.predict_step = 1
                st.rerun()

        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.predict_step = 1
                st.rerun()

    # ===== Navigation Buttons =====
    st.markdown("<br>", unsafe_allow_html=True)
    col_prev, col_next = st.columns([1, 1])

    with col_prev:
        if st.session_state.predict_step > 1 and st.session_state.predict_step < 6:
            if st.button("← Previous", use_container_width=True):
                st.session_state.predict_step -= 1
                st.rerun()

    with col_next:
        if st.session_state.predict_step < 5 and st.session_state.predict_step < 6:
            if st.button("Next →", use_container_width=True):
                st.session_state.predict_step += 1
                st.rerun()
# -----------------------------
# PAGE: HEALTH INFO
# -----------------------------
elif page == "Health Info":

    st.markdown("### Understand the 7 Obesity Categories")
    st.markdown("Tap a tab below to see what each category means, its BMI range, and its typical health risks.")

    CATEGORY_INFO = {
        "Insufficient Weight": {
            "range": "BMI below 18.5", "badge": "badge-warning",
            "desc": "Body weight is lower than what's considered healthy for your height.",
            "risks": ["Weakened immune system", "Nutrient deficiencies", "Fatigue and low energy", "Bone density loss over time"],
        },
        "Normal Weight": {
            "range": "BMI 18.5 – 24.9", "badge": "badge-healthy",
            "desc": "Body weight is within the healthy range for your height — the lowest risk category.",
            "risks": ["Low risk of weight-related disease", "Maintain with balanced diet and regular activity"],
        },
        "Overweight Level I": {
            "range": "BMI 25.0 – 27.4", "badge": "badge-warning",
            "desc": "Body weight is moderately above the healthy range.",
            "risks": ["Increased risk of high blood pressure", "Higher strain on joints", "Early insulin resistance risk"],
        },
        "Overweight Level II": {
            "range": "BMI 27.5 – 29.9", "badge": "badge-warning",
            "desc": "Body weight is significantly above the healthy range.",
            "risks": ["Elevated cholesterol risk", "Higher cardiovascular strain", "Increased risk of type 2 diabetes"],
        },
        "Obesity Type I": {
            "range": "BMI 30.0 – 34.9", "badge": "badge-danger",
            "desc": "Class I obesity — a meaningful increase in weight-related health risk.",
            "risks": ["Type 2 diabetes risk rises sharply", "Higher blood pressure risk", "Joint and mobility strain"],
        },
        "Obesity Type II": {
            "range": "BMI 35.0 – 39.9", "badge": "badge-danger",
            "desc": "Class II (severe) obesity — substantially elevated health risk.",
            "risks": ["High risk of heart disease", "Sleep apnea risk increases", "Greater metabolic strain"],
        },
        "Obesity Type III": {
            "range": "BMI 40.0 and above", "badge": "badge-danger",
            "desc": "Class III (morbid) obesity — the highest risk category, often warranting medical guidance.",
            "risks": ["Very high cardiovascular risk", "Significant diabetes risk", "Reduced life expectancy without intervention"],
        },
    }

    tabs = st.tabs(list(CATEGORY_INFO.keys()))
    for tab, (cat_name, info) in zip(tabs, CATEGORY_INFO.items()):
        with tab:
            st.markdown(f"""
            <div class="material-card" style="align-items:flex-start; text-align:left;">
                <span class="info-pill">{info['range']}</span>
                <span class="{info['badge']}" style="margin-bottom:14px;">{cat_name}</span>
                <p style="color:#334155; margin:14px 0 10px 0;">{info['desc']}</p>
                <div style="font-weight:700; color:#0F172A; margin-bottom:6px;">Typical Risk Factors</div>
                <ul style="color:#64748B; margin:0; padding-left:20px;">
                    {''.join(f"<li>{r}</li>" for r in info['risks'])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Quick BMI Calculator")
    st.markdown("Just here for a fast check — not the full assessment. For the complete AI-powered prediction, use **Predict My Risk**.")

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        h = st.number_input("Height (m)", min_value=1.20, max_value=2.20, value=1.70, step=0.01, key="quickbmi_h")
    with c2:
        w = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5, key="quickbmi_w")
    with c3:
        quick_bmi = w / (h ** 2)
        if quick_bmi < 18.5:
            qb, qc = "badge-warning", "Insufficient Weight"
        elif quick_bmi < 25:
            qb, qc = "badge-healthy", "Normal Weight"
        elif quick_bmi < 30:
            qb, qc = "badge-warning", "Overweight"
        else:
            qb, qc = "badge-danger", "Obesity Range"
        st.markdown(f"""
        <div class="calc-result-box">
            <div class="num">{quick_bmi:.1f}</div>
            <div class="lbl">Your BMI</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f'<div style="text-align:center; margin-top:10px;"><span class="{qb}">{qc}</span></div>', unsafe_allow_html=True)

# -----------------------------
# PAGE: WEIGHT LOSS TIPS
# -----------------------------
elif page == "Weight Loss Tips":

    st.markdown("### Practical Tips, Organized by Category")

    TIPS = {
        "Diet": [
            "Fill half your plate with vegetables at every meal.",
            "Swap sugary drinks for water or unsweetened tea.",
            "Eat slowly — it takes ~20 minutes for your brain to register fullness.",
            "Plan meals ahead to avoid impulsive high-calorie choices.",
        ],
        "Exercise": [
            "Aim for at least 150 minutes of moderate activity per week.",
            "Mix cardio with strength training for better long-term results.",
            "Take the stairs and walk short distances instead of driving.",
            "Find an activity you enjoy — consistency beats intensity.",
        ],
        "Sleep": [
            "Aim for 7–9 hours of sleep — poor sleep raises hunger hormones.",
            "Keep a consistent sleep schedule, even on weekends.",
            "Avoid screens for 30 minutes before bed.",
        ],
        "Mindset": [
            "Set realistic, gradual goals (0.5–1 kg per week is sustainable).",
            "Track progress with photos and measurements, not just the scale.",
            "Don't let one off day derail the whole plan — consistency over perfection.",
        ],
    }

    category = st.radio("Filter tips by category", list(TIPS.keys()), horizontal=True, key="tip_filter")
    for tip in TIPS[category]:
        st.markdown(f'<div class="tip-card">💡 {tip}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Daily Calorie Needs Calculator")
    st.markdown("Estimates your maintenance calories (TDEE) using the Mifflin-St Jeor formula, and a healthy deficit for weight loss.")

    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        gender_c = st.radio("Gender", ["Female", "Male"], key="calc_gender", horizontal=True)
        age_c = st.number_input("Age", min_value=10, max_value=100, value=25, key="calc_age")
    with cc2:
        height_c = st.number_input("Height (cm)", min_value=120, max_value=220, value=170, key="calc_height")
        weight_c = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=70.0, step=0.5, key="calc_weight")
    with cc3:
        activity_c = st.selectbox(
            "Activity level",
            ["Sedentary (little/no exercise)", "Light (1-3 days/week)", "Moderate (3-5 days/week)",
             "Active (6-7 days/week)", "Very Active (physical job/athlete)"],
            key="calc_activity"
        )

    if gender_c == "Male":
        bmr = 10 * weight_c + 6.25 * height_c - 5 * age_c + 5
    else:
        bmr = 10 * weight_c + 6.25 * height_c - 5 * age_c - 161

    activity_factors = {
        "Sedentary (little/no exercise)": 1.2,
        "Light (1-3 days/week)": 1.375,
        "Moderate (3-5 days/week)": 1.55,
        "Active (6-7 days/week)": 1.725,
        "Very Active (physical job/athlete)": 1.9,
    }
    tdee = bmr * activity_factors[activity_c]
    deficit_target = tdee - 500

    rc1, rc2 = st.columns(2)
    with rc1:
        st.markdown(f"""
        <div class="calc-result-box">
            <div class="num">{tdee:,.0f}</div>
            <div class="lbl">Calories/day to MAINTAIN weight</div>
        </div>
        """, unsafe_allow_html=True)
    with rc2:
        st.markdown(f"""
        <div class="calc-result-box" style="background:linear-gradient(135deg,#0EA5E9,#38BDF8);">
            <div class="num">{deficit_target:,.0f}</div>
            <div class="lbl">Calories/day to LOSE ~0.5 kg/week</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Today's Habit Tracker")
    st.markdown("Check off healthy habits as you complete them today.")

    HABITS = ["Drank at least 2L of water", "Ate vegetables with a meal", "Got 30+ minutes of activity",
              "Slept 7+ hours last night", "Avoided sugary drinks"]

    if "habit_checks" not in st.session_state:
        st.session_state.habit_checks = {h: False for h in HABITS}

    for h in HABITS:
        st.session_state.habit_checks[h] = st.checkbox(h, value=st.session_state.habit_checks[h], key=f"habit_{h}")

    completed = sum(st.session_state.habit_checks.values())
    pct_done = int(completed / len(HABITS) * 100)
    st.markdown(f"""
    <div class="habit-progress-wrap">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span style="font-weight:700; color:#0F172A;">Today's Progress</span>
            <span style="color:#0F766E; font-weight:700;">{completed}/{len(HABITS)} done</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width:{pct_done}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# PAGE: ABOUT
# -----------------------------
elif page == "About":

    st.markdown("### About VitalIndex")
    st.markdown("""
    <div class="material-card" style="align-items:flex-start; text-align:left;">
        <p style="color:#334155; margin:0;">
        VitalIndex uses a Random Forest machine learning model to estimate obesity risk category
        based on lifestyle, diet, and physical attributes. It's designed to give quick, data-driven
        insight — not a substitute for professional medical advice.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Model Insights: What Drives the Prediction?")
    st.markdown("This chart is generated live from the actual trained model — showing which factors it weighs most heavily.")

    display_names = {
        "Age": "Age", "Gender": "Gender", "Height": "Height", "Weight": "Weight",
        "CALC": "Alcohol Consumption", "FAVC": "High-Calorie Food", "FCVC": "Vegetable Intake",
        "NCP": "Meals per Day", "SCC": "Calorie Monitoring", "SMOKE": "Smoking",
        "CH2O": "Water Intake", "family_history_with_overweight": "Family History",
        "FAF": "Physical Activity", "TUE": "Tech Usage Time", "CAEC": "Snacking Between Meals",
        "BMI": "BMI", "MTRANS_Automobile": "Uses Car", "MTRANS_Bike": "Uses Bike",
        "MTRANS_Motorbike": "Uses Motorbike", "MTRANS_Public_Transportation": "Uses Public Transport",
        "MTRANS_Walking": "Walks",
    }

    importances = model.feature_importances_
    feat_names = [display_names.get(f, f) for f in model.feature_names_in_]
    imp_df = pd.DataFrame({"Feature": feat_names, "Importance": importances}).sort_values("Importance", ascending=True)

    fig_imp = go.Figure(go.Bar(
        x=imp_df["Importance"], y=imp_df["Feature"], orientation="h",
        marker=dict(color=imp_df["Importance"], colorscale=[[0, "#99F6E4"], [1, "#0F766E"]]),
    ))
    fig_imp.update_layout(
        height=550, margin=dict(l=10, r=10, t=10, b=10),
        xaxis_title="Relative Importance", plot_bgcolor="white", paper_bgcolor="white",
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("### Model Details")
    st.markdown(f"""
    <div class="stat-grid" style="grid-template-columns: repeat(3, 1fr);">
    <div class="material-card">
        <div class="stat-number">Random Forest</div>
        <div class="stat-label">Algorithm</div>
    </div>
    <div class="material-card">
        <div class="stat-number">99.5%</div>
        <div class="stat-label">Test Accuracy</div>
    </div>
    <div class="material-card">
        <div class="stat-number">{model.n_features_in_}</div>
        <div class="stat-label">Input Features</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Frequently Asked Questions")
    with st.expander("How is my obesity category predicted?"):
        st.write("Your answers are converted into the same numerical format the model was trained on, "
                 "then a Random Forest classifier — trained on thousands of records — predicts the most "
                 "likely category along with a confidence score.")
    with st.expander("Is this a medical diagnosis?"):
        st.write("No. VitalIndex provides a data-driven estimate for informational purposes only. "
                 "Please consult a healthcare professional for medical advice.")
    with st.expander("What data is used?"):
        st.write("Age, gender, height, weight, family history, eating habits, physical activity, "
                 "water intake, screen time, and transportation habits.")