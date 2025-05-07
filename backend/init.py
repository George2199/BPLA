import os
import subprocess
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения

# Путь к SQLite файлу
DB_PATH = os.getenv("SQLITE_PATH", "db.sqlite3")

def ensure_db_file():
    if not os.path.exists(DB_PATH):
        print(f"📁 Creating SQLite database at '{DB_PATH}'...")
        open(DB_PATH, 'a').close()
    else:
        print(f"✅ SQLite database already exists at '{DB_PATH}'.")

def run_migrations():
    print("📦 Running migrations...")

    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ["FLASK_APP"] = "app.py"

    result = subprocess.run(
        ["flask", "db", "upgrade"],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print("⚠️ Migration errors:\n", result.stderr)

if __name__ == "__main__":
    ensure_db_file()
    run_migrations()
