import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    USE_SQLITE = os.getenv("USE_SQLITE", "1") == "1"

    if USE_SQLITE:
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'app.db')}"
    else:
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
