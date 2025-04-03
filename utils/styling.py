# utils/styling.py
import streamlit as st

def apply_common_styling():
    """Apply common styling across all pages"""
    st.set_page_config(
        page_title="Exercise App",
        page_icon="💪",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Hide default Streamlit elements
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def apply_landing_styling():
    """Apply styling specific to the landing page"""
    st.markdown(
        """
        <style>
            .stApp { 
                background-color: #FFF8E1; 
                padding: 0;
                margin: 0;
            }

            .progress-title {
                color: #1A2E44;
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 30px;
                font-family: 'Helvetica Neue', Arial, sans-serif;
            }
            .progress-bar-container {
                background-color: #D1F2EB;
                border-radius: 15px;
                height: 30px;
                width: 100%;
                margin: 20px 0 40px 0;
                overflow: hidden;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
            }
            .progress-bar-fill {
                background-color: #48C9B0;
                height: 100%;
                width: 50%;
                border-radius: 15px;
                transition: width 0.5s ease-in-out;
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
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                border: 4px solid #E8F8F5;
            }
            .days-number { 
                font-size: 80px; 
                font-weight: bold; 
                line-height: 1;
                font-family: 'Helvetica Neue', Arial, sans-serif;
            }
            .days-text { 
                font-size: 28px;
                font-family: 'Helvetica Neue', Arial, sans-serif;
            }
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
                transition: all 0.3s !important;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
                font-family: 'Helvetica Neue', Arial, sans-serif !important;
            }
            .stButton > button:hover { 
                background-color: #E76F51 !important; 
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 8px rgba(0,0,0,0.15) !important;
            }
            .stButton > button:active {
                transform: translateY(1px) !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def apply_drills_styling():
    """Apply styling specific to the drills page"""
    st.markdown(
        """
        <style>
            .stApp { background-color: #FFF8E1; }
            /* Banner styling */
            .banner {
                background-color: #C1D8C3;
                padding: 20px;
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                color: #6A9C89;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                font-family: 'Helvetica Neue', Arial, sans-serif;
            }

            /* Button styling */
            .stButton>button {
                background-color: #FFF5E4 !important;
                color: black !important;
                border-radius: 10px !important;
                font-size: 18px !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: all 0.3s !important;
                width: auto !important;
                margin: 10px auto !important;
                display: block !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                font-family: 'Helvetica Neue', Arial, sans-serif !important;
            }

            /* Button hover effect */
            .stButton>button:hover {
                background-color: #ffebd2 !important;
                cursor: pointer !important;
                transform: translateY(-2px) !important;
                box-shadow: 0 4px 6px rgba(0,0,0,0.15) !important;
            }
            
            .stButton>button:active {
                transform: translateY(1px) !important;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
            }

            /* Image container styling */
            .image-container {
                width: 200px;
                height: 200px;
                border-radius: 50%;
                overflow: hidden;
                margin: 0 auto 15px auto;
                position: relative;
                border: 3px solid #6A9C89;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }
            
            .image-container:hover {
                transform: scale(1.05);
                border-color: #8BBAA8;
                box-shadow: 0 6px 12px rgba(0,0,0,0.25);
            }
            
            /* Image styling */
            .image-container img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                object-position: center;
                transition: transform 0.5s ease;
            }
            
            .image-container:hover img {
                transform: scale(1.1);
            }
            
            /* Back button styling */
            .back-button button {
                background-color: #6A9C89 !important;
                color: white !important;
            }
            
            /* Exercise columns styling */
            .exercise-column {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .exercise-column:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }
            
            /* Exercise name styling */
            .exercise-name {
                font-size: 22px;
                font-weight: bold;
                color: #6A9C89;
                margin: 10px 0;
                font-family: 'Helvetica Neue', Arial, sans-serif;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def apply_workout_styling():
    """Apply styling specific to the workout page"""
    st.markdown(
        """
        <style>
            .stApp { background-color: #FFF8E1; }
            
            /* Title styling */
            h1 {
                color: #6A9C89 !important;
                text-align: center !important;
                font-family: 'Helvetica Neue', Arial, sans-serif !important;
                margin-bottom: 30px !important;
                font-size: 36px !important;
            }
            
            /* Video container styling */
            .stImage {
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
                margin: 20px auto !important;
                max-width: 800px !important;
            }
            
            /* Button styling */
            .stButton>button {
                background-color: #E76F51 !important;
                color: white !important;
                border-radius: 10px !important;
                font-size: 18px !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: all 0.3s !important;
                width: auto !important;
                margin: 10px auto !important;
                display: block !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
                font-family: 'Helvetica Neue', Arial, sans-serif !important;
            }
            
            /* Success message styling */
            .stSuccess {
                background-color: #C1D8C3 !important;
                color: #2C3E50 !important;
                border-radius: 10px !important;
                padding: 16px !important;
                font-family: 'Helvetica Neue', Arial, sans-serif !important;
            }
            
            /* Navigation buttons container */
            .stColumnContainer {
                max-width: 600px !important;
                margin: 20px auto !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )