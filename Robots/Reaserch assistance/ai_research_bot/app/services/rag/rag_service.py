from app.services.retrieval.retrieval_service import RetrievalService
from app.services.llm.llm_service import LLMService


class RAGService:

    def __init__(self, retrieval_service: RetrievalService, llm_service: LLMService):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def answer_question(self, question: str, document_id: str, limit: int = 5) -> str:
        results = self.retrieval_service.retrieve(query=question,
            limit=limit,document_id=document_id)

        context = self._build_context(results)
        prompt = self._build_prompt(question=question,context=context)

        return self.llm_service.generate_answer(prompt)

    def _build_context(self, results) -> str:
        chunks = []
        for result in results:
            text = result.payload.get("text", "")
            chunks.append(text)

        return "\n\n".join(chunks)

    def _build_prompt(self,question: str,context: str) -> str:

        return f"""You are a research assistant. Answer the user's question based only on the 
                        provided research paper context. If the answer cannot be found in the context, 
                            say that the information is not available in the provided document. 
                                Research paper context: {context}
                                    User question: {question}
                                        Answer: """
                                        
    def generate_summary(self, document_id: str, limit: int = 10) -> str:
        results = self.retrieval_service.retrieve(
            query="research paper summary methodology findings conclusion",limit=limit,document_id=document_id)

        context = self._build_context(results)

        prompt = f"""You are a research assistant.
                Summarize the research paper based only on the provided context.
        Include:
        - Research problem
        - Methodology
        - Main findings
        - Conclusion
    Research paper context:
    {context}
    Summary:"""

        return self.llm_service.generate_answer(prompt)
    
    def extract_key_information(self, document_id: str, limit: int = 15) -> str:
        results = self.retrieval_service.retrieve(
            query="research problem research gap methodology algorithms metrics results findings",
            limit=limit, document_id=document_id)

        context = self._build_context(results)

        prompt = f"""You are a research assistant.

    Extract the following information from the research paper.
    Use only the provided context.

    1. Problem Statement
    2. Research Gap
    3. Methodology
    4. Algorithms
    5. Evaluation Metrics
    6. Main Results

    If any information is not available in the context, say:
    "Not available in the provided context." 
    but dont write not available, you should find it and extract it in the context, by similar name or context
    if there was any number for metrics also say them, also mention the name of algorithms too. 
    finally there are 6 parts, so dont make it more just put them in these 6 related parts.

    Research paper context:
    {context}

    Extracted Information:"""

        return self.llm_service.generate_answer(prompt)