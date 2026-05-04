from pydantic import BaseModel
from typing import Optional

class VocabCreate(BaseModel):
    """Schema for creating a new vocabulary entry."""
    user_id: str
    word: str
    meaning: str
    example: Optional[str] = ""         
    status: Optional[str] = "learning"

class VocabUpdateStatus(BaseModel):
    """Schema for updating a vocabulary word's status."""
    user_id: str
    word_id: str
    status: str  # "learning", "learned", or "difficult"
