import streamlit as st
from workout import workout_page

# Function for exercise selection
def choose_drills_page():
    st.title("Choose Exercise")

    # Check if an exercise has been selected
    if 'selected_exercise' not in st.session_state:
        st.session_state.selected_exercise = None

    # Create exercise options
    exercise_options = ["squat", "leg rise", "hand rise"]
    #exercise_workout = {"squat": processed_frame, "leg rise"}
    
    for exercise in exercise_options:
        if st.button(exercise):
            st.write(f"let start the {exercise} exercise!")
            workout_page()


