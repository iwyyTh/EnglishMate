from pydantic import BaseModel

class ChatMessage(BaseModel):
    user_id: str
    role: str       # Sẽ chứa chữ "user" hoặc "assistant"
    content: str    # Nội dung tin nhắn
