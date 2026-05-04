import streamlit as st
import google.generativeai as genai
import requests

# --- AI CONFIGURATION ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
model_name = available_models[0] if available_models else "gemini-1.5-flash"
model = genai.GenerativeModel(model_name)

def show_chat_page():
    """Render the main chat interface.

    Handles user interaction with the Gemini AI, saving messages to Firestore,
    and displaying the chat history in separate tabs.
    """
    # --- TABS ---
    tab_chat, tab_save_word, tab_history = st.tabs(["New Chat", "Lưu từ nhanh", "Chat History"])
    
    # === TAB 1: CURRENT CHAT ===
    with tab_chat:
        # Initialize default greeting without loading full history
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hello! I am your English Mate. I will help you correct your English grammar!"}
            ]
            
        # Use a container to group messages above the chat input
        msg_container = st.container()
        
        with msg_container:
            for msg in st.session_state["messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                
        user_input = st.chat_input("Type a message in English...")
        if user_input:
            user_id = st.session_state["user_id"]
            
            # Save user message
            st.session_state["messages"].append({"role": "user", "content": user_input})
            requests.post("http://127.0.0.1:8000/chat/save", json={"user_id": user_id, "role": "user", "content": user_input})
            
            # Display new user message inside the container
            with msg_container:
                with st.chat_message("user"):
                    st.markdown(user_input)
                
            try:
                # Call AI
                prompt = f"Bạn là một giáo viên tiếng Anh nhiệt tình tên là EnglishMate. Hãy trả lời câu sau của học viên một cách thân thiện, sửa lỗi ngữ pháp (nếu có) và giữ độ dài ngắn gọn: '{user_input}'"
                response = model.generate_content(prompt)
                bot_reply = {"role": "assistant", "content": response.text}
                
                # Save AI message
                requests.post("http://127.0.0.1:8000/chat/save", json={"user_id": user_id, "role": "assistant", "content": bot_reply["content"]})
                st.session_state["messages"].append(bot_reply)
                
                with msg_container:
                    with st.chat_message("assistant"):
                        st.markdown(bot_reply["content"])
                    
            except Exception as e:
                st.error("The AI teacher is busy right now! Please wait 10 seconds and try again.")

    # === TAB 2: QUICK SAVE WORD ===
    with tab_save_word:
        st.subheader("Lưu từ vựng nhanh")
        st.caption("Gõ từ tiếng Anh bạn muốn lưu, AI sẽ tự động tra nghĩa cho bạn.")

        word_input = st.text_input("Nhập từ tiếng Anh:", key="quick_word_input")

        if st.button("Tra nghĩa", key="lookup_btn"):
            if word_input.strip():
                with st.spinner("Đang tra từ..."):
                    try:
                        lookup_prompt = (
                            f"Hãy cho tôi nghĩa tiếng Việt ngắn gọn (tối đa 10 từ) và "
                            f"1 câu ví dụ tiếng Anh đơn giản cho từ '{word_input.strip()}'. "
                            f"Trả lời theo đúng format sau, không thêm gì khác:\n"
                            f"Nghĩa: <nghĩa tiếng Việt>\n"
                            f"Ví dụ: <câu ví dụ tiếng Anh>"
                        )
                        result = model.generate_content(lookup_prompt)
                        reply = result.text.strip()

                        # Parse response
                        meaning = ""
                        example = ""
                        for line in reply.split("\n"):
                            line = line.strip()
                            if line.lower().startswith("nghĩa:"):
                                meaning = line.split(":", 1)[1].strip()
                            elif line.lower().startswith("ví dụ:"):
                                example = line.split(":", 1)[1].strip()

                        st.session_state["lookup_word"] = word_input.strip()
                        st.session_state["lookup_meaning"] = meaning
                        st.session_state["lookup_example"] = example
                    except Exception:
                        st.error("Không thể tra từ lúc này. Vui lòng thử lại.")
            else:
                st.warning("Vui lòng nhập một từ tiếng Anh.")

        # Show lookup result and save button
        if st.session_state.get("lookup_word"):
            st.divider()
            st.markdown(f"**Từ:** {st.session_state['lookup_word']}")
            
            meaning_edit = st.text_input(
                "Nghĩa:", 
                value=st.session_state.get("lookup_meaning", ""),
                key="meaning_edit",
            )
            example_edit = st.text_input(
                "Ví dụ:", 
                value=st.session_state.get("lookup_example", ""),
                key="example_edit",
            )

            if st.button("Lưu vào Kho Từ Vựng", type="primary", key="save_word_btn"):
                user_id = st.session_state["user_id"]
                payload = {
                    "user_id": user_id,
                    "word": st.session_state["lookup_word"],
                    "meaning": meaning_edit,
                    "example": example_edit,
                    "status": "learning",
                }
                res = requests.post("http://127.0.0.1:8000/vocab/add", json=payload)
                if res.status_code == 200:
                    st.success(f"Đã lưu '{st.session_state['lookup_word']}' vào kho từ vựng!")
                    # Clear lookup state
                    del st.session_state["lookup_word"]
                    del st.session_state["lookup_meaning"]
                    del st.session_state["lookup_example"]
                else:
                    st.error("Không thể lưu từ. Vui lòng thử lại.")

    # === TAB 3: CHAT HISTORY ===
    with tab_history:
        st.subheader("Firestore Chat Archive")
        if st.button("Load Chat History"):
            # Fetch previous messages from the backend
            user_id = st.session_state["user_id"]
            response = requests.get(f"http://127.0.0.1:8000/chat/history/{user_id}")
            
            if response.status_code == 200:
                history = response.json().get("history", [])
                if len(history) == 0:
                    st.info("No chat history available.")
                else:
                    for msg in history:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])
