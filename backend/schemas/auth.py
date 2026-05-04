from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """Schema for user login credentials."""
    email: EmailStr
    password: str

class SignupRequest(BaseModel):
    """Schema for user registration credentials."""
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    """Schema for Google OAuth login payload."""
    id_token: str