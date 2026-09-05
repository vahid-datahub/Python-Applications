from app.bot.telegram_bot import TelegramBot
from app.config.settings import Settings
import asyncio
from dotenv import load_dotenv

load_dotenv()

def main():
    telegram_bot = TelegramBot(Settings.TELEGRAM_BOT_TOKEN)
    asyncio.run(telegram_bot.start())

if __name__ == "__main__":
    main()