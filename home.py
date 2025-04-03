# home.py - Welcome screen
import streamlit as st

def home_page():
    st.title("ברוך הבא לאימון הפיזיותרפיה שלך")
    st.write("עקוב אחר ההתקדמות שלך והתאמן עם פידבק בזמן אמת!")
    
    # Example progress bar (replace with real data tracking)
    days_trained = st.session_state.get("days_trained", 8)
    st.progress(days_trained / 30)  # Assuming a 30-day goal
    
    st.markdown(f"<h1 style='text-align: center; color: blue;'>{days_trained} ימים</h1>", unsafe_allow_html=True)
    
    if st.button("התחל אימון", key="start_button"):
        st.session_state.page = "camera"
        st.rerun()