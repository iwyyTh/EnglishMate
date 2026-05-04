from fastapi import APIRouter
from backend.schemas.vocab import VocabCreate
from backend.services.vocab_service import add_vocab, get_vocab_list

router = APIRouter(prefix="/vocab", tags=["vocabulary"])

@router.post("/add")
def api_add_vocab(request: VocabCreate):
    add_vocab(request)
    return {"message" : "add vocabulary successfully"}

@router.get("/list/{user_id}")
def api_get_vocab_list(user_id : str):
    vocab_list = get_vocab_list(user_id)
    return {"vocab_list" : vocab_list}