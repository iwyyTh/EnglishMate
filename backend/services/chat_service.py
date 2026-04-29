from backend.core.firebase_config import get_firestore_client
from backend.schemas.chat import ChatMessage
import datetime

def save_message(msg: ChatMessage):
    db = get_firestore_client()
    timestamp = datetime.datetime.now().isoformat()
    
    doc_ref = db.collection("users").document(msg.user_id).collection("messages").document(timestamp)
    
    doc_ref.set({
        "role": msg.role,
        "content": msg.content,
        "timestamp": timestamp
    })
    return True

def get_chat_history(user_id: str):
    db = get_firestore_client()
    
    docs = db.collection("users").document(user_id).collection("messages").order_by("timestamp").stream()
    
    history = []
    for doc in docs:
        history.append(doc.to_dict())
    return history
