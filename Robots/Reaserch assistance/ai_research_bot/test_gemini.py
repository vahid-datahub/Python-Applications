from dotenv import load_dotenv
load_dotenv()

from app.services.llm.gemini_provider import GeminiLLMProvider

provider = GeminiLLMProvider()

answer = provider.generate("What is artificial intelligence?")

print(answer)