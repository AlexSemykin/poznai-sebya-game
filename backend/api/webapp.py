from fastapi import FastAPI, Request
from aiogram import types
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict

class WebAppManager:
    """Класс для управления FastAPI приложением"""
    def __init__(self, telegram_bot, webhook_path: str = "/webhook", webhook_url: str = None):
        self.telegram_bot = telegram_bot
        self.webhook_path = webhook_path
        self.webhook_url = webhook_url
        self.app = self._create_app()
        
    def _create_app(self) -> FastAPI:
        """Создание FastAPI приложения"""
        telegram_bot = self.telegram_bot
        webhook_path = self.webhook_path
        webhook_url = self.webhook_url
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # Настройка вебхука при запуске
            await telegram_bot.setup_webhook(f"{webhook_url}{webhook_path}")
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
