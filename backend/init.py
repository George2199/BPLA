import os
import subprocess
import psycopg2
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

if __name__ == "__main__":
    create_user_and_db()
    run_migrations()