import os

from dotenv import load_dotenv


load_dotenv()


BASE_API_PATH = os.getenv("BASE_API_PATH", "")
