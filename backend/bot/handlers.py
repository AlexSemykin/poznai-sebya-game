from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup

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
