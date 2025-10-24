from sqlalchemy import select, insert, update, delete
from database import engine
from models import events, participants
from datetime import datetime


# CRUD events
def get_events():
    with engine.connect() as conn:
        query = select(events)
        result = conn.execute(query).fetchall()
        data = []
        for row in result:
            event_dict = dict(row._mapping)

            # untuk hitung jml peserta event ini
            q_count = select(participants).where(participants.c.event_id == event_dict["id"])
            registered = len(conn.execute(q_count).fetchall())
            event_dict["registered"] = registered
            event_dict["remaining_quota"] = event_dict["quota"] - registered
            data.append(event_dict)
        return data

def create_event(data):
    
    if isinstance(data.get("date"), str):
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").date()

    with engine.begin() as conn:
        query = insert(events).values(**data)
        result = conn.execute(query)
        return {**data, "id": result.lastrowid}

def update_event(event_id, data):
    if isinstance(data.get("date"), str):
        data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").date()

    with engine.begin() as conn:
        query = update(events).where(events.c.id == event_id).values(**data)
        conn.execute(query)
        return get_event_by_id(event_id)

def delete_event(event_id):
    with engine.begin() as conn:
        query = delete(events).where(events.c.id == event_id)
        conn.execute(query)
        return True

def get_event_by_id(event_id):
    with engine.connect() as conn:
        query = select(events).where(events.c.id == event_id)
        row = conn.execute(query).fetchone()
        return dict(row._mapping) if row else None

# CRUD participants
def get_participants():
    with engine.connect() as conn:
        query = select(participants)
        result = conn.execute(query).fetchall()
        return [dict(row._mapping) for row in result]

def register_participant(data):
    event_id = data["event_id"]

    with engine.begin() as conn:
        # mengecek eventnya ada/tidak
        q_event = select(events).where(events.c.id == event_id)
        event = conn.execute(q_event).fetchone()
        if not event:
            raise ValueError("Event tidak ditemukan")

        # hitung jml peserta saat ini
        q_count = select(participants).where(participants.c.event_id == event_id)
        current = len(conn.execute(q_count).fetchall())

        if current >= event._mapping["quota"]:
            raise ValueError("Kuota event sudah penuh!")

        # untuk save peserta baru
        q_insert = insert(participants).values(**data)
        res = conn.execute(q_insert)
        return {**data, "id": res.lastrowid}