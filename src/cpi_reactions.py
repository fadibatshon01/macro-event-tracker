from __future__ import annotations

from pathlib import Path
import pandas as pd

from .config import load_config
from .macro_events import load_cpi_events
from .event_window import get_event_window_prices, compute_before_after_returns


def _project_root() -> Path:
    """Return the project root directory (one level above src)."""
    return Path(__file__).resolve().parents[1]


def _get_processed_path(symbol: str) -> Path:
    """Return the path where the CPI reaction table CSV will be saved."""
    cfg = load_config()
    processed_dir = cfg["paths"]["processed_dir"]
    return _project_root() / processed_dir / f"cpi_reactions_{symbol.lower()}.csv"


def build_cpi_reaction_table(
    symbol: str = "SPY",
    days_before: int = 5,
    days_after: int = 5,
) -> pd.DataFrame:
    """
    For each CPI event in the local CSV, build an event-study table with:
      - event timestamp
      - actual / consensus CPI
      - surprise (actual - consensus)
      - before-event return (%)
      - after-event return (%)
    """
    events = load_cpi_events()

    rows: list[dict] = []

    for _, row in events.iterrows():
        try:
            event_time = row["event_timestamp"]
        except KeyError:
            # Fallback if someone accidentally named the column differently
            for cand in ["timestamp", "date", "event_time"]:
                if cand in row.index:
                    event_time = row[cand]
                    break
            else:
                print("Skipping row with no recognizable timestamp column.")
                continue

        try:
            actual = float(row["actual"])
            consensus = float(row["consensus"])
        except Exception:
            # Skip rows with bad numeric values
            print(f"Skipping event at {event_time} due to invalid actual/consensus.")
            continue

        surprise = actual - consensus

        try:
            prices = get_event_window_prices(
                symbol=symbol,
                event_time=event_time,
                days_before=days_before,
                days_after=days_after,
            )
            stats = compute_before_after_returns(prices, event_time)
        except Exception as e:
            print(f"Skipping event at {event_time} due to error: {e}")
            continue

        rows.append(
            {
                "symbol": symbol,
                "event": row.get("event", "CPI_YoY"),
                "event_timestamp": event_time,
                "actual": actual,
                "consensus": consensus,
                "surprise": surprise,
                "before_return_pct": stats["before_return"] * 100.0,
                "after_return_pct": stats["after_return"] * 100.0,
            }
        )

    table = pd.DataFrame(rows)
    table = table.sort_values("event_timestamp").reset_index(drop=True)
    return table


def save_cpi_reaction_table(
    symbol: str = "SPY",
    days_before: int = 5,
    days_after: int = 5,
) -> Path:
    """
    Build the CPI reaction table and save it to data/processed/cpi_reactions_<symbol>.csv.
    Returns the path to the saved CSV.
    """
    table = build_cpi_reaction_table(
        symbol=symbol,
        days_before=days_before,
        days_after=days_after,
    )

    out_path = _get_processed_path(symbol)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_path, index=False)

    print(f"Saved CPI reaction table to: {out_path}")
    return out_path


if __name__ == "__main__":
    # Quick manual test
    df = build_cpi_reaction_table(symbol="SPY", days_before=5, days_after=5)
    print(df.tail())
    print(f"\nBuilt CPI reaction table with {len(df)} rows.")
