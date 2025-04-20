# main.py
from fastapi import FastAPI
from api import sticker_router
from core.logging import setup_logger

setup_logger()

app = FastAPI()

app.include_router(sticker_router.router, prefix="/api")
