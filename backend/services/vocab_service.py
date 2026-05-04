from backend.core.firebase_config import get_firestore_client
from backend.schemas.vocab import VocabCreate
import datetime

def add_vocab(vocab : VocabCreate):
    db = get_firestore_client()
    timestamp = datetime.datetime.now().isoformat()

    word_id = vocab.word.lower().strip()

    doc_ref = db.collection("users").document(vocab.user_id).collection("vocabulary").document(word_id)

    doc_ref.set({
        "word" : vocab.word,
        "meaning" : vocab.meaning,
        "example" : vocab.example,
        "status" : vocab.status,
        "created_at" : timestamp
    })
    return True

def get_vocab_list(user_id : str):
    db = get_firestore_client()
    # Lấy danh sách từ vựng, xếp theo thời gian mới nhất lên đầu (DESCENDING)
    docs = db.collection("users").document(user_id).collection("vocabulary").order_by("created_at", direction="DESCENDING").stream()
    
    vocab_list = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        vocab_list.append(data)
    return vocab_list
