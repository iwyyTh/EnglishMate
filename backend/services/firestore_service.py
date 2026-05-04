from backend.core.firebase_config import get_firestore_client
from backend.schemas.chat import ChatMessage
import datetime
from firebase_admin import firestore

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

def get_chat_history(user_id: str, limit: int = 8):
    db = get_firestore_client()
    
    q = (
        db.collection("users")
        .document(user_id)
        .collection("messages")
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    
    docs = list(q.stream())
    docs.reverse()
    
    history = []
    for doc in docs:
        d = doc.to_dict()
        history.append({
            "role": d.get("role", "assistant"),
            "content": d.get("content", ""),
            "timestamp": d.get("timestamp", "")
        })
    return history
