import streamlit as st
import requests

def show_vocab_page():
    st.title("📚 Kho Lưu Từ Vựng")
    user_id = st.session_state.get("user_id")

    # --- PHẦN 1: FORM THÊM TỪ MỚI ---
    # st.expander giúp tạo một cái hộp có thể đóng/mở được cho gọn
    with st.expander("➕ Thêm từ vựng mới", expanded=True):
        # st.form giúp gom nhóm các ô nhập liệu lại, bấm nút mới gửi đi 1 thể
        with st.form("add_vocab_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                word = st.text_input("Từ vựng (Tiếng Anh)*")
            with col2:
                meaning = st.text_input("Nghĩa (Tiếng Việt)*")
            
            example = st.text_input("Câu ví dụ (Không bắt buộc)")
            
            submit = st.form_submit_button("Lưu từ vựng")
            
            if submit:
                if word and meaning:
                    # Gói hàng dữ liệu
                    payload = {
                        "user_id": user_id,
                        "word": word,
                        "meaning": meaning,
                        "example": example,
                        "status": "learning"
                    }
                    # Bắn lên API Backend
                    res = requests.post("http://127.0.0.1:8000/vocab/add", json=payload)
                    if res.status_code == 200:
                        st.success("Đã thêm từ vựng thành công! Tải lại trang để xem nhé.")
                else:
                    st.error("Vui lòng điền đủ Từ vựng và Nghĩa!")

    st.divider()

    # --- PHẦN 2: BẢNG DANH SÁCH TỪ VỰNG ---
    st.subheader("📖 Danh sách từ đang học")
    
    # Hút dữ liệu từ API về
    response = requests.get(f"http://127.0.0.1:8000/vocab/list/{user_id}")
    if response.status_code == 200:
        vocab_list = response.json().get("vocab_list", [])
        
        if len(vocab_list) == 0:
            st.info("Kho từ vựng đang trống. Hãy học chăm chỉ và lưu thêm từ nhé!")
        else:
            # Vẽ từng từ vựng ra màn hình
            for item in vocab_list:
                with st.container(border=True): # Vẽ cái khung viền cho đẹp
                    colA, colB = st.columns([3, 1])
                    with colA:
                        st.markdown(f"**{item['word']}** : {item['meaning']}")
                        if item.get("example"):
                            st.caption(f"Ví dụ: *{item['example']}*")
                    with colB:
                        st.button("Đang học 🔄", key=item["id"], disabled=True)
