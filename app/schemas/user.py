
from pydantic import BaseModel


class User(BaseModel):
    account_id : int
    is_public : bool
    user_id : str
    user_name : str
    profile_image_url : str
    jwt : str

