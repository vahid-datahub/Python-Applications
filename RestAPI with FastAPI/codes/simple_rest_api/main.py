from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# =====================================
# ========== Way 1 by Decorator ==========
# @app.get("/")
# def home():
#     return {"message": "Hello World"}
# ========== way 2 without decorator ==========
# def home():
#     return {"message": "Hello World"}
# app.add_api_route("/", home, methods=["GET"])
# =====================================

notes = [
    {"id": 1, "title": "Concept Drift", "content": "Concept drift changes over time."},
    {"id": 2, "title": "Federated Learning", "content": "FL trains models on distributed data."}]

class Note(BaseModel):
    title: str = Field(min_length=3)
    content: str

# using GET method to get user requests
@app.get("/notes")
def get_notes():
    return notes

# creating new note by user via API
@app.post("/notes")
def create_note(note: Note):
    new_note = {
        "id": len(notes) + 1,
        "title": note.title,
        "content": note.content
    }

    notes.append(new_note)
    return new_note

# now we want to get just one note instead of all notes
# with Path Parameter
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note

    return {"error": "Note not found"}

# editing existing note
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    for existing_note in notes:
        if existing_note["id"] == note_id:
            existing_note["title"] = note.title
            existing_note["content"] = note.content
            return existing_note

    return {"error": "Note not found"}

# deleting a notes
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return {"message": "Note deleted"}

    return {"error": "Note not found"}

# getting information from a URL with Query Parameters
@app.get("/search")
def search_notes(keyword: str):
    results = []

    for note in notes:
        if keyword.lower() in note["title"].lower():
            results.append(note)

    return results