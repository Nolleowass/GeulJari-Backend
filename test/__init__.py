from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from starlette.responses import Response


app = FastAPI()

dummy_user = {
    'account_id' : 1,
    'is_public' : True,
    'user_id' : "userid",
    'user_name' : "김뜻돌",
    'profile_image_url' : "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTAxMDZfMjM3%2FMDAxNjA5OTIyNzA4NzYy.db0HEh5p-7U4twgH-osVagQHKRUlF114w6Z8RvzyZisg.GIYLzk1SrGrXIx-3_FjdQfh5B9xhhaHskoOK3Ko4R6Ig.PNG.dkdoo98%2FKakaoTalk_20210103_191822702.png&type=sc960_832"
}

dummy_diary = {
    'diary_id' : 1,
    'content' : "해커톤 꿀잼꿀잼",
    'create_at' : "2022-01-08 19:32:10.0",
    'emotion_point' : '98',
    'account_id' : 1
}


@app.post("/auth/login", status_code=200)
async def login():
    return {
        "user_name" : "김뜻돌",
        "token" : "woeighfnqaweowoefb"
    }
    
@app.put("/auth/name", status_code=200)
async def name(response : Response):
    return {"" : ""}

@app.put("/auth/is_public", status_code=200)
async def name(response : Response):
    return {"" : ""}

@app.get("/auth/profile/list", status_code=200)
async def profile_list(response : Response):
    return {
        "profile_list" : [
            dummy_diary,
            dummy_diary.copy(),
            dummy_diary.copy(),
            dummy_diary.copy(),
            dummy_diary.copy()
        ]
    }
    
@app.post("/diary", status_code=201)
async def diary(response : Response):
    return {}

@app.put("/diary/{diary_id}", status_code=201)
async def diary(diary_id, response : Response):
    return {}

@app.delete("/diary/{diary_id}", status_code=201)
async def diary(diary_id, response : Response):
    return {}

@app.get("/diary/list/{user_id}", status_code=200)
async def diary(user_id, response : Response):
    return {
        "diary_list" : [
            dummy_diary,
            dummy_diary.copy(),
            dummy_diary.copy(),
        ]
    }
    

@app.get("/profile/list/", status_code=200)
async def diary(response : Response):
    return {
        "profile_list" : [
            dummy_diary,
            dummy_diary.copy(),
            dummy_diary.copy(),
            dummy_diary.copy(),
            dummy_diary.copy()
        ]
    }