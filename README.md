# EnglishMate 🎓

EnglishMate là một ứng dụng trợ lý học tiếng Anh thông minh được xây dựng bằng Python. Dự án sử dụng mô hình AI của Google (Gemini) để giúp người dùng luyện tập tiếng Anh thông qua việc trò chuyện trực tiếp, sửa lỗi ngữ pháp và quản lý kho từ vựng cá nhân.

## ✨ Tính năng nổi bật

*   **Trò chuyện với AI (Chatbot):** Tương tác với "giáo viên tiếng Anh" AI (Gemini 1.5 Flash). Tự động sửa lỗi ngữ pháp và duy trì ngữ cảnh trò chuyện.
*   **Quản lý Từ vựng (Vocabulary):** Lưu trữ từ mới, định nghĩa, ví dụ và phân loại từ vựng vào hệ thống cơ sở dữ liệu.
*   **Hệ thống Xác thực (Authentication):**
    *   Đăng nhập / Đăng ký bằng Email và Mật khẩu (Firebase Auth).
    *   **Tích hợp Đăng nhập bằng Google (Google OAuth 2.0)** hiện đại, tiện lợi.
*   **Lưu trữ Đám mây:** Toàn bộ lịch sử trò chuyện và kho từ vựng được lưu trữ và đồng bộ hóa thời gian thực bằng Google Firebase (Cloud Firestore).

## 🛠️ Kiến trúc hệ thống

Dự án được chia thành 2 phần độc lập kết nối với nhau qua REST API:

1.  **Frontend (Giao diện người dùng):** Viết bằng [Streamlit](https://streamlit.io/), giúp xây dựng giao diện nhanh chóng, trực quan.
2.  **Backend (Máy chủ xử lý):** Viết bằng [FastAPI](https://fastapi.tiangolo.com/), tốc độ cao, xử lý logic nghiệp vụ, giao tiếp với Firebase và Google Gemini API.

```text
EnglishMate/
├── backend/                  # Mã nguồn FastAPI
│   ├── core/                 # Cấu hình Firebase & kết nối cơ bản
│   ├── routers/              # Các API Endpoints (auth, chat, vocab)
│   ├── schemas/              # Các Pydantic Models (định dạng dữ liệu)
│   ├── services/             # Logic nghiệp vụ (auth, chat, vocab service)
│   └── main.py               # File chạy server FastAPI
├── frontend/                 # Mã nguồn Streamlit
│   ├── views/                # Các trang giao diện (auth_view, chat_view, vocab_view)
│   └── app.py                # File khởi chạy giao diện
├── .streamlit/
│   └── secrets.toml          # Chứa CÁC MÃ BẢO MẬT (Không push lên Git)
└── README.md                 # File bạn đang đọc
```

## 🚀 Hướng dẫn Cài đặt & Chạy dự án

### 1. Cài đặt thư viện
Yêu cầu Python 3.9 trở lên. Mở Terminal và chạy lệnh:
```bash
pip install fastapi uvicorn streamlit pyrebase4 firebase-admin google-generativeai requests pydantic
```

### 2. Cấu hình Bảo mật (Môi trường)
Bạn cần tạo một file tên là `secrets.toml` bên trong thư mục `.streamlit/` (Nếu chưa có thì tự tạo thư mục này ở thư mục gốc).
Điền các thông tin sau vào file `secrets.toml`:

```toml
GEMINI_API_KEY = "MÃ_API_GEMINI_CỦA_BẠN"

[firebase_client]
apiKey = "WEB_API_KEY"
authDomain = "TEN_PROJECT.firebaseapp.com"
projectId = "TEN_PROJECT"
storageBucket = "TEN_PROJECT.firebasestorage.app"
messagingSenderId = "..."
appId = "..."

[firebase_admin]
type = "service_account"
project_id = "TEN_PROJECT"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "..."
universe_domain = "googleapis.com"

[google-login]
google-url = "http://127.0.0.1:8000/auth/google/start"
google_client_id = "CLIENT_ID_CỦA_BẠN.apps.googleusercontent.com"
google_client_secret = "CLIENT_SECRET_CỦA_BẠN"
google_redirect_uri = "http://127.0.0.1:8000/auth/google/callback"
firebase_web_api_key = "WEB_API_KEY"
frontend_url = "http://localhost:8501"
cookie_secure = false
```
*(Lưu ý: Các mã trên lấy từ Google Cloud Console, Firebase Console và Google AI Studio).*

### 3. Khởi chạy Ứng dụng

Bạn cần mở **2 cửa sổ Terminal (Command Prompt)** song song để chạy cả Backend và Frontend.

**Terminal 1: Chạy Server Backend (FastAPI)**
```bash
uvicorn backend.main:app --reload
```
*Server sẽ chạy ở địa chỉ: `http://127.0.0.1:8000`*

**Terminal 2: Chạy Giao diện Frontend (Streamlit)**
```bash
streamlit run frontend/app.py
```
*Trang web sẽ tự động mở lên tại địa chỉ: `http://localhost:8501`*

---
Được phát triển với ❤️ bằng Python.
