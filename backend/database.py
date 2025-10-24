from sqlalchemy import create_engine, MetaData

# URL database SQLite 
DATABASE_URL = "sqlite:///./events.db"

# untuk engine koneksi ke SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Metadata dipakai untuk definisi tabel
metadata = MetaData()
