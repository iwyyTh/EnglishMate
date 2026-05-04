from pydantic import BaseModel

class ChatMessage(BaseModel):
    """Schema for a single chat message."""
    user_id: str
    role: str       # "user" or "assistant"
    content: str    # Message text content
