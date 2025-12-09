from pathlib import Path
import pandas as pd

from .config import load_config


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _get_raw_path() -> Path:
    cfg = load_config()
    raw_dir = cfg["paths"]["raw_dir"]
    return _project_root() / raw_dir / "us_cpi_events.csv"


def load_cpi_events() -> pd.DataFrame:
    """
    Load CPI event data from the local CSV file in data/raw.
    Expected columns:
    - event
    - event_timestamp
    - actual
    - consensus
    """
    csv_path = _get_raw_path()

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Expected CPI CSV not found at: {csv_path}\n"
            "Make sure us_cpi_events.csv exists in data/raw/"
        )

    df = pd.read_csv(csv_path, parse_dates=["event_timestamp"])
    df = df.sort_values("event_timestamp").reset_index(drop=True)

    return df


if __name__ == "__main__":
    events = load_cpi_events()
    print(events)
    print(f"\nLoaded {len(events)} CPI events from local CSV.")
