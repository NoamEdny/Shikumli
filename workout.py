# workout.py - Camera page
import streamlit as st
import cv2
from video_processor import process_frame

<<<<<<< HEAD
def workou_page():
    st.title("מצלמה - ניתוח תנועה")
=======
def workout_page():
>>>>>>> 8e9d99141bbfc398d0fea513e0d05979147b341d
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Could not open webcam. Please check permissions.")
        return

    stframe = st.empty()
<<<<<<< HEAD
    stop_button = st.button("עצור", key="stop_button")
=======
    stop_button = st.button("next exercise", key="stop_button")
>>>>>>> 8e9d99141bbfc398d0fea513e0d05979147b341d

    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to read from webcam.")
            break
        
        processed_frame = process_frame(frame)
        stframe.image(processed_frame, channels="BGR")
    
    cap.release()
<<<<<<< HEAD
    st.success("מצלמה נסגרה בהצלחה.")
=======
    st.success("camera closed successfully")
>>>>>>> 8e9d99141bbfc398d0fea513e0d05979147b341d
