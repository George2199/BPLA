import os
from dotenv import load_dotenv

load_dotenv()

USE_SQLITE = os.getenv("USE_SQLITE", "1") == "1"

class Config:
    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    else:
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
