from backend.core.firebase_config import get_firestore_client
from backend.schemas.chat import ChatMessage
import datetime
from firebase_admin import firestore

def save_message(msg: ChatMessage):
    """Save a chat message to Firestore.

    Args:
        msg (ChatMessage): The message to save.

    Returns:
        bool: True if successful.
    """
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
    """Retrieve the most recent chat messages for a user.

    Args:
        user_id (str): The user's ID.
        limit (int, optional): The maximum number of messages. Defaults to 8.

    Returns:
        list[dict]: A list of message dictionaries.
    """
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


def get_learning_activity(user_id: str, days: int = 28):
    """Count daily learning activities for the past N days.

    Counts both chat messages and vocabulary additions per day
    to build a GitHub-style activity heatmap.

    Args:
        user_id (str): The user's ID.
        days (int, optional): Number of past days to check. Defaults to 28.

    Returns:
        dict: A dict mapping date strings (YYYY-MM-DD) to activity counts.
    """
    db = get_firestore_client()
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days - 1)

    # Initialize all days with 0
    activity = {}
    for i in range(days):
        d = start_date + datetime.timedelta(days=i)
        activity[d.isoformat()] = 0

    # Count messages
    msgs = db.collection("users").document(user_id).collection("messages").stream()
    for doc in msgs:
        ts = doc.to_dict().get("timestamp", "")
        if ts:
            date_str = ts[:10]  # Extract YYYY-MM-DD
            if date_str in activity:
                activity[date_str] += 1

    # Count vocabulary additions
    vocabs = db.collection("users").document(user_id).collection("vocabulary").stream()
    for doc in vocabs:
        ts = doc.to_dict().get("created_at", "")
        if ts:
            date_str = ts[:10]
            if date_str in activity:
                activity[date_str] += 1

    return activity
