import streamlit as st
import os
from pathlib import Path

from utils import load_css, add_bg_with_overlay, save_user_to_db, render_welcome_screen

sidebar_state = "expanded" if st.experimental_user.is_logged_in else "collapsed"


# Configure page
st.set_page_config(
    page_title="AgriPreneur Finance Platform | Login",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state=sidebar_state
)

ROOT_DIR = Path(__file__).parent.resolve()
load_css(os.path.join(ROOT_DIR, "static", "css", "style.css"))

def set_naijayield_theme():
    """Set the NaijaYield brand theme with a soft green background"""
    st.markdown("""
    <style>
    /* Main app background */
    .stApp {
        background-color: #f0f7f0;  /* Very light green */
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #e8f5e9;  /* Slightly darker light green */
        border-right: 1px solid #c8e6c9;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2e7d32;  /* Dark green for headers */
    }
    
    /* Improve container visibility */
    .stBlock, div.stBlock {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

if not st.experimental_user.is_logged_in:
    render_welcome_screen()

else:

    set_naijayield_theme()

    if 'user_processed' not in st.session_state:
        user_data = {
            'email': st.experimental_user.email,
            'name': st.experimental_user.name,
            'given_name': getattr(st.experimental_user, 'given_name', ''),
            'family_name': getattr(st.experimental_user, 'family_name', '')
        }
        
        user_status = save_user_to_db(user_data)
        st.session_state['user_processed'] = True

    user_name = st.experimental_user.name
    #st.write(f"**{user_name}**")

    with st.sidebar:
        st.write("")
        st.write(f'👋 Welcome to **NaijaYield**, {user_name}',)
        st.button("Log out", on_click=st.logout)

    available_pages = {}
    home = st.Page("./page/Dashboard.py", title="General Dashboard", icon="📊", default=True)
    household_analytics = st.Page("./page/hhid_analytics.py", title="Individual Analytcs", icon="👨‍🌾")

    pages = [home, household_analytics]
    pg = st.navigation(pages)

    pg.run()
