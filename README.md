# EnglishMate

EnglishMate là ứng dụng trợ lý học tiếng Anh thông minh. Sử dụng AI (Google Gemini) để sửa ngữ pháp, tra từ tự động và quản lý kho từ vựng cá nhân.

## Tính năng

- **AI sửa ngữ pháp** — Chat với AI, tự động sửa lỗi ngữ pháp tiếng Anh.
- **Lưu từ nhanh** — Gõ từ lạ, AI tự tra nghĩa + ví dụ, lưu 1 click.
- **Kho Từ Vựng** — Phân loại 3 nhóm: Đang học / Đã học / Từ khó. Chuyển trạng thái linh hoạt.
- **Flashcard** — Ôn tập từ vựng bằng thẻ lật, lọc theo nhóm, trộn bài ngẫu nhiên.
- **Streak học tập** — Theo dõi chuỗi ngày học liên tục trên sidebar.
- **Thống kê từ vựng** — Hiển thị số từ đang học, đã học, từ khó trên sidebar.
- **Xác thực** — Đăng nhập Email/Password hoặc Google OAuth 2.0 (Firebase Auth).
- **Lưu trữ đám mây** — Dữ liệu đồng bộ qua Google Firestore.

## Kiến trúc

```
Frontend (Streamlit)  ←→  Backend (FastAPI)  ←→  Firebase / Gemini AI
```

```text
EnglishMate/
├── backend/
│   ├── core/                 # Cấu hình Firebase
│   ├── routers/              # API Endpoints (auth, chat, vocab)
│   ├── schemas/              # Pydantic Models
│   ├── services/             # Business logic
│   └── main.py
├── frontend/
│   ├── views/                # UI pages (auth, chat, vocab, flashcard)
│   └── app.py
├── .streamlit/
│   ├── config.toml           # Theme configuration
│   └── secrets.toml          # API keys (không push lên Git)
├── requirements.txt
└── README.md
```

## Cài đặt

**Yêu cầu:** Python 3.9+

```bash
pip install -r requirements.txt
```

## Cấu hình

Tạo file `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

[firebase_client]
apiKey = "..."
authDomain = "PROJECT.firebaseapp.com"
projectId = "PROJECT"
storageBucket = "PROJECT.firebasestorage.app"
messagingSenderId = "..."
appId = "..."

[firebase_admin]
type = "service_account"
project_id = "PROJECT"
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
google_client_id = "YOUR_CLIENT_ID.apps.googleusercontent.com"
google_client_secret = "YOUR_CLIENT_SECRET"
google_redirect_uri = "http://127.0.0.1:8000/auth/google/callback"
firebase_web_api_key = "YOUR_WEB_API_KEY"
frontend_url = "http://localhost:8501"
cookie_secure = false
```

> Lấy các mã này từ: [Google AI Studio](https://aistudio.google.com/), [Firebase Console](https://console.firebase.google.com/), [Google Cloud Console](https://console.cloud.google.com/).

## Chạy ứng dụng

Mở **2 terminal** song song:

```bash
# Terminal 1 — Backend
uvicorn backend.main:app --reload
```

```bash
# Terminal 2 — Frontend
streamlit run frontend/app.py
```

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:8501`
- API Docs: `http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/auth/register` | Đăng ký tài khoản |
| POST | `/auth/login` | Đăng nhập |
| POST | `/auth/google` | Đăng nhập Google |
| GET | `/auth/google/start` | Khởi tạo OAuth flow |
| GET | `/auth/google/callback` | Xử lý OAuth callback |
| POST | `/chat/save` | Lưu tin nhắn |
| GET | `/chat/history/{user_id}` | Lấy lịch sử chat |
| GET | `/chat/activity/{user_id}` | Lấy dữ liệu hoạt động |
| POST | `/vocab/add` | Thêm từ vựng |
| GET | `/vocab/list/{user_id}` | Lấy danh sách từ |
| PUT | `/vocab/update-status` | Cập nhật trạng thái từ |

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** Google Firestore
- **AI:** Google Gemini 1.5 Flash
- **Auth:** Firebase Authentication + Google OAuth 2.0
