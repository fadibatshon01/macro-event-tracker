from pathlib import Path
import pandas as pd


# Path to the raw data folder
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def load_cpi_events(csv_name: str = "us_cpi_events.csv") -> pd.DataFrame:
    """
    Load US CPI event data from a CSV file.

    Returns a DataFrame with a combined 'timestamp' column.
    """
    csv_path = DATA_DIR / csv_name
    df = pd.read_csv(csv_path)

    # Combine date + time into a single datetime column
    df["timestamp"] = pd.to_datetime(df["date"] + " " + df["time"], format="%Y-%m-%d %H:%M")

    # Sort by time just to be safe
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


if __name__ == "__main__":
    events = load_cpi_events()
    print(events.head())
    print("\nColumns:", events.columns.tolist())
