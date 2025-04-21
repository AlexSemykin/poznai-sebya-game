from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from contextlib import asynccontextmanager
from aiogram.fsm.storage.memory import MemoryStorage
import uvicorn

from config import BOT_TOKEN, WEBHOOK_URL

# Инициализация компонентов
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Настройка lifespan для FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Настройка вебхука при запуске
    try:
        await bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
        print(f"Вебхук настроен на {WEBHOOK_URL}/webhook")
    except Exception as e:
        print(f"Ошибка при настройке вебхука: {e}")

    yield

    # Очистка при завершении
    await bot.delete_webhook()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)

# Добавляем корневой маршрут для проверки
@app.get("/")
async def root():
    return {"status": "ok", "message": "Сервер работает"}

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(
            text="Открыть Mini App",
            web_app=WebAppInfo(url="https://alexsemykin.github.io/poznai-sebya-game/")
        )]
    ])
    await message.answer("Привет! Нажми кнопку ниже:", reply_markup=keyboard)

# Обработчик данных из Web App
@router.message(F.web_app_data)
async def web_app_data_handler(message: types.Message):
    payload = message.web_app_data.data
    await message.answer(f"Получены данные из приложения: <code>{payload}</code>", parse_mode="HTML")

# Регистрация роутера
dp.include_router(router)

@app.post("/webhook")
async def webhook(request: Request):
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)