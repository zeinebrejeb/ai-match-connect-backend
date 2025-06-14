from typing import Optional, List 
from pydantic import BaseModel

# from enum import Enum
# class UserRole(str, Enum):
#     CANDIDATE = "candidate"
#     RECRUITER = "recruiter"
#     ADMIN = "admin"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer" 
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    email: Optional[str] = None 
    roles: Optional[List[str]] = [] 

class RefreshTokenRequest(BaseModel):
    refresh_token: str