from typing import List
from pydantic import BaseModel

from app.schemas.user import User

class ResponseGetViewProfileList(BaseModel):
    profile_list: List[User]
