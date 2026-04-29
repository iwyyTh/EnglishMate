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

