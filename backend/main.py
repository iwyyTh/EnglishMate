"""Main entry point for the EnglishMate FastAPI backend application."""

from fastapi import FastAPI
from backend.routers.auth import router as auth_router
from backend.routers.chat import router as chat_router
from backend.routers.vocab import router as vocab_router

app = FastAPI(title="EnglishMate API")

# Register API routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(vocab_router)


@app.get("/")
def read_root():
    """Health check endpoint.

    Returns:
        dict: A welcome message indicating the server is running.
    """
    return {"message": "Hello from EnglishMate FastAPI Backend!"}
