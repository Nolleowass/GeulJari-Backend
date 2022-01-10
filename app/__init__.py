from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import config
from app.views import auth_router, diary_router, profile_router

def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
  
def init_routers(app : FastAPI) -> None:
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(diary_router, prefix="/diary", tags=["diary"])
    app.include_router(profile_router, prefix="/profile", tags=["profile"])

def create_app() -> FastAPI:
    app = FastAPI(
        title="Nolleowass-Backend",
        description="Hello World",
        version="1.0.0"
    )
    init_routers(app=app)
    init_cors(app=app)
    return app

app = create_app()
    