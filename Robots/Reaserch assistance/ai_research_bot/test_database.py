from dotenv import load_dotenv
load_dotenv()

from app.database.database import Database
from app.database.models import Base


database = Database()

Base.metadata.drop_all(database.engine)
Base.metadata.create_all(database.engine)

print("Database tables recreated successfully!")