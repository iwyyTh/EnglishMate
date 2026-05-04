import streamlit as st

# Import 2 hàm giao diện mà chúng ta vừa đóng gói
from views.vocab_view import show_vocab_page
from views.auth_view import show_auth_page
from views.chat_view import show_chat_page

st.set_page_config(page_title="EnglishMate", page_icon="🎓")

import requests

# Khởi tạo trạng thái mặc định
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- XỬ LÝ GOOGLE LOGIN CALLBACK ---
def clear_google_query_params():
    params = st.query_params.to_dict()
    if "id_token" in params:
        del params["id_token"]
        st.query_params.clear()
        for k, v in params.items():
            st.query_params[k] = v

def handle_google_login_callback():
    if st.session_state.get("logged_in"):
        return

    id_token = st.query_params.get("id_token")
    if id_token:
        try:
            r = requests.post("http://127.0.0.1:8000/auth/google", json={"id_token": id_token})
            r.raise_for_status()
            user = r.json()
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user.get("user_id")
            clear_google_query_params()
            st.success("Đăng nhập Google thành công! 🎉")
            st.rerun()
        except Exception as e:
            st.error(f"Đăng nhập Google thất bại: {e}")
            clear_google_query_params()

handle_google_login_callback()

# Điều hướng (Routing) rất rõ ràng:
if st.session_state["logged_in"]:
    # Tạo Sidebar bên hông trái
    st.sidebar.title("EnglishMate")
    page = st.sidebar.radio("Danh mục", ["💬 Chatbot", "📚 Kho Từ Vựng"])
    
    # Cầu dao chuyển trang
    if page == "💬 Chatbot":
        show_chat_page()
    elif page == "📚 Kho Từ Vựng":
        show_vocab_page()
else:
    show_auth_page()

