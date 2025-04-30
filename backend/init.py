import os
import subprocess
from dotenv import load_dotenv

load_dotenv()  # Загрузка из .env

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

def ensure_db_exists():
    if not os.path.exists(DB_PATH):
        print(f"🗃 Creating new SQLite DB at {DB_PATH}...")
        # Просто создаем пустой файл — SQLAlchemy его инициализирует при миграции
        open(DB_PATH, 'a').close()
    else:
        print("✅ SQLite DB already exists.")

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
    ensure_db_exists()
    run_migrations()
