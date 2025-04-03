# choose_drills.py (updated with fixed image styling)
import streamlit as st
from workout import workout_page
import os

# Custom CSS for styling
st.markdown(
    """
    <style>
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
        }

        /* Button container */
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }

        /* Styling for buttons */
        .stButton>button {
            background-color: #FFF5E4;
            color: black;
            border-radius: 10px;
            font-size: 18px;
            padding: 10px 20px;
            border: none;
            transition: 0.3s;
            width: auto;
            margin: 10px auto;
            display: block;
        }

        /* Button hover effect */
        .stButton>button:hover {
            background-color: #ffebd2;
            cursor: pointer;
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
        }
        
        /* Image styling */
        .image-container img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to display the drill selection page
def choose_drills_page():
    st.markdown('<div class="banner">Choose Your Exercise</div>', unsafe_allow_html=True)

    # Initialize session state variables if they don't exist
    if 'selected_exercise' not in st.session_state:
        st.session_state.selected_exercise = None
    
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
        
    if 'workout_started' not in st.session_state:
        st.session_state.workout_started = False

    # Define exercises with their corresponding image paths
    exercises = {
        "Squat": "pictures/squat_jumps.jpg",
        "Leg Rise": "pictures/lag.jpg",
        "Hand Rise": "pictures/hand.jpg"
    }

    # Create columns for layout
    cols = st.columns(len(exercises))

    # Display images if no button has been clicked yet
    if not st.session_state.button_clicked:
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
    
    # Always display the buttons
    for i, (exercise, img_path) in enumerate(exercises.items()):
        with cols[i]:
            # Use a unique key for each button to avoid reuse issues
            if st.button(exercise, key=f"exercise_button_{i}"):
                st.session_state.selected_exercise = exercise
                st.session_state.button_clicked = True
                st.session_state.workout_started = True
                st.rerun()

    # Add a back button to return to landing page
    if st.button("Back to Home", key="back_to_home"):
        st.session_state.page = 'landing'
        st.session_state.button_clicked = False
        st.session_state.selected_exercise = None
        st.rerun()

    # If an exercise is selected and workout has started, navigate to the workout page
    if st.session_state.selected_exercise and st.session_state.workout_started:
        st.write(f"Let's start the {st.session_state.selected_exercise} exercise!")
        # Set workout_started to False to prevent repeated calls
        st.session_state.workout_started = False
        # Call the original workout_page function
        workout_page()

# Function to convert image to base64 for embedding in HTML
def get_image_base64(image_path):
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()