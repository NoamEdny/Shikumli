import streamlit as st
from workout import workout_page  # Import the workout page function

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

        /* Button container to center buttons horizontally */
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
            font-size: 24px;
            padding: 15px 30px;
            border: none;
            transition: 0.3s;
            width: 200px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 10px;
        }

        /* Button hover effect */
        .stButton>button:hover {
            background-color: #ffebd2;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to choose an exercise
def choose_drills_page():
    # Display banner at the top of the page
    st.markdown('<div class="banner">Choose Your Exercise</div>', unsafe_allow_html=True)

    # Initialize session state for exercise selection
    if 'selected_exercise' not in st.session_state:
        st.session_state.selected_exercise = None

    # Create a horizontal button layout
    col1, col2, col3 = st.columns([1, 1, 1])

    # List of exercises
    exercise_options = ["Squat", "Leg Rise", "Hand Rise"]

    # Assign buttons to columns to keep them centered
    with col1:
        if st.button(exercise_options[0]):
            st.session_state.selected_exercise = exercise_options[0]
    with col2:
        if st.button(exercise_options[1]):
            st.session_state.selected_exercise = exercise_options[1]
    with col3:
        if st.button(exercise_options[2]):
            st.session_state.selected_exercise = exercise_options[2]

    # If an exercise is selected, navigate to the workout page
    if st.session_state.selected_exercise:
        st.write(f"Let's start the {st.session_state.selected_exercise} exercise!")
        workout_page()
