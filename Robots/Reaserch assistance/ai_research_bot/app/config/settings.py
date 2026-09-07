from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    WEBAPP_URL = "https://vahid-datahub.github.io/Python-Applications/"