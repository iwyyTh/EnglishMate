import streamlit as st
import requests
def show_auth_page():
    st.title("Chào mừng đến với EnglishMate 🚀")

    tab_login, tab_signup = st.tabs(["Đăng nhập", "Đăng ký"])
    
    # Tạo 2 tab trên giao diện

    # --- GIAO DIỆN ĐĂNG KÝ ---
    with tab_signup:
        st.subheader("Tạo tài khoản mới")
        
        # Tạo một Form để người dùng nhập liệu
        with st.form("signup_form"):
            new_email = st.text_input("Email của bạn")
            new_password = st.text_input("Mật khẩu", type="password")
            submit_btn = st.form_submit_button("Đăng ký ngay")
            
            if submit_btn:
                # Người dùng vừa bấm nút! Gói hàng (data) lại để gửi đi:
                payload = {
                    "email": new_email,
                    "password": new_password
                }
                
                # CHỖ TRỐNG 1: Điền URL API đăng ký của Backend (nhớ lại bài test Swagger UI lúc nãy)
                # Gợi ý: URL kết thúc bằng /auth/register
                api_url = "http://127.0.0.1:8000/auth/register"  
                
                try:
                    # CHỖ TRỐNG 2: Dùng thư viện requests để gửi gói hàng bằng phương thức POST
                    # Gợi ý: requests.post(url, json=gói_hàng)
                    response = requests.post(api_url, json=payload)
                    
                    # CHỖ TRỐNG 3: Kiểm tra xem server có trả về mã 200 (Thành công) hay không?
                    if response.status_code == 200:  
                        st.success("Tạo tài khoản thành công! Hãy chuyển sang tab Đăng nhập.")
                    else:
                        # Nếu lỗi (ví dụ 400), lấy chi tiết lỗi từ server in ra màn hình
                        error_msg = response.json().get("detail", "Lỗi không xác định")
                        st.error(f"Đăng ký thất bại: {error_msg}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Không thể kết nối đến máy chủ Backend. Bạn đã chạy uvicorn chưa?")


    # --- GIAO DIỆN ĐĂNG NHẬP ---
    with tab_login:
        st.subheader("Đăng nhập")
        
        with st.form("login_form"):
            login_email = st.text_input("Email")
            login_password = st.text_input("Mật khẩu", type="password")
            login_btn = st.form_submit_button("Đăng nhập")
            
            if login_btn:
                payload = {
                    "email": login_email,
                    "password": login_password
                }
                
                # CHỖ TRỐNG 1: Điền URL API đăng nhập
                api_url = "http://127.0.0.1:8000/auth/login" 
                
                try:
                    # CHỖ TRỐNG 2: Gửi request POST
                    response = requests.post(api_url, json=payload)  
                    
                    if response.status_code == 200:
                        # Lấy dữ liệu server trả về (có chứa user_id)
                        data = response.json()
                        
                        # CẤT VÀO TÚI THẦN KỲ (Session State)
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = data.get("user_id")
                        
                        st.success("Đăng nhập thành công! 🎉")
                        st.write(f"ID của bạn là: {st.session_state['user_id']}")
                        st.rerun()
                    else:
                        error_msg = response.json().get("detail", "Lỗi không xác định")
                        st.error(f"Đăng nhập thất bại: {error_msg}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("Không thể kết nối đến máy chủ Backend.")
        # ⚠️ QUAN TRỌNG: Bạn hãy copy TOÀN BỘ phần code tab_login và tab_signup 
        # của bạn lúc nãy dán vào đây. 
        # MẸO: Nhớ bôi đen toàn bộ code cũ rồi ấn phím `Tab` một cái để thụt nó lùi vào trong khối `else:` nhé!

        st.write("---")
        try:
            google_cfg = st.secrets["google-login"]
            google_login_url = google_cfg.get("google-url", "")
            if google_login_url:
                st.markdown(
                    f"""
                    <a href="{google_login_url}" target="_self" style="
                        display: inline-block;
                        padding: 0.5em 1em;
                        color: #000;
                        background-color: #fff;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        text-decoration: none;
                        font-weight: bold;
                        text-align: center;
                        width: 100%;
                    ">
                        🌐 Đăng nhập với Google
                    </a>
                    """,
                    unsafe_allow_html=True
                )
        except Exception:
            st.info("💡 Chưa cấu hình Google Login. Vui lòng thêm vào `.streamlit/secrets.toml` để sử dụng tính năng này.")

    