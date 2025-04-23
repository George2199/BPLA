import os
import subprocess
import psycopg2
import urllib.request
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()  # Загрузка из .env

DB_NAME = os.getenv("DB_NAME", "BPLA")
DB_USER = os.getenv("DB_USER", "creator")
DB_PASS = os.getenv("DB_PASS", "1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def create_user_and_db():
    try:
        # Подключаемся от имени postgres
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=os.getenv("PG_POSTGRES_PASS", "1234"),  # или через .pgpass
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Создание пользователя, если не существует
        cur.execute(sql.SQL(
            "SELECT 1 FROM pg_roles WHERE rolname = %s"
        ), [DB_USER])
        if not cur.fetchone():
            print(f"🧑‍💻 Creating user '{DB_USER}'...")
            cur.execute(sql.SQL(
                "CREATE USER {} WITH PASSWORD %s"
            ).format(sql.Identifier(DB_USER)), [DB_PASS])
        else:
            print(f"✅ User '{DB_USER}' already exists.")

        # Создание БД, если не существует
        cur.execute(sql.SQL(
            "SELECT 1 FROM pg_database WHERE datname = %s"
        ), [DB_NAME])
        if not cur.fetchone():
            print(f"🗃 Creating database '{DB_NAME}'...")
            cur.execute(sql.SQL(
                "CREATE DATABASE {} OWNER {}"
            ).format(sql.Identifier(DB_NAME), sql.Identifier(DB_USER)))
        else:
            print(f"✅ Database '{DB_NAME}' already exists.")

        # Выдаём права (на всякий случай)
        cur.execute(sql.SQL(
            "GRANT ALL PRIVILEGES ON DATABASE {} TO {}"
        ).format(sql.Identifier(DB_NAME), sql.Identifier(DB_USER)))

        cur.close()
        conn.close()
        print("🚀 User and DB setup completed.")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_migrations():
    print("📦 Running migrations...")

    # Перейти в backend, где находится app.py
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ["FLASK_APP"] = "app.py"

    result = subprocess.run(
        ["flask", "db", "upgrade"],
        cwd=backend_dir,  # <-- указание рабочей директории
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print("⚠️ Migration errors:\n", result.stderr)

def download_pyodide():
    print("📡 Checking Pyodide...")

    base_url = "https://cdn.jsdelivr.net/pyodide/v0.27.5/full/"
    files = [
        "pyodide.js",
        "pyodide.asm.js",
        "pyodide.asm.wasm",
        "python_stdlib.zip",
        "pyodide-lock.json"  # ✅ Вот этот файл тебя сейчас убивает
    ]
    target_dir = os.path.join(os.path.dirname(__file__), "..", "public", "pyodide")
    os.makedirs(target_dir, exist_ok=True)

    for filename in files:
        local_path = os.path.join(target_dir, filename)
        if not os.path.exists(local_path):
            print(f"⬇️ Downloading {filename}...")
            try:
                urllib.request.urlretrieve(base_url + filename, local_path)
                print(f"✅ Saved: {local_path}")
            except Exception as e:
                print(f"❌ Failed to download {filename}: {e}")
        else:
            print(f"✔️ Already exists: {filename}")

if __name__ == "__main__":
    create_user_and_db()
    run_migrations()
    download_pyodide()