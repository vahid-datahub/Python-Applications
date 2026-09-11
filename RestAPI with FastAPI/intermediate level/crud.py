from sqlalchemy.orm import Session
from models import Note
from schemas import NoteCreate


"""
This function is responsible for creating a new Note in the database.
"""
"""
crud.py receives valid data from schemas.py 
    and uses models.py to create database records. 
It also uses a session—derived from the infrastructure that is 
    set up in database.py to perform database operations.

"""


def create_note(db: Session, note: NoteCreate):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def get_notes(db: Session):
    return db.query(Note).all()


def update_note(db: Session, note_id: int, note: NoteCreate):
    existing_note = db.query(Note).filter(Note.id == note_id).first()

    if existing_note:
        existing_note.title = note.title
        existing_note.content = note.content
        db.commit()
        db.refresh(existing_note)

    return existing_note


def delete_note(db: Session, note_id: int):
    existing_note = db.query(Note).filter(Note.id == note_id).first()

    if existing_note:
        db.delete(existing_note)
        db.commit()

    return existing_note

def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()

def search_notes(db: Session, keyword: str):
    return db.query(Note).filter(Note.title.contains(keyword)).all()