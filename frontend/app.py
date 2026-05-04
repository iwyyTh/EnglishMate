import streamlit as st

# Import the views (UI pages)

from views.vocab_view import show_vocab_page
from views.auth_view import show_auth_page
from views.chat_view import show_chat_page
from views.flashcard_view import show_flashcard_page

st.set_page_config(page_title="EnglishMate", layout="wide")

import requests

# Initialize default session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- HANDLE GOOGLE LOGIN CALLBACK ---
def clear_google_query_params():
    """Remove the 'id_token' from the URL query parameters."""
    params = st.query_params.to_dict()
    if "id_token" in params:
        del params["id_token"]
        st.query_params.clear()
        for k, v in params.items():
            st.query_params[k] = v

def handle_google_login_callback():
    """Process the Google OAuth callback token from the URL."""
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
            st.success("Đăng nhập Google thành công!")
            st.rerun()
        except Exception as e:
            st.error(f"Đăng nhập Google thất bại: {e}")
            clear_google_query_params()

handle_google_login_callback()

# App Routing logic
if st.session_state["logged_in"]:
    user_id = st.session_state.get("user_id", "")

    # --- Sidebar ---
    st.sidebar.title("EnglishMate")
    st.sidebar.caption(f"ID: {user_id}")
    st.sidebar.divider()

    page = st.sidebar.radio("Danh mục", ["AI sửa ngữ pháp", "Kho Từ Vựng", "Flashcard"])

    # Vocab stats in sidebar
    st.sidebar.divider()
    st.sidebar.markdown("**Thống kê từ vựng**")
    try:
        res = requests.get(f"http://127.0.0.1:8000/vocab/list/{user_id}")
        if res.status_code == 200:
            vocab = res.json().get("vocab_list", [])
            learning = len([v for v in vocab if v.get("status") == "learning"])
            learned = len([v for v in vocab if v.get("status") == "learned"])
            difficult = len([v for v in vocab if v.get("status") == "difficult"])

            col1, col2, col3 = st.sidebar.columns(3)
            col1.metric("Đang học", learning)
            col2.metric("Đã học", learned)
            col3.metric("Từ khó", difficult)
        else:
            st.sidebar.write("Chưa có dữ liệu")
    except Exception:
        st.sidebar.write("Backend chưa khởi động")

    # Learning streak in sidebar
    st.sidebar.divider()
    st.sidebar.markdown("**Chuỗi ngày học tập**")
    try:
        act_res = requests.get(f"http://127.0.0.1:8000/chat/activity/{user_id}")
        if act_res.status_code == 200:
            activity = act_res.json().get("activity", {})
            dates = sorted(activity.keys(), reverse=True)

            # Calculate streak (consecutive days with activity > 0)
            streak = 0
            for date_str in dates:
                if activity[date_str] > 0:
                    streak += 1
                else:
                    break

            today_count = activity.get(dates[0], 0) if dates else 0

            # Streak display
            if streak >= 7:
                fire = "🔥🔥🔥"
                msg = "Tuyệt vời! Giữ vững phong độ!"
            elif streak >= 3:
                fire = "🔥🔥"
                msg = "Rất tốt! Cố lên nào!"
            elif streak >= 1:
                fire = "🔥"
                msg = "Khởi đầu tốt lắm!"
            else:
                fire = "❄️"
                msg = "Hãy bắt đầu học hôm nay!"

            st.sidebar.markdown(
                f"""
                <div style="text-align:center; padding:12px 0;">
                    <div style="font-size:2.5rem;">{fire}</div>
                    <div style="font-size:2rem; font-weight:bold; color:#fafafa;">{streak} ngày</div>
                    <div style="font-size:0.85rem; color:#8b949e; margin-top:4px;">{msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.sidebar.caption(f"Hôm nay: {today_count} hoạt động")
    except Exception:
        pass

    # Logout at the bottom
    st.sidebar.divider()
    if st.sidebar.button("Đăng xuất", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = ""
        st.rerun()

    # Page Switcher
    if page == "AI sửa ngữ pháp":
        show_chat_page()
    elif page == "Kho Từ Vựng":
        show_vocab_page()
    elif page == "Flashcard":
        show_flashcard_page()
else:
    show_auth_page()
