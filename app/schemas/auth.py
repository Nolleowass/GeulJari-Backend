from typing import List, Optional
from pydantic import BaseModel

from app.schemas.user import User


class RequestLogIn(BaseModel):
    user_id : str
    password : str
    user_name : Optional[str]
    
class ResponseLogIn(BaseModel):
    user_name : str
    token : str
    
class RequestChangeUserName(BaseModel):
    user_name : str
    
class RequestIsPublic(BaseModel):
    is_public : bool
    
 