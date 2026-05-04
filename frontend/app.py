import streamlit as st

# Import 2 hàm giao diện mà chúng ta vừa đóng gói
from views.vocab_view import show_vocab_page
from views.auth_view import show_auth_page
from views.chat_view import show_chat_page

st.set_page_config(page_title="EnglishMate", page_icon="🎓")

# Khởi tạo trạng thái mặc định
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Điều hướng (Routing) rất rõ ràng:
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

