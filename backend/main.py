import logging

# Импорт модулей из внутренних пакетов
from bot import TelegramBot
from api import WebAppManager
from config import BOT_TOKEN, WEBHOOK_URL  # Импорт теперь происходит из пакета config


def setup_logging() -> None:
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


# Инициализация для доступа через uvicorn
telegram_bot = TelegramBot(BOT_TOKEN)
telegram_bot.register_handlers()
webapp_manager = WebAppManager(telegram_bot, webhook_url=WEBHOOK_URL)
app = webapp_manager.app  # Экспорт app для запуска через uvicorn


def main() -> None:
    """Основная функция запуска приложения"""
    setup_logging()
    webapp_manager.run()


if __name__ == "__main__":
    main()
