from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    cfg = load_config()
    print(cfg)