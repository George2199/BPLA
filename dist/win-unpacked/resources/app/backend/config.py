import os
from dotenv import load_dotenv

load_dotenv()

USE_SQLITE = os.getenv("USE_SQLITE", "1") == "1"

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_sqlite_uri(db_path=None):
        if not db_path:
            # Get path from .env (relative or absolute)
            env_path = os.getenv("SQLITE_PATH", "db.sqlite3")

            # If it's relative, resolve it to absolute
            if not os.path.isabs(env_path):
                base_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.abspath(os.path.join(base_dir, env_path))
            else:
                db_path = env_path

        return f"sqlite:///{db_path}"
