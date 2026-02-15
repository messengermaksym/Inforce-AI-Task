"""
Точка входу FastAPI: створення додатку, підключення маршрутів та статики.
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.database import engine, Base
from app.models import ChatSession, Message  # реєстрація моделей для create_all
from app.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inforce AI Task - Gemini 2.5 SDK")
app.include_router(api_router)

static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", include_in_schema=False)
async def index():
    """Головна сторінка — чат UI."""
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "UI не знайдено. Додайте app/static/index.html"}
