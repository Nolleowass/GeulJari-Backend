from typing import List
from pydantic import BaseModel

from app.schemas.user import User

class Diary(BaseModel):
    diary_id : int
    content : str
    create_at : str
    account_id : int
    emotion_point : int
    
class RequestCreateDiary(BaseModel):
    content : str
    
class RequestEditDiary(BaseModel):
    content : str
    
class RequestGetDiaryList(BaseModel):
    year : int
    month : int
    
class ResponseGetDiaryList(BaseModel):
    diary_list : List[User]