"""
here defines the structure of the data entering or leaving via the API.
also it checks and validates

schema.py --> relates to API input/output.
"""

from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(min_length=3)
    content: str