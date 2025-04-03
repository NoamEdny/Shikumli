# pages/01_choose_drills.py
import streamlit as st
import os
import base64
from utils.styling import apply_common_styling, apply_drills_styling

# Apply styling
apply_common_styling()
apply_drills_styling()

# Initialize session state if needed
if 'selected_exercise' not in st.session_state:
    st.session_state.selected_exercise = None

# Function to convert image to base64 for embedding in HTML
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Page header
st.markdown('<div class="banner">Choose Your Exercise</div>', unsafe_allow_html=True)

# Define exercises with their corresponding image paths
exercises = {
    "Squat": "pictures/squat_jumps.jpg",
    "Leg Rise": "pictures/lag.jpg",
    "Hand Rise": "pictures/hand.jpg"
}

# Create columns for layout
cols = st.columns(len(exercises))

# Display images and buttons
for i, (exercise, img_path) in enumerate(exercises.items()):
    with cols[i]:
        if os.path.exists(img_path):
            # Create a circular container for the image using HTML/CSS
            st.markdown(f"""
                <div class="image-container">
                    <img src="data:image/png;base64,{get_image_base64(img_path)}" alt="{exercise}">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Error: Image {img_path} not found!")
        
        # Exercise selection button
        if st.button(exercise, key=f"exercise_button_{i}"):
            st.session_state.selected_exercise = exercise
            # Navigate to the workout page
            st.switch_page("pages/02_workout.py")

# Back button to return to home page
with st.container():
    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("Back to Home", key="back_to_home"):
        st.switch_page("Home.py")
    st.markdown('</div>', unsafe_allow_html=True)