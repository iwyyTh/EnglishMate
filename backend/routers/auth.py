from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from backend.schemas.auth import SignupRequest, LoginRequest, GoogleLoginRequest
from backend.services.auth_service import login as auth_login, register as auth_register, google_login as auth_google_login
import secrets
from urllib.parse import urlencode
import requests
import streamlit as st

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def api_register(mess : SignupRequest):
    user = auth_register(mess.email, mess.password)

    if isinstance(user, str):
        raise HTTPException(status_code=400, detail=user)
    return {"message": "Tạo tài khoản thành công", "user_id" : user.get("localId")}

@router.post("/login")
def api_login(mess : LoginRequest):
    user = auth_login(mess.email, mess.password)

    if isinstance(user, str):
        raise HTTPException(status_code=400, detail=user)
    return {"message": "Đăng nhập thành công", "user_id" : user.get("localId")}

try:
    google_cfg = st.secrets["google-login"]
    GOOGLE_CLIENT_ID = google_cfg["google_client_id"]
    GOOGLE_CLIENT_SECRET = google_cfg["google_client_secret"]
    GOOGLE_REDIRECT_URI = google_cfg["google_redirect_uri"]
    FIREBASE_WEB_API_KEY = google_cfg["firebase_web_api_key"]
    FRONTEND_URL = google_cfg["frontend_url"]
    COOKIE_SECURE = google_cfg["cookie_secure"]
except Exception:
    # Tránh lỗi sập server nếu chưa config
    GOOGLE_CLIENT_ID = None

@router.post("/google")
def api_google_login(payload: GoogleLoginRequest):
    user = auth_google_login(payload.id_token)
    if isinstance(user, str):
        raise HTTPException(status_code=401, detail=f"Google token invalid: {user}")
    return {"message": "Đăng nhập Google thành công", "user_id": user.get("localId")}

@router.get("/google/start")
def google_start():
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Chưa cấu hình Google Login")
        
    state = secrets.token_urlsafe(32)

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account",
    }

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urlencode(params)
    )

    response = RedirectResponse(url=google_auth_url, status_code=302)
    response.set_cookie(
        key="google_oauth_state",
        value=state,
        max_age=600,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
    )
    return response

@router.get("/google/callback")
def google_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
):
    if error:
        raise HTTPException(status_code=400, detail=f"Google OAuth error: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    saved_state = request.cookies.get("google_oauth_state")
    if not saved_state or not state or saved_state != state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=20,
    )

    if not token_resp.ok:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to exchange Google code: {token_resp.text}"
        )

    token_data = token_resp.json()
    google_id_token = token_data.get("id_token")

    if not google_id_token:
        raise HTTPException(status_code=400, detail="Google did not return id_token")

    firebase_resp = requests.post(
        f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_WEB_API_KEY}",
        json={
            "postBody": urlencode({
                "id_token": google_id_token,
                "providerId": "google.com",
            }),
            "requestUri": GOOGLE_REDIRECT_URI,
            "returnIdpCredential": True,
            "returnSecureToken": True,
        },
        timeout=20,
    )

    if not firebase_resp.ok:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to sign in with Firebase Google provider: {firebase_resp.text}"
        )

    firebase_data = firebase_resp.json()
    firebase_id_token = firebase_data.get("idToken")

    if not firebase_id_token:
        raise HTTPException(status_code=400, detail="Firebase did not return idToken")

    separator = "&" if "?" in FRONTEND_URL else "?"
    redirect_to_frontend = f"{FRONTEND_URL}{separator}{urlencode({'id_token': firebase_id_token})}"

    response = RedirectResponse(url=redirect_to_frontend, status_code=302)
    response.delete_cookie("google_oauth_state", path="/")
    return response
