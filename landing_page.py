# landing_page.py (updated)
import streamlit as st
from choose_drills import choose_drills_page

# הגדרת CSS מותאם אישית לעיצוב
st.markdown(
    """
    <style>
        .stApp { background-color: #FFF8E1; }
        .main-container {
            background-color: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 600px;
            margin: 40px auto;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .progress-title {
            color: #1A2E44;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .progress-bar-container {
            background-color: #D1F2EB;
            border-radius: 15px;
            height: 30px;
            width: 100%;
            margin: 20px 0 40px 0;
            overflow: hidden;
        }
        .progress-bar-fill {
            background-color: #48C9B0;
            height: 100%;
            width: 50%;
            border-radius: 15px;
        }
        .days-counter {
            background-color: #48C9B0;
            color: #1A2E44;
            width: 180px;
            height: 180px;
            border-radius: 50%;
            margin: 30px auto;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .days-number { font-size: 80px; font-weight: bold; line-height: 1; }
        .days-text { font-size: 28px; }
        .stButton > button {
            background-color: #F4A261 !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 15px 0 !important;
            font-size: 28px !important;
            font-weight: bold !important;
            width: 100% !important;
            cursor: pointer !important;
            margin-top: 30px !important;
            transition: background-color 0.3s !important;
        }
        .stButton > button:hover { background-color: #E76F51 !important; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
    </style>
    """,
    unsafe_allow_html=True
)

def landing_page():
    # Make sure we have the session state initialized
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    
    # Clear any previous button clicks when returning to landing page
    if st.session_state.page == 'landing':
        st.session_state.button_clicked = False
        st.session_state.selected_exercise = None
    
    if st.session_state.page == 'landing':
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<div class="progress-title">Progress</div>', unsafe_allow_html=True)
        st.markdown('<div class="progress-bar-container"><div class="progress-bar-fill"></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="days-counter"><div class="days-number">8</div><div class="days-text">days</div></div>', unsafe_allow_html=True)
        
        # Use a unique key for the button to avoid reuse issues
        if st.button("Start", key="start_button_landing"):
            st.session_state.page = 'drills'
            # Use st.rerun() instead of st.experimental_rerun()
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif st.session_state.page == 'drills':
        # Call the choose_drills_page function
        choose_drills_page()