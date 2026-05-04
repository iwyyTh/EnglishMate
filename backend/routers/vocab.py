from fastapi import APIRouter
from backend.schemas.vocab import VocabCreate
from backend.services.vocab_service import add_vocab, get_vocab_list

router = APIRouter(prefix="/vocab", tags=["vocabulary"])

@router.post("/add")
def api_add_vocab(request: VocabCreate):
    """Add a new vocabulary word for a user.

    Args:
        request (VocabCreate): The vocabulary details including user_id, word, meaning, etc.

    Returns:
        dict: A success message.
    """
    add_vocab(request)
    return {"message": "Add vocabulary successfully"}

@router.get("/list/{user_id}")
def api_get_vocab_list(user_id: str):
    """Retrieve the vocabulary list for a specific user.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        dict: A dictionary containing the list of vocabulary words.
    """
    vocab_list = get_vocab_list(user_id)
    return {"vocab_list": vocab_list}