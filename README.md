# Campus Event Registration Platform

Proyek Ujian Tengah Semester untuk mata kuliah **Interoperability**.

---

## Teknologi yang Digunakan

- **Backend**: Python FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML + CSS + JavaScript (Fetch API)
- **API Docs**: Swagger UI (otomatis dari FastAPI)

---

## Cara Menjalankan Proyek

1. **Clone Repository**

```bash
git clone https://github.com/chibimarukochaan/interoperability-final-ratna-dewi
cd interoperability-final-ratna-dewi
```

2. **Setup Database**
   Jika database belum ada, jalankan:

```bash
Copy code
sqlite3 events.db < create_db.sql
```

3. **Install Dependencies**

```bash
Copy code
pip install fastapi uvicorn sqlalchemy pydantic email-validator
```

4. **Jalankan Backend**

```bash
Copy code
uvicorn main:app --reload
Server berjalan di:
http://127.0.0.1:8000

Dokumentasi API (Swagger):
http://127.0.0.1:8000/docs
```

5. **Jalankan Frontend**
   Buka file:

diff
Copy code
index.html
langsung di browser.

**Deskripsi Endpoint API**
Events

GET /events
Mendapatkan daftar semua event & sisa kuota
Response: 200 OK

POST /events (Admin Only)
Menambah event baru
Header:

```bash
x-token: rahasia123
```

Body:

```bash
json
Copy code
{
  "title": "Judul Event",
  "date": "2025-12-01",
  "location": "Aula Kampus",
  "quota": 50
}
```

Response: 201 Created

PUT /events/{event_id} (Admin Only)
Mengubah event berdasarkan ID
Response: 200 OK

DELETE /events/{event_id} (Admin Only)
Menghapus event
Response: 200 OK

Participants

POST /register
Mendaftarkan peserta ke event
Body:

```bash
json
Copy code
{
  "name": "Nama Peserta",
  "email": "nama@peserta.com",
  "event_id": 1
}
```

Response: 201 Created

GET /participants
Menampilkan semua peserta
Response: 200 OK

Authentication Admin Token
Endpoint CRUD Event dilindungi:

```bash
x-token: rahasia123
```
