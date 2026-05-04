import streamlit as st
import requests

def show_auth_page():
    """Render the authentication page (Login/Signup).

    Displays a tabbed interface allowing users to either log in to an existing 
    account or register a new one. Handles form submission, API requests to the 
    backend, and updates the session state upon successful authentication. 
    Also includes a Google Sign-In option if configured.
    """
    # Center the form in a narrow column for wide layout
    _, center, _ = st.columns([1, 2, 1])

    with center:
        st.title("Welcome to EnglishMate")

        tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
        
        # --- SIGN UP UI ---
        with tab_signup:
            st.subheader("Create a new account")
            
            with st.form("signup_form"):
                new_email = st.text_input("Your Email")
                new_password = st.text_input("Password", type="password")
                submit_btn = st.form_submit_button("Sign Up Now")
                
                if submit_btn:
                    payload = {
                        "email": new_email,
                        "password": new_password
                    }
                    
                    api_url = "http://127.0.0.1:8000/auth/register"  
                    
                    try:
                        response = requests.post(api_url, json=payload)
                        
                        if response.status_code == 200:  
                            st.success("Account created successfully! Please switch to the Login tab.")
                        else:
                            error_msg = response.json().get("detail", "Unknown error")
                            st.error(f"Registration failed: {error_msg}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to the backend server. Is uvicorn running?")


        # --- LOGIN UI ---
        with tab_login:
            st.subheader("Login")
            
            with st.form("login_form"):
                login_email = st.text_input("Email")
                login_password = st.text_input("Password", type="password")
                login_btn = st.form_submit_button("Login")
                
                if login_btn:
                    payload = {
                        "email": login_email,
                        "password": login_password
                    }
                    
                    api_url = "http://127.0.0.1:8000/auth/login" 
                    
                    try:
                        response = requests.post(api_url, json=payload)  
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Store credentials in Session State
                            st.session_state["logged_in"] = True
                            st.session_state["user_id"] = data.get("user_id")
                            
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            error_msg = response.json().get("detail", "Unknown error")
                            st.error(f"Login failed: {error_msg}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to the backend server.")

            st.write("---")
            
            # --- GOOGLE LOGIN ---
            try:
                google_cfg = st.secrets["google-login"]
                google_login_url = google_cfg.get("google-url", "")
                if google_login_url:
                    st.markdown(
                        f"""
                        <a href="{google_login_url}" target="_self" style="
                            display: inline-block;
                            padding: 0.5em 1em;
                            color: #000;
                            background-color: #fff;
                            border: 1px solid #ccc;
                            border-radius: 4px;
                            text-decoration: none;
                            font-weight: bold;
                            text-align: center;
                            width: 100%;
                        ">
                            Login with Google
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
            except Exception:
                st.info("Google Login is not configured. Please add credentials to `.streamlit/secrets.toml` to enable this feature.")