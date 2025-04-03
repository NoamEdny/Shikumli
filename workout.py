# workout.py - Camera page
import streamlit as st
import cv2
from video_processor import process_frame

def workou_page():
    st.title("מצלמה - ניתוח תנועה")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Could not open webcam. Please check permissions.")
        return

    stframe = st.empty()
    stop_button = st.button("עצור", key="stop_button")

    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to read from webcam.")
            break
        
        processed_frame = process_frame(frame)
        stframe.image(processed_frame, channels="BGR")
    
    cap.release()
    st.success("מצלמה נסגרה בהצלחה.")