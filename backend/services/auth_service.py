from backend.core.firebase_config import get_auth_client, get_firestore_client
from backend.schemas.auth import LoginRequest, SignupRequest
from datetime import datetime

def login(email, password):
    """Authenticate a user using their email and password.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict | str: The user data if successful, or an error string if failed.
    """
    try:
        auth = get_auth_client()
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        return str(e)

def register(email, password):
    """Register a new user and initialize their profile in Firestore.

    Args:
        email (str): The user's email address.
        password (str): The user's chosen password.

    Returns:
        dict | str: The user data if successful, or an error string if failed.
    """
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
    """Verify Google token and create user in Firestore if not exists.

    Args:
        id_token (str): The Google ID token.

    Returns:
        dict | str: A dict with localId and email, or an error string if failed.
    """
    try:
        # Ensure firebase_admin is initialized
        db = get_firestore_client()
        
        # Verify the id_token returned by Google
        decoded_token = admin_auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        email = decoded_token.get('email', '')
        
        # Check if user exists in Firestore, if not, create a new profile
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
