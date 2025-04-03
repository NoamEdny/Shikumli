# utils/session_state.py
import streamlit as st

def initialize_session_state():
    """
    Initialize all session state variables needed across the application.
    Call this function at the beginning of each page to ensure consistent state.
    """
    # Exercise selection
    if 'selected_exercise' not in st.session_state:
        st.session_state.selected_exercise = None
    
    # UI state tracking
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
    
    # Workout progress tracking
    if 'workout_started' not in st.session_state:
        st.session_state.workout_started = False
    
    if 'workout_completed' not in st.session_state:
        st.session_state.workout_completed = False
    
    # User progress tracking
    if 'total_workouts' not in st.session_state:
        st.session_state.total_workouts = 0
    
    if 'streak_days' not in st.session_state:
        st.session_state.streak_days = 8  # Starting with 8 as shown in your UI
    
    if 'last_workout_date' not in st.session_state:
        st.session_state.last_workout_date = None

def reset_exercise_selection():
    """Reset the exercise selection state"""
    st.session_state.selected_exercise = None
    st.session_state.button_clicked = False
    st.session_state.workout_started = False

def complete_workout():
    """Mark the current workout as completed and update stats"""
    import datetime
    
    st.session_state.workout_completed = True
    st.session_state.total_workouts += 1
    
    # Update streak logic
    today = datetime.date.today()
    if st.session_state.last_workout_date is None:
        # First workout
        st.session_state.streak_days = 1
    elif (today - st.session_state.last_workout_date).days == 1:
        # Consecutive day
        st.session_state.streak_days += 1
    elif (today - st.session_state.last_workout_date).days > 1:
        # Streak broken
        st.session_state.streak_days = 1
    
    # Update last workout date
    st.session_state.last_workout_date = today

def get_progress_percentage():
    """Calculate and return the user's progress percentage"""
    # This is a placeholder - you would implement your own logic
    # based on your app's requirements
    if st.session_state.total_workouts == 0:
        return 0
    
    # Example: if goal is 30 workouts
    goal = 30
    progress = min(st.session_state.total_workouts / goal * 100, 100)
    return progress