# Home.py
import streamlit as st
from utils.styling import apply_common_styling, apply_landing_styling
from utils.session_state import initialize_session_state

# Initialize session state
initialize_session_state()

# Apply styling
apply_common_styling()
apply_landing_styling()

# Landing page content with improved styling
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="progress-title">Progress</div>', unsafe_allow_html=True)
st.markdown(f'<div class="progress-bar-container"><div class="progress-bar-fill" style="width: {st.session_state.streak_days * 5}%;"></div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="days-counter"><div class="days-number">{st.session_state.streak_days}</div><div class="days-text">days</div></div>', unsafe_allow_html=True)

# Link to the drills page with improved button styling
if st.button("Start", key="start_button_landing"):
    # Set any needed session state
    st.session_state.button_clicked = False
    st.session_state.selected_exercise = None
    # Navigate to the choose drills page
    st.switch_page("pages/01_choose_drills.py")

st.markdown('</div>', unsafe_allow_html=True)