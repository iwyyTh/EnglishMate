from fastapi import APIRouter
from backend.schemas.chat import ChatMessage
from backend.services.firestore_service import save_message, get_chat_history, get_learning_activity

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/save")
def api_save_message(msg: ChatMessage):
    """Save a user or AI message to the database.

    Args:
        msg (ChatMessage): The message object containing user_id, role, and content.

    Returns:
        dict: A success message.
    """
    save_message(msg)
    return {"message": "Đã lưu tin nhắn thành công"}

@router.get("/history/{user_id}")
def api_get_history(user_id: str, limit: int = 8):
    """Retrieve recent chat history for a user.

    Args:
        user_id (str): The unique identifier of the user.
        limit (int, optional): Maximum number of messages to return. Defaults to 8.

    Returns:
        dict: A dictionary containing the list of recent messages.
    """
    history = get_chat_history(user_id, limit)
    return {"history": history}

@router.get("/activity/{user_id}")
def api_get_activity(user_id: str):
    """Retrieve daily learning activity for the heatmap.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        dict: A dictionary mapping dates to activity counts.
    """
    activity = get_learning_activity(user_id)
    return {"activity": activity}
