import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path().cwd()
DATA_DIR = BASE_DIR.joinpath("data")

print(DATA_DIR)

if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)

BASE_API_PATH = os.getenv("BASE_API_PATH", "")
DATA_STRATEGY = os.getenv("DATA_STRATEGY", "from_request")