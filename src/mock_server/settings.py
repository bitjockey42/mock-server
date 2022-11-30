import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path().cwd()
DEFAULT_DATA_DIR = BASE_DIR.joinpath("data")
DATA_DIR = Path(os.getenv("DATA_DIR", DEFAULT_DATA_DIR)).resolve()

if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)

BASE_API_PATH = os.getenv("BASE_API_PATH", "")
DATA_STRATEGY = os.getenv("DATA_STRATEGY", "from_request")
DEFAULT_DATA_FORMAT = os.getenv("DEFAULT_DATA_FORMAT", "json")
