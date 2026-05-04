import streamlit as st
import requests
import random

API_BASE = "http://127.0.0.1:8000"


def show_flashcard_page():
    """Render the flashcard practice page.

    Fetches the user's vocabulary and displays words one at a time
    as interactive flashcards. Users can flip to reveal the meaning,
    navigate between cards, and shuffle the deck.
    """
    st.title("Flashcard")
    user_id = st.session_state.get("user_id")

    # Fetch vocabulary from backend
    response = requests.get(f"{API_BASE}/vocab/list/{user_id}")
    if response.status_code != 200:
        st.error("Không thể tải danh sách từ vựng.")
        return

    vocab_list = response.json().get("vocab_list", [])

    if len(vocab_list) == 0:
        st.info("Kho từ vựng đang trống. Hãy thêm từ mới trước khi luyện tập!")
        return

    # --- Filter options ---
    filter_option = st.radio(
        "Chọn nhóm từ muốn ôn tập:",
        ["Tất cả", "Đang học", "Từ khó", "Đã học"],
        horizontal=True,
    )

    status_map = {
        "Tất cả": None,
        "Đang học": "learning",
        "Từ khó": "difficult",
        "Đã học": "learned",
    }
    target_status = status_map[filter_option]

    if target_status:
        cards = [v for v in vocab_list if v.get("status") == target_status]
    else:
        cards = vocab_list

    if len(cards) == 0:
        st.info(f"Không có từ nào trong nhóm '{filter_option}'.")
        return

    # --- Initialize session state ---
    if "fc_index" not in st.session_state:
        st.session_state["fc_index"] = 0
    if "fc_flipped" not in st.session_state:
        st.session_state["fc_flipped"] = False

    # Clamp index to valid range
    idx = st.session_state["fc_index"] % len(cards)
    current = cards[idx]

    # --- Progress ---
    st.progress((idx + 1) / len(cards), text=f"Từ {idx + 1} / {len(cards)}")

    # --- Flashcard display ---
    st.markdown(
        """
        <style>
        .flashcard {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px;
            padding: 60px 40px;
            text-align: center;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        .flashcard h1 {
            font-size: 2.5rem;
            margin: 0;
            color: white;
        }
        .flashcard p {
            font-size: 1.3rem;
            margin-top: 12px;
            opacity: 0.9;
        }
        .flashcard .hint {
            font-size: 0.9rem;
            opacity: 0.6;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["fc_flipped"]:
        # Show meaning side
        example_html = f"<p><em>Ex: {current['example']}</em></p>" if current.get("example") else ""
        st.markdown(
            f"""
            <div class="flashcard">
                <h1>{current['meaning']}</h1>
                <p>{current['word']}</p>
                {example_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Show word side
        st.markdown(
            f"""
            <div class="flashcard">
                <h1>{current['word']}</h1>
                <p class="hint">Nhấn "Lật thẻ" để xem nghĩa</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- Control buttons ---
    col_prev, col_flip, col_next, col_shuffle = st.columns(4)

    with col_prev:
        if st.button("Trước", use_container_width=True, disabled=(idx == 0)):
            st.session_state["fc_index"] = idx - 1
            st.session_state["fc_flipped"] = False
            st.rerun()

    with col_flip:
        flip_label = "Lật lại" if st.session_state["fc_flipped"] else "Lật thẻ"
        if st.button(flip_label, use_container_width=True, type="primary"):
            st.session_state["fc_flipped"] = not st.session_state["fc_flipped"]
            st.rerun()

    with col_next:
        if st.button("Tiếp", use_container_width=True, disabled=(idx >= len(cards) - 1)):
            st.session_state["fc_index"] = idx + 1
            st.session_state["fc_flipped"] = False
            st.rerun()

    with col_shuffle:
        if st.button("Trộn bài", use_container_width=True):
            random.shuffle(cards)
            st.session_state["fc_index"] = 0
            st.session_state["fc_flipped"] = False
            st.rerun()
