import streamlit as st

# Import 2 hàm giao diện mà chúng ta vừa đóng gói
from views.auth_view import show_auth_page
from views.chat_view import show_chat_page

st.set_page_config(page_title="EnglishMate", page_icon="🎓")

# Khởi tạo trạng thái mặc định
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Điều hướng (Routing) rất rõ ràng:
if st.session_state["logged_in"]:
    show_chat_page()
else:
    show_auth_page()
