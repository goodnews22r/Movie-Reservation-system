from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./movie.db")
SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM: str = "HS256"
