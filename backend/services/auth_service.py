from backend.core.firebase_config import get_auth_client, get_firestore_client
from backend.schemas.auth import LoginRequest, SignupRequest
from datetime import datetime

def login(email, password):
    try:
        auth = get_auth_client()
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        return str(e)

def register(email, password):
    try:
        auth = get_auth_client()
        user = auth.create_user_with_email_and_password(email, password)

        db = get_firestore_client()
        user_id = user['localId']
        user_data = {
            "email": email,
            "created_at": datetime.now().isoformat(),
            "vocabulary_count": 0,
            "level": "Beginner"
        }
        db.collection("users").document(user_id).set(user_data)
        
        return user
    except Exception as e:
        return str(e)

from firebase_admin import auth as admin_auth

def google_login(id_token):
    try:
        # Đảm bảo firebase_admin đã được khởi tạo
        db = get_firestore_client()
        
        # Xác thực id_token do Google trả về
        decoded_token = admin_auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        email = decoded_token.get('email', '')
        
        # Kiểm tra xem user đã có trong Firestore chưa, nếu chưa thì tạo mới
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            user_data = {
                "email": email,
                "created_at": datetime.now().isoformat(),
                "vocabulary_count": 0,
                "level": "Beginner",
                "auth_provider": "google"
            }
            db.collection("users").document(user_id).set(user_data)
            
        return {"localId": user_id, "email": email}
    except Exception as e:
        return str(e)
