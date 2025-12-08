from pathlib import Path
import pandas as pd

from .macro_events import load_cpi_events
from .event_window import get_event_window_prices, compute_before_after_returns


def build_cpi_reaction_table(
    symbol: str = "SPY",
    days_before: int = 5,
    days_after: int = 5,
) -> pd.DataFrame:
    """
    Loop over all CPI events and compute before/after returns for each.
    Returns a DataFrame summary.
    """
    events = load_cpi_events()

    rows = []

    for _, row in events.iterrows():
        event_time = row["timestamp"]

        try:
            # Get price window around this event
            prices = get_event_window_prices(symbol, event_time, days_before, days_after)

            # Compute before/after reactions
            stats = compute_before_after_returns(prices, event_time)
        except Exception as e:
            print(f"Skipping event at {event_time} due to error: {e}")
            continue

        # Compute macro surprise (actual - consensus), if available
        surprise = None
        try:
            actual = float(row["actual"])
            consensus = float(row["consensus"])
            surprise = actual - consensus
        except Exception:
            actual = row.get("actual", None)
            consensus = row.get("consensus", None)

        rows.append(
            {
                "symbol": symbol,
                "event": row["event"],
                "event_timestamp": event_time,
                "actual": actual,
                "consensus": consensus,
                "surprise": surprise,
                "before_return_pct": stats["before_return"] * 100,
                "after_return_pct": stats["after_return"] * 100,
            }
        )

    return pd.DataFrame(rows)


def save_cpi_reaction_table(
    symbol: str = "SPY",
    days_before: int = 5,
    days_after: int = 5,
    output_path: Path | None = None,
) -> Path:
    """
    Build the CPI reaction table and save it to CSV.
    Returns the path to the saved file.
    """
    table = build_cpi_reaction_table(symbol, days_before, days_after)

    if output_path is None:
        root = Path(__file__).resolve().parents[1]
        output_dir = root / "data" / "processed"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"cpi_reactions_{symbol.lower()}.csv"

    table.to_csv(output_path, index=False)
    print(f"Saved CPI reaction table to: {output_path}")
    return output_path


if __name__ == "__main__":
    # Build and display table
    table = build_cpi_reaction_table(symbol="SPY", days_before=5, days_after=5)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 120)
    pd.set_option("display.float_format", lambda x: f"{x:6.2f}")

    print("\n=== CPI Reaction Summary (SPY) ===")
    print(table)

    # Save to CSV in data/processed
    save_cpi_reaction_table(symbol="SPY", days_before=5, days_after=5)
