import streamlit as st
import pandas as pd
import numpy as np



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.write("Welcome to the app!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

else:
    with st.form("login_form"):
        st.text_input("Username",key = "username")
        st.text_input("Password", type="password",key = "password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if st.session_state.username == "admin" and st.session_state.password == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")
        
