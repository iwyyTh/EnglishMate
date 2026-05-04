from pydantic import BaseModel
from typing import Optional

class VocabCreate(BaseModel):
    user_id: str
    word: str
    meaning: str
    example: Optional[str] = ""         
    status: Optional[str] = "learning"  
