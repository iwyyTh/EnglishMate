import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

def _update_status(user_id, word_id, new_status):
    """Send a status update request to the backend API.

    Args:
        user_id (str): The user's ID.
        word_id (str): The vocabulary document ID.
        new_status (str): The new status value.
    """
    requests.put(f"{API_BASE}/vocab/update-status", json={
        "user_id": user_id,
        "word_id": word_id,
        "status": new_status,
    })


def _render_vocab_card(item, user_id, available_actions):
    """Render a single vocabulary card with action buttons.

    Args:
        item (dict): The vocabulary data dictionary.
        user_id (str): The user's ID.
        available_actions (list[tuple]): List of (label, status_value) tuples for action buttons.
    """
    with st.container(border=True):
        col_text, col_actions = st.columns([3, 2])
        with col_text:
            st.markdown(f"**{item['word']}** — {item['meaning']}")
            if item.get("example"):
                st.caption(f"_Ex: {item['example']}_")
        with col_actions:
            btn_cols = st.columns(len(available_actions))
            for i, (label, target_status) in enumerate(available_actions):
                with btn_cols[i]:
                    if st.button(label, key=f"{target_status}_{item['id']}"):
                        _update_status(user_id, item["id"], target_status)
                        st.rerun()


def show_vocab_page():
    """Render the vocabulary management page.

    Provides a form for adding new words and organizes vocabulary into
    three categories: Learning, Learned, and Difficult.
    """
    st.title("Kho Lưu Từ Vựng")
    user_id = st.session_state.get("user_id")

    # --- ADD NEW VOCABULARY FORM ---
    with st.expander("Thêm từ vựng mới", expanded=False):
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
                    payload = {
                        "user_id": user_id,
                        "word": word,
                        "meaning": meaning,
                        "example": example,
                        "status": "learning",
                    }
                    res = requests.post(f"{API_BASE}/vocab/add", json=payload)
                    if res.status_code == 200:
                        st.success("Đã thêm từ vựng thành công!")
                        st.rerun()
                else:
                    st.error("Vui lòng điền đủ Từ vựng và Nghĩa!")

    st.divider()

    # --- FETCH ALL VOCABULARY ---
    response = requests.get(f"{API_BASE}/vocab/list/{user_id}")
    if response.status_code != 200:
        st.error("Không thể tải danh sách từ vựng.")
        return

    vocab_list = response.json().get("vocab_list", [])

    if len(vocab_list) == 0:
        st.info("Kho từ vựng đang trống. Hãy thêm từ mới để bắt đầu học!")
        return

    # Categorize words by status
    learning = [v for v in vocab_list if v.get("status") == "learning"]
    learned = [v for v in vocab_list if v.get("status") == "learned"]
    difficult = [v for v in vocab_list if v.get("status") == "difficult"]

    # --- TABBED DISPLAY ---
    tab_learning, tab_learned, tab_difficult = st.tabs([
        f"Đang học ({len(learning)})",
        f"Đã học ({len(learned)})",
        f"Từ khó ({len(difficult)})",
    ])

    with tab_learning:
        if not learning:
            st.info("Không có từ nào đang học.")
        for item in learning:
            _render_vocab_card(item, user_id, [
                ("Đã thuộc", "learned"),
                ("Đánh dấu khó", "difficult"),
            ])

    with tab_learned:
        if not learned:
            st.info("Chưa có từ nào được đánh dấu đã học.")
        for item in learned:
            _render_vocab_card(item, user_id, [
                ("Học lại", "learning"),
                ("Đánh dấu khó", "difficult"),
            ])

    with tab_difficult:
        if not difficult:
            st.info("Chưa có từ nào được đánh dấu là khó.")
        for item in difficult:
            _render_vocab_card(item, user_id, [
                ("Học lại", "learning"),
                ("Đã thuộc", "learned"),
            ])
