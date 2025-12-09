from pathlib import Path
import os

import yaml
from dotenv import load_dotenv


# Load environment variables from .env (API keys, etc.)
load_dotenv()


# Path to config.yml at project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "config.yml"


def load_config() -> dict:
    """Load YAML config as a dictionary."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)

    return cfg


def get_env_key(var_name: str) -> str:
    """Return environment variable or raise a clear error if missing."""
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(
            f"Environment variable '{var_name}' is not set. "
            f"Add it to your .env file in the project root."
        )
    return value
