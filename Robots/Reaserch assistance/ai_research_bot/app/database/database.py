import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base

class Database:

    def __init__(self):
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise ValueError("DATABASE_URL is not set.")

        self.engine = create_engine(database_url)
        self.session_factory = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.session_factory()