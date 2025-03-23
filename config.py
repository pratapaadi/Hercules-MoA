import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def get_api_key():
    return os.getenv("GEMINI_API_KEY")

# Page configuration
def configure_page():
    st.set_page_config(
        page_title="Mixture of Agents Demo",
        layout="wide",
        initial_sidebar_state="expanded"
    )
     # Add custom CSS to center the title
    st.markdown("""
        <style>
        .title {
            text-align: center;
            padding: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []