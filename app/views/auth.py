from fastapi import APIRouter, Depends
from sqlalchemy import extract
from sqlalchemy.sql.operators import all_op
from starlette.responses import JSONResponse, PlainTextResponse, Response

from sqlalchemy.orm import Session
from app.models.diary import Diary
from app.models.relation import Relation
from app.models.user import User
from core.db import get_db
import jwt
import bcrypt

from app.schemas.auth import RequestChangeUserName, RequestIsPublic, RequestLogIn
from core.config import config
from core.middlewares.auth import AuthProvider
from jwt import decode
import random
auth_router = APIRouter()


@auth_router.post("/login")
async def login(req: RequestLogIn, db: Session = Depends(get_db)):
    random_image_url = [
        "https://user-images.githubusercontent.com/2310571/148657214-fdd027a1-5eda-441f-9e97-fbb546c13511.png",
        "https://user-images.githubusercontent.com/2310571/148657219-eb9096e4-4cc4-441b-a07c-5e03cc381cbb.png",
        "https://user-images.githubusercontent.com/2310571/148657226-136633e0-2f53-4f0f-bf82-90f2e3bc88e7.png",
        "https://user-images.githubusercontent.com/2310571/148657227-592ebd3b-6084-4811-9e9e-be073d50e8d0.png",
        "https://user-images.githubusercontent.com/2310571/148657228-1a29cbf9-e306-4fe9-bc91-f1175641597d.png"
    ]
    random.shuffle(random_image_url)
    user_info = db.query(User).filter(User.user_id == req.user_id).first()
    encoded_jwt = None

    if user_info is None:
        db.add(User(
            is_public=True,
            user_id=req.user_id,
            password=bcrypt.hashpw(req.password.encode(
                "utf-8"), bcrypt.gensalt()).decode("utf-8"),
            profile_image_url=random_image_url[0],
            user_name=req.user_name if req.user_name else "닉네임",
        ))
        db.commit()
        user_info = db.query(User).filter(User.user_id == req.user_id).first()
    else:
        if(not bcrypt.checkpw(req.password.encode("utf-8"), user_info.password.encode("utf-8"))):
            return PlainTextResponse(status_code=404)

    encoded_jwt = jwt.encode(
        {
            'exp': 99999999999,
            'user_id': req.user_id,
        },
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

    return JSONResponse({
        'user_id': user_info.user_id,
        "token": encoded_jwt
    }, status_code=200)


@auth_router.put("/name")
async def name(req: RequestChangeUserName, authorization: str = Depends(AuthProvider()), db: Session = Depends(get_db)):
    decoded_token = decode(
        authorization, key=config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
    user_id = decoded_token['user_id']
    db.query(User).filter(User.user_id == user_id).update(
        {"user_name": req.user_name})
    db.commit()
    return PlainTextResponse(status_code=200)


@auth_router.put("/is_public")
async def name(req: RequestIsPublic, authorization: str = Depends(AuthProvider()), db: Session = Depends(get_db)):
    decoded_token = decode(
        authorization, key=config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
    user_id = decoded_token['user_id']
    db.query(User).filter(User.user_id == user_id).update(
        {"is_public": req.is_public})
    db.commit()
    return PlainTextResponse(status_code=200)


@auth_router.get("/profile/list")
async def get_profile_list(authorization: str = Depends(AuthProvider()), db: Session = Depends(get_db)):
    print("hello")
    user_id = decode(authorization, key=config.JWT_SECRET_KEY,
                     algorithms=config.JWT_ALGORITHM)["user_id"]
    account_id = db.query(User).filter(
        User.user_id == user_id).first().account_id
    query = db.query(Relation).filter(Relation.source_id == account_id).all()
    profile_list = []
    for relation in query:
        user = db.query(User).filter(
            User.account_id == relation.target_id).first()
        profile_list.append({
            "account_id": user.account_id,
            "user_name": user.user_name,
            "user_id": user.user_id,
            "profile_image_url": user.profile_image_url,
            "is_public": user.is_public
        })

    return JSONResponse({'profile_list': profile_list}, status_code=200)
