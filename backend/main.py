from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import models, crud

app = FastAPI()

# buat tabel saat aplikasi pertama kali jalan
models.create_tables()


# autentikasi admin 
ADMIN_TOKEN = "rahasia123"

def verify_token(x_token: Optional[str] = Header(None)):
    """Memeriksa apakah header x-token berisi token admin yang benar"""
    if x_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token tidak valid")

# model Pydantic
class EventCreate(BaseModel):
    title: str
    date: str
    location: str
    quota: int

class ParticipantCreate(BaseModel):
    name: str
    email: EmailStr
    event_id: int

# endpoint utama 
@app.get("/")
def root():
    return {"message": "Halo, nana"}


# ENDPOINT CRUD EVENTS
@app.get("/events")
def read_events():
    return crud.get_events()

# CREATE (hanya admin)
@app.post("/events", dependencies=[Depends(verify_token)])
def create_event(event: EventCreate):
    created = crud.create_event(event.dict())
    return {"message": "Event berhasil dibuat!", "event": created}

# UPDATE (hanya admin)
@app.put("/events/{event_id}", dependencies=[Depends(verify_token)])
def update_event(event_id: int, event: EventCreate):
    existing = crud.get_event_by_id(event_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Event tidak ditemukan.")
    updated = crud.update_event(event_id, event.dict())
    return {"message": "Event berhasil diperbarui!", "event": updated}

# DELETE (hanya admin)
@app.delete("/events/{event_id}", dependencies=[Depends(verify_token)])
def delete_event(event_id: int):
    existing = crud.get_event_by_id(event_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Event tidak ditemukan.")
    crud.delete_event(event_id)
    return {"message": f"Event dengan ID {event_id} berhasil dihapus!"}

# ENDPOINT PARTICIPANTS
@app.get("/participants")
def get_all_participants():
    return crud.get_participants()

@app.post("/register")
def register_participant(participant: ParticipantCreate):
    try:
        data = participant.dict()
        created = crud.register_participant(data)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# halaman frontend
from fastapi.responses import FileResponse
import os

@app.get("/web")
def serve_webpage():
    base_path = os.path.dirname(os.path.abspath(__file__))
    frontend_path = os.path.join(base_path, "../frontend/index.html")
    return FileResponse(frontend_path)
