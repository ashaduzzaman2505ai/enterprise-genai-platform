import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = "Enterprise GenAI Platform"
    DATA_DIR = os.getenv("DATA_DIR", "data")
    ENV = os.getenv("ENV", "dev")

settings = Settings()
