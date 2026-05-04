import streamlit as st
import google.generativeai as genai
import requests

# --- CẤU HÌNH BỘ NÃO AI ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
model_name = available_models[0] if available_models else "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

def show_chat_page():
    # --- PHẦN HEADER ---
    st.title("Trang Chủ (Dashboard) 🏠")
    st.write(f"Đang đăng nhập bằng ID: {st.session_state.get('user_id', '')}")
    
    logout_btn = st.button("Đăng xuất")
    if logout_btn:
        st.session_state["logged_in"] = False
        st.session_state["user_id"] = ""
        st.rerun()

    st.divider()
    
    # --- CHIA 2 TABS ---
    tab_chat, tab_history = st.tabs(["💬 Trò chuyện mới", "🕰️ Lịch sử học tập"])
    
    # === TAB 1: TRÒ CHUYỆN HIỆN TẠI ===
    with tab_chat:
        # Chỉ tạo 1 câu chào trên RAM, KHÔNG tải lịch sử cũ
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hello! I am your English Mate. Let's practice!"}
            ]
            
        # Dùng container để nhóm toàn bộ tin nhắn lại phía trên thanh chat
        msg_container = st.container()
        
        with msg_container:
            for msg in st.session_state["messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                
        user_input = st.chat_input("Nhập tin nhắn bằng tiếng Anh...")
        if user_input:
            user_id = st.session_state["user_id"]
            
            # Lưu tin user
            st.session_state["messages"].append({"role": "user", "content": user_input})
            requests.post("http://127.0.0.1:8000/chat/save", json={"user_id": user_id, "role": "user", "content": user_input})
            
            # Hiển thị tin nhắn mới ngay trong container phía trên
            with msg_container:
                with st.chat_message("user"):
                    st.markdown(user_input)
                
            try:
                # Gọi AI
                prompt = f"Bạn là một giáo viên tiếng Anh nhiệt tình tên là EnglishMate. Hãy trả lời câu sau của học viên một cách thân thiện, sửa lỗi ngữ pháp (nếu có) và giữ độ dài ngắn gọn: '{user_input}'"
                response = model.generate_content(prompt)
                bot_reply = {"role": "assistant", "content": response.text}
                
                # Lưu tin AI
                requests.post("http://127.0.0.1:8000/chat/save", json={"user_id": user_id, "role": "assistant", "content": bot_reply["content"]})
                st.session_state["messages"].append(bot_reply)
                
                with msg_container:
                    with st.chat_message("assistant"):
                        st.markdown(bot_reply["content"])
                    
            except Exception as e:
                st.error("Thầy giáo AI đang bận uống nước (Quá tải)! Bạn vui lòng đợi khoảng 10 giây rồi thử lại.")

    # === TAB 2: XEM LẠI LỊCH SỬ ===
    with tab_history:
        st.subheader("Kho lưu trữ tin nhắn Firestore")
        if st.button("Tải lịch sử chat"):
            # Khi người dùng bấm nút mới gọi API lấy dữ liệu cũ
            user_id = st.session_state["user_id"]
            response = requests.get(f"http://127.0.0.1:8000/chat/history/{user_id}")
            
            if response.status_code == 200:
                history = response.json().get("history", [])
                if len(history) == 0:
                    st.info("Chưa có lịch sử trò chuyện nào.")
                else:
                    for msg in history:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])
