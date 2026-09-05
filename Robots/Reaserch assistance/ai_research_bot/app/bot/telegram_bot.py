from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import CommandStart
from pathlib import Path
from app.services.document_processor import DocumentProcessor
from app.services.embedding.ollama_provider import OllamaEmbeddingProvider
from app.services.embedding.embedding_service import EmbeddingService
from app.services.vector_store.qdrant_store import QdrantStore
from app.services.rag.rag_service import RAGService
from app.services.retrieval.retrieval_service import RetrievalService
from app.services.llm.ollama_provider import OllamaLLMProvider
from app.services.llm.llm_service import LLMService
from app.services.llm.gemini_provider import GeminiLLMProvider
from app.config.settings import Settings
from app.services.llm.openai_provider import OpenAILLMProvider
from app.database.database import Database
from app.database.models import User, Document

class TelegramBot:
    def __init__(self, token: str):
        
        self.token = token
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher() # to get telegram update
        self.documents_path = Path(__file__).resolve().parents[2] / "documents"
        print("DOCUMENT PATH:", self.documents_path.resolve())
        self.documents_path.mkdir(exist_ok=True)
        self.question_mode = {}
        self.document_selection_mode = {}
        self.max_file_size = 20 * 1024 * 1024
        
        self.dp.message.register(self.start_handler,CommandStart())
        self.dp.message.register(self.start_handler,lambda message: message.text == "🏠 Start")
        self.dp.message.register(self.research_assistant_handler, lambda message: message.text == "Research Assistant")
        self.dp.message.register(self.upload_document_handler, lambda message: message.text == "Upload Document")
        self.dp.message.register(self.my_documents_handler,lambda message: message.text == "My Documents")
        self.dp.message.register(self.research_question_handler,lambda message: message.text == "Ask Research Question")
        self.dp.message.register(self.paper_summary_handler,lambda message: message.text == "Paper Summary")
        self.dp.message.register(self.key_information_handler,lambda message: message.text == "Key Information")
        self.dp.message.register(self.document_handler, lambda message: message.document is not None)     
        self.dp.message.register(self.back_to_main_menu_handler,lambda message: message.text == "Back to Main Menu")   
        self.dp.message.register(self.select_document_handler,lambda message: message.text is not None)
        self.dp.message.register(self.question_handler,lambda message: message.text is not None)
        
        self.database = Database()
        embedding_provider = OllamaEmbeddingProvider()
        embedding_service = EmbeddingService(embedding_provider)
        vector_store = QdrantStore()
        self.document_processor = DocumentProcessor(embedding_service=embedding_service, vector_store=vector_store)
        
        if Settings.LLM_PROVIDER == "ollama":
            llm_provider = OllamaLLMProvider()
        elif Settings.LLM_PROVIDER == "gemini":
            llm_provider = GeminiLLMProvider()
        elif Settings.LLM_PROVIDER == "openai":
            llm_provider = OpenAILLMProvider()
        else:
            raise ValueError(f"Unsupported LLM provider: {Settings.LLM_PROVIDER}")

        llm_service = LLMService(llm_provider)
        retrieval_service = RetrievalService(embedding_service=embedding_service,vector_store=vector_store)
        self.rag_service = RAGService(retrieval_service=retrieval_service,llm_service=llm_service)

    async def start_handler(self, message: Message):
        user_id = message.from_user.id
        username = message.from_user.username

        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_id).first()
            if not user:
                user = User(telegram_id=user_id,username=username)
                session.add(user)
                session.commit()
                
        await message.answer("Welcome to your AI Research Assistant.\n\n"
        "Please select an option:", reply_markup=self.create_main_menu())    

    async def research_assistant_handler(self, message: Message):
        user_id = message.from_user.id
        
        self.question_mode[user_id] = False
        self.document_selection_mode[user_id] = False
    
        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_id).first()

            if not user:
                await message.answer("User not found in database.")
                return

            active_document_id = user.active_document_id

            active_file_name = None

            if active_document_id:
                document = session.query(Document).filter_by(document_id=active_document_id,user_id=user.id).first()

                if document:
                    active_file_name = document.file_name

        if active_file_name:
            text = (f"Active document:\n{active_file_name}\n\n""What would you like to do?")
        else:
            text = "No active document selected.\n\nWhat would you like to do?"

        await message.answer(text,reply_markup=self.create_research_menu())  
         
    async def document_handler(self, message: Message):
        document = message.document
        if document is None:
            return
        
        if document.file_size and document.file_size > self.max_file_size:
            await message.answer("File is too large. Maximum allowed size is 20 MB.")
            return

        file_name = document.file_name
        if not self.is_valid_document(file_name):
            await message.answer("Invalid file format.\n\n Please upload a PDF or Microsoft Word (.docx) file.")
            return

        file = await self.bot.get_file(document.file_id)
        print("ORIGINAL FILE:", file_name)
        file_path = self.get_unique_file_path(file_name)
        print("FINAL FILE PATH:", file_path)
        await self.bot.download_file(file.file_path,destination=file_path)

        try:
            result = self.document_processor.extract_document(file_path)

            user_id = message.from_user.id

            with self.database.get_session() as session:
                user = session.query(User).filter_by(telegram_id=user_id).first()

                if not user:
                    await message.answer("User not found in database.")
                    return

                document_record = Document(document_id=result.document_id, user_id=user.id,
                    file_name=result.file_name, file_path=str(file_path),
                    character_count=result.character_count, chunk_count=len(result.chunks))

                session.add(document_record)
                user.active_document_id = result.document_id
                session.commit()

            await message.answer(
                f"Document processed successfully.\n\n"
                f"File name: {result.file_name}\n"
                f"Characters extracted: {result.character_count}\n"
                f"Chunks created: {len(result.chunks)}\n"
                f"Embeddings created: {len(result.embeddings)}")

        except Exception as error:
            print(f"Document processing error: {error}")
            await message.answer("Sorry, something went wrong while processing your document.")
    
    async def my_documents_handler(self, message: Message):
        telegram_id = message.from_user.id

        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()

            if not user:
                await message.answer("User not found in database.")
                return

            documents = session.query(Document).filter_by(user_id=user.id).all()

        if not documents:
            await message.answer("You have not uploaded any documents yet.")
            return
        
        self.document_selection_mode[telegram_id] = True
        
        keyboard = [[KeyboardButton(text=document.file_name)] for document in documents]
        await message.answer("Select a document:",reply_markup=ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True))
                
    async def upload_document_handler(self, message: Message):
        await message.answer("Please upload your PDF or Microsoft Word file.") 
    
    async def research_question_handler(self, message: Message):
        user_id = message.from_user.id

        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_id).first()

            if not user or not user.active_document_id:
                await message.answer("Please select or upload a document before asking a question.")
                return

        self.question_mode[user_id] = True
        await message.answer("I'm ready to help. Go ahead and ask your Research Question.")
    
    async def select_document_handler(self, message: Message):
        telegram_id = message.from_user.id

        if not self.document_selection_mode.get(telegram_id):
            return

        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()

            if not user:
                await message.answer("User not found in database.")
                return

            document = session.query(Document).filter_by(user_id=user.id,file_name=message.text).first()

            if not document:
                await message.answer("Document not found.")
                return

            user.active_document_id = document.document_id
            session.commit()

        self.document_selection_mode[telegram_id] = False

        await message.answer(f"Active document selected:\n\n{document.file_name}",
            reply_markup=self.create_research_menu())
        
    async def question_handler(self, message: Message):
        user_id = message.from_user.id

        if not self.question_mode.get(user_id):
            return
        
        question = message.text
        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_id).first()

            if not user:
                await message.answer("User not found in database.")
                return

            document_id = user.active_document_id

        if not document_id:
            await message.answer("Please select a research paper before asking a question.")
            return

        await message.answer("Processing your question...")
        self.question_mode[user_id] = False
        
        try:
            answer = self.rag_service.answer_question(question=question, document_id=document_id,limit=5)
            await message.answer(answer)

        except Exception as error:
            print(f"Question processing error: {error}")
            await message.answer("An error occurred while processing your question.")
      
    def is_valid_document(self, file_name: str) -> bool:
        allowed_extensions = {".pdf", ".docx"}
        file_extension = Path(file_name).suffix.lower()
        return file_extension in allowed_extensions
        
    async def start(self):
        print("Telegram bot is starting...")

        await self.dp.start_polling(self.bot)
        
    def create_main_menu(self):
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Research Assistant")]],resize_keyboard=True)
        return keyboard
    
    def create_research_menu(self):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Upload Document"),
                KeyboardButton(text="Ask Research Question")],
                [KeyboardButton(text="Paper Summary")],
                [KeyboardButton(text="Key Information")],
                [KeyboardButton(text="My Documents")],
                [KeyboardButton(text="Back to Main Menu")],
                [KeyboardButton(text="🏠 Start")]],
            resize_keyboard=True)

        return keyboard
    
    def get_unique_file_path(self, file_name: str) -> Path:
        original_path = self.documents_path / file_name

        print(f"Checking path: {original_path}")
        print(f"File exists: {original_path.exists()}")

        if not original_path.exists():
            return original_path

        file_stem = original_path.stem
        file_suffix = original_path.suffix
        counter = 1

        while True:
            new_path = self.documents_path / f"{file_stem}_{counter}{file_suffix}"

            print(f"Checking new path: {new_path}")

            if not new_path.exists():
                return new_path

            counter += 1
    
    async def back_to_main_menu_handler(self, message: Message):
        user_id = message.from_user.id

        self.question_mode[user_id] = False
        self.document_selection_mode[user_id] = False

        await message.answer("Main Menu",reply_markup=self.create_main_menu())
        
    async def paper_summary_handler(self, message: Message):
        user_id = message.from_user.id

        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_id).first()

            if not user or not user.active_document_id:
                await message.answer("Please select or upload a document first.")
                return

            document_id = user.active_document_id
        await message.answer("Generating paper summary... \n\n --it may takes a few minutes please be patient!--")

        try:
            summary = self.rag_service.generate_summary(document_id=document_id,limit=10)

            await message.answer(summary)

        except Exception as error:
            print(f"Summary error: {error}")
            await message.answer("An error occurred while generating the summary.")
    
    async def key_information_handler(self, message: Message):
        user_id = message.from_user.id

        with self.database.get_session() as session:
            user = session.query(User).filter_by(telegram_id=user_id).first()

            if not user or not user.active_document_id:
                await message.answer("Please select or upload a document first.")
                return

            document_id = user.active_document_id

        await message.answer("Extracting key research information... \n\n --it may takes a few minutes please be patient!--")

        try:
            information = self.rag_service.extract_key_information(document_id=document_id,limit=15)

            await message.answer(information)

        except Exception as error:
            print(f"Key information extraction error: {error}")
            await message.answer("An error occurred while extracting the information.")