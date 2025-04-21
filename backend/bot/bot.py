from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
import logging

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
        from .handlers import MessageHandler
        MessageHandler(self.router)
        self.dp.include_router(self.router)
