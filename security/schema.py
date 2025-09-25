"""Contains request and response security schemas"""

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    

class LoginResponse(BaseModel):
    message: str = "Login successful"
    token: Token
    user_id: str
    role: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []