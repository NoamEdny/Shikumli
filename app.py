import streamlit as st
import cv2
from video_processor import process_frame

# app.py - Main file to manage navigation
import streamlit as st
from home import home_page
from workout import workou_page

def main():
    st.title("הקבוצה של הטובים")

    # Try to open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Could not open webcam. Please check permissions in System Settings > Privacy & Security > Camera.")
        return

    stframe = st.empty()
    stop_button = st.button("Stop", key="stop_button")

    # Loop until the user presses Stop
    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to read from webcam.")
            break

        # Process frame: detect pose and draw results
        image, finished = process_frame(frame)
        stframe.image(image, channels="BGR")

    cap.release()
    st.success("Camera released. You can now close the app.")

if __name__ == "__main__":
    main()

