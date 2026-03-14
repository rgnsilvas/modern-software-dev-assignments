# Project Guidance - Week 4
Aplikasi ini adalah full-stack task manager menggunakan FastAPI dan SQLite. Proyek ini berjalan di lingkungan Windows menggunakan Conda.

## Build & Run Commands (Windows)
- **Menjalankan Server**: `uvicorn backend.app.main:app --host 127.0.0.1 --port 8000` 
  *(Gunakan uvicorn langsung jika `python -m backend.app.main` mengalami kendala startup)*.
- **Inisialisasi Database**: Jalankan perintah SQL dari `backend/data/seed.sql` melalui SQLite atau script database.
- **Menjalankan Pengujian**: `pytest backend/tests`
- **Formatting**: `black .`

## Panduan Pengembangan & Konteks
- **Entry Point**: Logika utama aplikasi berada di `backend/app/main.py`.
- **Database**: Database SQLite otomatis diinisialisasi melalui fungsi `startup_event` di `main.py` menggunakan SQLAlchemy.
- **Frontend**: File statis dilayani dari folder `frontend/` melalui endpoint root `/`.
- **Warning**: Abaikan `DeprecationWarning` terkait `on_event("startup")` karena fitur tersebut masih didukung di versi FastAPI saat ini.

## Aturan Koding
- Selalu jalankan `black .` sebelum melakukan commit untuk menjaga konsistensi format.
- Setiap penambahan endpoint baru di router harus disertai dengan unit test di `backend/tests`.