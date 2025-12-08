from pathlib import Path
import yaml

# Path to the config.yml file (one level above /src)
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yml"


def load_config():
    """Load the YAML config file as a Python dictionary."""
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    cfg = load_config()
    print(cfg)
