from backend.core.firebase_config import get_firestore_client
from backend.schemas.vocab import VocabCreate
import datetime

def add_vocab(vocab: VocabCreate):
    """Add a new vocabulary word to the user's Firestore collection.

    Args:
        vocab (VocabCreate): The vocabulary data model.

    Returns:
        bool: True if the word was successfully added.
    """
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

def get_vocab_list(user_id: str):
    """Retrieve the user's vocabulary list, ordered by newest first.

    Args:
        user_id (str): The user's ID.

    Returns:
        list[dict]: A list of vocabulary dictionaries.
    """
    db = get_firestore_client()
    # Fetch vocabulary list, ordered by creation time (DESCENDING)
    docs = db.collection("users").document(user_id).collection("vocabulary").order_by("created_at", direction="DESCENDING").stream()
    
    vocab_list = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        vocab_list.append(data)
    return vocab_list
