from fastapi import APIRouter, Depends
from sqlalchemy import extract
from starlette.responses import JSONResponse, PlainTextResponse, Response

from app.models import Diary, User, Relation
from app.schemas.diary import RequestCreateDiary, RequestEditDiary, RequestGetDiaryList

from sqlalchemy.orm import Session

from core.db import get_db
from core.middlewares.auth import AuthProvider
from jwt import decode
from core.config import config
import requests

diary_router = APIRouter()

def get_emotion_point(content : str) -> int:
    response = requests.post(url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze",
                             json={
                                 'content': content
                             },
                             headers={
                                 config.CLOVA_API_KEY_ID_NAME: config.CLOVA_API_KEY_ID,
                                 config.CLOVA_API_KEY_NAME: config.CLOVA_API_KEY,
                                 "Content-Type": "application/json"
                             }

                             ).json()
    positive = response['document']['confidence']['positive']
    neutral = response['document']['confidence']['neutral']
    negative = response['document']['confidence']['negative']
    print(positive, neutral, negative)
    return (positive - negative) / 2 + 50

@diary_router.post("/create")
async def create(req: RequestCreateDiary,
                 db: Session = Depends(get_db),
                 authorization: str = Depends(AuthProvider())
                 ):
    decoded_token = decode(authorization, key=config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
    user_info = db.query(User).filter(User.user_id == decoded_token['user_id']).first()
    account_id = user_info.account_id
    
    db.add(Diary(
        content = req.content,
        account_id = account_id,
        emotion_point = get_emotion_point(req.content)
    ))
    db.commit()
    return PlainTextResponse(status_code=200)
    
    
    
@diary_router.put("/{diary_id}")
async def edit(diary_id, req: RequestEditDiary, response: Response,
               db: Session = Depends(get_db),
               authorization: str = Depends(AuthProvider())):
    db.query(Diary).filter(Diary.diary_id == diary_id).update({
        "content" : req.content,
        "emotion_point" : get_emotion_point(req.content)
    })
    db.commit()
    return PlainTextResponse(status_code=200)
    

@diary_router.delete("/{diary_id}")
async def delete(diary_id, db: Session = Depends(get_db), authorization: str = Depends(AuthProvider())):
    db.query(Diary).filter(Diary.diary_id == diary_id).delete()
    db.commit()
    return PlainTextResponse(status_code=200)
    

@diary_router.get("/list/{user_id}")
async def diary_list(
    
    user_id: str,
    db: Session = Depends(get_db),
    authorization : str = Depends(AuthProvider()),
    year: int = 2022,
    month: int = 1
):
    user_info = db.query(User).filter(User.user_id == user_id).first()
    source_user_id = decode(authorization, key=config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)['user_id']
    source_account_id = db.query(User).filter(User.user_id == source_user_id).first().account_id
    target_account_id = user_info.account_id
    
    if source_account_id is not target_account_id:
        if db.query(Relation).filter(
            Relation.source_id == source_account_id,
            Relation.target_id == target_account_id
        ).first() is None:
            
            db.add(Relation(
                source_id = source_account_id,
                target_id = target_account_id
            ))
            db.commit()

    
    diary_list_query = db.query(Diary).filter(  
        extract('month', Diary.create_at) == month,
        extract('year', Diary.create_at) == year,
        Diary.account_id == target_account_id,
    ).all()
    
    diary_list = [ {
        "diary_id" : diary.diary_id,
        "content" : diary.content,
        "create_at" : str(diary.create_at)[:10],
        "account_id" : diary.account_id,
        "emotion_point" : diary.emotion_point
    } for diary in diary_list_query]
    return JSONResponse({"diary_list": diary_list})
    
    

