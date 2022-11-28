import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR.joinpath("data")

if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)

BASE_API_PATH = os.getenv("BASE_API_PATH", "")
DATA_STRATEGY = os.getenv("DATA_STRATEGY", "from_request")