from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from database import SessionLocal
from schemas import NoteCreate
import crud


"""
POST request is sent to crud.create_note
and GET requests to crud.get_note
"""

router = APIRouter(prefix="/notes")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, note)

@router.get("/search")
def search_notes(keyword: str, db: Session = Depends(get_db)):
    return crud.search_notes(db, keyword)

@router.get("/")
def get_notes(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return crud.get_notes(db)

@router.get("/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


@router.put("/{note_id}")
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    updated_note = crud.update_note(db, note_id, note)

    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")

    return updated_note


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    deleted_note = crud.delete_note(db, note_id)

    if not deleted_note:
        raise HTTPException(status_code=404, detail="Note not found")
    