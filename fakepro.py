import pickle
import streamlit as st
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Fake Account Detection",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
.result-box {
    padding: 20px;
    border-radius: 10px;
    font-size:20px;
    font-weight:bold;
    text-align:center;
}
.fake {
    background-color:#7f1d1d;
    color:white;
}
.real {
    background-color:#14532d;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("fake profile.sav", "rb"))

# ---------------- SIDEBAR ----------------
with st.sidebar:
    selected = option_menu(
        "🛡️ AI Cyber Security",
        ["Prediction", "About"],
        icons=["shield-lock", "info-circle"],
        default_index=0
    )

# ---------------- PREDICTION PAGE ----------------
if selected == "Prediction":

    st.title("🧠 AI Powered Fake Account Detection")
    st.markdown("### Enter Profile Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("Name")
        screen_name = st.text_input("Screen Name")
        profile_link_color = st.text_input("Profile Link Color")

    with col2:
        statuses_count = st.number_input("Statuses Count", min_value=0)
        followers_count = st.number_input("Followers Count", min_value=0)
        friends_count = st.number_input("Friends Count", min_value=0)

    with col3:
        favourites_count = st.number_input("Favourites Count", min_value=0)
        listed_count = st.number_input("Listed Count", min_value=0)
        created_at = st.text_input("Created At (Wed Oct 10 20:19:24 +0000 2018)")

    st.markdown("---")

    if st.button("🔍 Predict Account Type"):

        name_len = len(name)
        screen_len = len(screen_name)
        color_len = len(profile_link_color)

        try:
            dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
            year = dt.year
        except:
            year = 0

        features = np.array([[
            name_len,
            screen_len,
            statuses_count,
            followers_count,
            friends_count,
            favourites_count,
            listed_count,
            color_len,
            year
        ]])

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        real_prob = round(probability[0] * 100, 2)
        fake_prob = round(probability[1] * 100, 2)

        st.markdown("## 📊 Prediction Confidence")

        colA, colB = st.columns(2)

        with colA:
            st.metric(label="Real Account Probability", value=f"{real_prob}%")

        with colB:
            st.metric(label="Fake Account Probability", value=f"{fake_prob}%")

        st.markdown("---")

        if prediction == 1:
            st.markdown(
                f'<div class="result-box fake">🚨 Account is FAKE ({fake_prob}%)</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="result-box real">✅ Account is REAL ({real_prob}%)</div>',
                unsafe_allow_html=True
            )

# ---------------- ABOUT PAGE ----------------
elif selected == "About":

    st.title("📌 About This Project")

    st.write("""
    AI Powered Fake Account Detection System
    
    Target Column:
    0 → Real Account  
    1 → Fake Account  
    
    This system uses Machine Learning to detect 
    suspicious social media accounts.
    """)
