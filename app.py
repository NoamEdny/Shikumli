import streamlit as st
import cv2
from video_processor import process_frame

# app.py - Main file to manage navigation
import streamlit as st
from home import home_page
from workout import workou_page

def main():
    st.set_page_config(page_title="Physio Trainer", page_icon="🏋️", layout="centered")
    
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "camera":
        workou_page()

if __name__ == "__main__":
    main()

