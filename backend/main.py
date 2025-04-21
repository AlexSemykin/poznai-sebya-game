from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from contextlib import asynccontextmanager
from aiogram.fsm.storage.memory import MemoryStorage
import uvicorn
import logging
from typing import Dict

from config import BOT_TOKEN, WEBHOOK_URL


class TelegramBot:
    """Класс для управления ботом Telegram"""
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.router = Router()
    
    async def setup_webhook(self, webhook_url: str) -> None:
        """Настройка вебхука для бота"""
        try:
            await self.bot.set_webhook(url=webhook_url)
            logging.info(f"Вебхук настроен на {webhook_url}")
        except Exception as e:
            logging.error(f"Ошибка при настройке вебхука: {e}")
            raise

    async def delete_webhook(self) -> None:
        """Удаление вебхука"""
        await self.bot.delete_webhook()
    
    async def close(self) -> None:
        """Закрытие сессии бота"""
        await self.bot.session.close()
        
    def register_handlers(self) -> None:
        """Регистрация обработчиков сообщений"""
        MessageHandler(self.router)
        self.dp.include_router(self.router)


class MessageHandler:
    """Класс для обработки сообщений бота"""
    def __init__(self, router: Router):
        self.router = router
        self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Настройка обработчиков сообщений"""
        @self.router.message(Command("start"))
        async def cmd_start(message: types.Message) -> None:
            keyboard = ReplyKeyboardMarkup(
                resize_keyboard=True, 
                keyboard=[
                    [
                        KeyboardButton(
                            text="Открыть Mini App",
                            web_app=WebAppInfo(url="https://alexsemykin.github.io/poznai-sebya-game/")
                        )
                    ]
                ]
            )
            await message.answer("Привет! Нажми кнопку ниже:", reply_markup=keyboard)
        
        @self.router.message(F.web_app_data)
        async def web_app_data_handler(message: types.Message) -> None:
            payload = message.web_app_data.data
            await message.answer(
                f"Получены данные из приложения: <code>{payload}</code>", 
                parse_mode="HTML"
            )


class WebAppManager:
    """Класс для управления FastAPI приложением"""
    def __init__(self, telegram_bot: TelegramBot, webhook_path: str = "/webhook"):
        self.telegram_bot = telegram_bot
        self.webhook_path = webhook_path
        self.app = self._create_app()
        
    def _create_app(self) -> FastAPI:
        """Создание FastAPI приложения"""
        telegram_bot = self.telegram_bot
        webhook_path = self.webhook_path
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Настройка вебхука при запуске
            await telegram_bot.setup_webhook(f"{WEBHOOK_URL}{webhook_path}")
            yield
            # Очистка при завершении
            await telegram_bot.delete_webhook()
            await telegram_bot.close()
            
        app = FastAPI(lifespan=lifespan)
        
        @app.get("/")
        async def root() -> Dict[str, str]:
            """Корневой эндпоинт для проверки состояния сервера"""
            return {"status": "ok", "message": "Сервер работает"}
        
        @app.post(webhook_path)
        async def webhook(request: Request) -> Dict[str, bool]:
            """Эндпоинт для получения обновлений от Telegram"""
            update = types.Update.model_validate(
                await request.json(), 
                context={"bot": telegram_bot.bot}
            )
            await telegram_bot.dp.feed_update(
                bot=telegram_bot.bot, 
                update=update
            )
            return {"ok": True}
            
        return app
    
    def run(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Запуск FastAPI приложения"""
        uvicorn.run(app=self.app, host=host, port=port)


def setup_logging() -> None:
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


# Инициализация для доступа через uvicorn
telegram_bot = TelegramBot(BOT_TOKEN)
telegram_bot.register_handlers()
webapp_manager = WebAppManager(telegram_bot)
app = webapp_manager.app  # Экспорт app для запуска через uvicorn


def main() -> None:
    """Основная функция запуска приложения"""
    setup_logging()
    webapp_manager.run()


if __name__ == "__main__":
    main()
