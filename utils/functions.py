import streamlit as st
import os
from pathlib import Path
import base64
import uuid
import duckdb
from datetime import datetime

ROOT_DIR = Path(__file__).parent.resolve()
@st.cache_resource(show_spinner='Connecting... 🔌')
def get_duckdb_connection():
    motherduck_token = st.secrets["motherduck_token"]
    return duckdb.connect(f'md:NaijaYield?motherduck_token={motherduck_token}')


# Function to load CSS from file
def load_css(css_file):
    """Load CSS styling from a file"""
    with open(css_file, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def add_bg_with_overlay(transparent=None):

    if transparent:
        st.markdown("""
        <style>
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.3;  /* Adjust this value: 0 = fully transparent, 1 = fully opaque */
            z-index: -1;
        }

        .stApp {
            position: relative;
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown(
            """
            <style>
            .stApp {
                background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

def render_welcome_screen():
    """Render the welcome screen with login button"""
    
    add_bg_with_overlay()
        
    # Welcome text
    st.markdown("""
    <div class="welcome-text">
        <h1>NaijaYield Finance Platform</h1>
        <p>Empowering young Nigerian farmers with access to affordable finance through data-driven credit assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a centered container for the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="logo-container">
                <div class="logo">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#2e7d32" width="80px" height="80px">
                        <path d="M0 0h24v24H0z" fill="none"/>
                        <path d="M12 22l-6.5-6.5H10v-5h4v5h4.5L12 22zm0-20l6.5 6.5H14v5h-4v-5H5.5L12 2z"/>
                    </svg>
                </div>
            </div>
            <div class="login-header">
                <h1>Welcome to NaijaYield</h1>
                <p>Please sign in to continue</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("Log in/register with Google", key="google_login"):
            st.login()  
        
        st.markdown("""
        <div class="login-footer">
            <p>By signing in, you agree to our <a href="#" style="color: #2e7d32;">Terms of Service</a> and <a href="#" style="color: #2e7d32;">Privacy Policy</a></p>
            <p style="margin-top: 10px;">© 2025 NaijaYield. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    

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


def save_user_to_db(user_data):
    conn = get_duckdb_connection()

    try:
        email = user_data.get('email')
        if not email:
            return "error: No email provided"
            
        first_name = user_data.get('given_name', '')
        last_name = user_data.get('family_name', '')
        name = user_data.get('name', f"{first_name} {last_name}".strip())
        
        email = email.replace("'", "''")
        first_name = first_name.replace("'", "''") if first_name else ""
        last_name = last_name.replace("'", "''") if last_name else ""
        name = name.replace("'", "''") if name else ""
        
        # Check if user already exists
        user_exists = conn.execute(f"SELECT user_id FROM naijayield_users WHERE email = '{email}'").fetchone()
        
        if user_exists:
            conn.execute(f"""
                UPDATE naijayield_users 
                SET login_count = login_count + 1,
                    last_login = CURRENT_TIMESTAMP
                WHERE email = '{email}'
            """)
            
            
        else:
            user_id = str(uuid.uuid4())
            conn.execute(f"""
                INSERT INTO naijayield_users (
                    user_id, email, name, first_name, last_name, 
                    login_count, last_login, created_at
                ) VALUES (
                    '{user_id}', '{email}', '{name}', '{first_name}', '{last_name}', 
                    1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                )
            """)
            
            print(f"===== ADDED NEW USER - {email} =============")
            return {"status": "new_user"}
    
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return {"status": "error", "message": str(e)}
