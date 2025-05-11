import streamlit as st
import os
from pathlib import Path

from utils import load_css, add_bg_with_overlay, save_user_to_db, render_welcome_screen


# Configure page
st.set_page_config(
    page_title="AgriPreneur Finance Platform | Login",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT_DIR = Path(__file__).parent.resolve()
load_css(os.path.join(ROOT_DIR, "static", "css", "style.css"))


if not st.experimental_user.is_logged_in:
    render_welcome_screen()

if st.experimental_user.is_logged_in:
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

    with st.sidebar:
        st.write(f'👋 Welcome to NaijaYield, *{user_name}*',)
        st.button("Log out", on_click=st.logout)
