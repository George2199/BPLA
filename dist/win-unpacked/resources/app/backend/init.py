import os
import subprocess
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения

# Путь к SQLite файлу
DB_PATH = os.getenv("SQLITE_PATH", "db.sqlite3")

def ensure_clean_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed old DB at '{DB_PATH}'")

    print(f"Creating clean SQLite DB at '{DB_PATH}'")
    open(DB_PATH, 'a').close()


def run_migrations():
    print("Running migrations...")

    # os.environ["FLASK_APP"] = "app.py
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

    result = subprocess.run(
        ["flask", "db", "upgrade"],
        cwd=backend_dir,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print("Migration errors:\n", result.stderr)

if __name__ == "__main__":
    ensure_clean_db()
    run_migrations()
