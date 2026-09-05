from app.services.llm.ollama_provider import OllamaLLMProvider
from app.services.llm.llm_service import LLMService


provider = OllamaLLMProvider()

llm_service = LLMService(
    provider=provider
)

prompt = "Explain artificial intelligence in two sentences."

answer = llm_service.generate_answer(prompt)

print(answer)