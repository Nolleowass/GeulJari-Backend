from fastapi import APIRouter
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette.responses import JSONResponse
from core.db import get_db

from core.middlewares.auth import AuthProvider
from jwt import decode
from core.config import config
from app.models import User, Relation

profile_router = APIRouter()

@profile_router.get("/list")
async def get_profile_list(authorization: str = Depends(AuthProvider()), db: Session = Depends(get_db)):
    print("hello")
    user_id = decode(authorization, key=config.JWT_SECRET_KEY,
                     algorithms=config.JWT_ALGORITHM)["user_id"]
    account_id = db.query(User).filter(
        User.user_id == user_id).first().account_id
    query = db.query(Relation).filter(Relation.target_id == account_id).all()
    profile_list = []
    
    for relation in query:
        user = db.query(User).filter(User.account_id == relation.source_id).first()
        profile_list.append({
            "account_id": user.account_id,
            "user_name": user.user_name,
            "user_id": user.user_id,
            "profile_image_url": user.profile_image_url,
            "is_public": user.is_public
        })
        

    return JSONResponse({'profile_list': profile_list}, status_code=200)
