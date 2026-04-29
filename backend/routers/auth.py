from fastapi import APIRouter, HTTPException
from backend.schemas.auth import SignupRequest, LoginRequest
from backend.services.auth_service import login as auth_login, register as auth_register

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def api_register(mess : SignupRequest):
    user = auth_register(mess.email, mess.password)

    if isinstance(user, str):
        raise HTTPException(status_code=400, detail=user)
    return {"message": "Tạo tài khoản thành công", "user_id" : user.get("localId")}

@router.post("/login")
def api_login(mess : LoginRequest):
    user = auth_login(mess.email, mess.password)

    if isinstance(user, str):
        raise HTTPException(status_code=400, detail=user)
    return {"message": "Đăng nhập thành công", "user_id" : user.get("localId")}
