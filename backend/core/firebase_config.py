import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore


def get_auth_client():

    firebase_cfg = st.secrets["firebase_client"]
    firebase_app = pyrebase.initialize_app(firebase_cfg)

    auth = firebase_app.auth()
    return auth


def get_firestore_client():
    if not firebase_admin._apps:
        cred_dict = dict(st.secrets["firebase_admin"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

    return firestore.client()