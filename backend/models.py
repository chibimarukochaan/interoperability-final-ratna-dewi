from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from database import metadata, engine

# Tabel events
events = Table(
    "events", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(100), nullable=False),
    Column("date", Date, nullable=False),
    Column("location", String(100), nullable=False),
    Column("quota", Integer, nullable=False)
)

# Tabel participants
participants = Table(
    "participants", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), nullable=False),
    Column("event_id", Integer, ForeignKey("events.id"))
)

# Fungsi untuk bikin semua tabel di database
def create_tables():
    metadata.create_all(engine)