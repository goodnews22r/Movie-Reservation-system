from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    model_config = {"from_attributes": True}


class RegisterResponse(BaseModel):
    message: str
    user_id: int
    access_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
