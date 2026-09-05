from dotenv import load_dotenv
load_dotenv()

from app.services.llm.openai_provider import OpenAILLMProvider

provider = OpenAILLMProvider()

print("TEST START")

answer = provider.generate("What is artificial intelligence?")

print("ANSWER:", repr(answer))

print(answer)