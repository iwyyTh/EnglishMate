from fastapi import APIRouter, HTTPException
from backend.schemas.vocab import VocabCreate, VocabUpdateStatus
from backend.services.vocab_service import add_vocab, get_vocab_list, update_vocab_status

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

@router.put("/update-status")
def api_update_vocab_status(request: VocabUpdateStatus):
    """Update the learning status of a vocabulary word.

    Args:
        request (VocabUpdateStatus): Contains user_id, word_id, and new status.

    Returns:
        dict: A success message.

    Raises:
        HTTPException: If the word is not found or the update fails.
    """
    try:
        update_vocab_status(request.user_id, request.word_id, request.status)
        return {"message": "Status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))