import os
from dotenv import load_dotenv

load_dotenv()

USE_SQLITE = os.getenv("USE_SQLITE", "1") == "1"

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_sqlite_uri(db_path=None):
        if not db_path:
            db_path = os.getenv("SQLITE_PATH", "data/db.sqlite3")
        return f"sqlite:///{db_path}"


    @staticmethod
    def get_postgres_uri():
        return (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
