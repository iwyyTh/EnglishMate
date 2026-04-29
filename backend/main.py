from fastapi import FastAPI
from backend.routers.auth import router as auth_router
from backend.routers.chat import router as chat_router

app = FastAPI(title="EnglishMate API")

app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
def read_root():
    return {"message": "Hello từ Backend FastAPI của EnglishMate!"}
