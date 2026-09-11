# this code defines the data structure to be stored in the database.
"""this structure in our code is Note

models.py --> Data structure within the database

"""

from sqlalchemy import Column, Integer, String
from database import Base

# using SQLAlchemy 
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)