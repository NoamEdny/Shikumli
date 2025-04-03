import streamlit as st

def navigate_to_workout(exercise):
    st.session_state.selected_exercise = exercise
    st.session_state.page = 'workout'

def choose_drills_page():
    # Display banner at the top of the page
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
    
    st.markdown('<div class="banner">Choose Your Exercise</div>', unsafe_allow_html=True)

    # Create a horizontal button layout
    col1, col2, col3 = st.columns([1, 1, 1])

    # List of exercises
    exercise_options = ["Squat", "Leg Rise", "Hand Rise"]

    # Assign buttons to columns to keep them centered
    with col1:
        if st.button(exercise_options[0]):
            navigate_to_workout(exercise_options[0])
    with col2:
        if st.button(exercise_options[1]):
            navigate_to_workout(exercise_options[1])
    with col3:
        if st.button(exercise_options[2]):
            navigate_to_workout(exercise_options[2])