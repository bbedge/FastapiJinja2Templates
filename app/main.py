import uvicorn
from loguru import logger
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.frontend import router as fronted_routes


@asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:   # if the 'app' parameter is used
async def lifespan(_: FastAPI) -> AsyncGenerator[dict, None]:
    """Управление жизненным циклом приложения."""
    # logger.info("Инициализация приложения...")
    yield
    # logger.info("Завершение работы приложения...")


# Регистрация приложения
app = FastAPI(lifespan=lifespan)

# Подключение статики
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Обработка ошибки 404
@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse("app/templates/404.html")


# Настройка CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,    # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Регистрация маршрутов
app.include_router(fronted_routes)  # fronted


if __name__ == "__main__":
    logger.info(f"Сервер стартован.")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
