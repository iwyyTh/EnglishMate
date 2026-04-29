from fastapi import APIRouter
from backend.schemas.chat import ChatMessage
from backend.services.chat_service import save_message, get_chat_history

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/save")
def api_save_message(msg: ChatMessage):
    # Gọi bác thủ kho cất hộ tin nhắn
    save_message(msg)
    return {"message": "Đã lưu tin nhắn thành công"}

@router.get("/history/{user_id}")
def api_get_history(user_id: str):
    # Trả về toàn bộ lịch sử trò chuyện của user này
    history = get_chat_history(user_id)
    return {"history": history}
