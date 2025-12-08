from datetime import timedelta

import pandas as pd

from .macro_events import load_cpi_events
from .market_data import get_daily_history


def get_event_window_prices(
    symbol: str,
    event_time,
    days_before: int = 5,
    days_after: int = 5,
) -> pd.DataFrame:
    """
    Get daily prices for a symbol in a window around a macro event.
    """
    start = event_time - timedelta(days=days_before)
    end = event_time + timedelta(days=days_after)

    prices = get_daily_history(symbol, start, end)

    # Ensure there's a 'date' column
    if "date" not in prices.columns:
        if isinstance(prices.index, pd.DatetimeIndex):
            prices = prices.reset_index().rename(columns={"index": "date", "Date": "date"})

    # Sort by date and reset index
    prices = prices.sort_values("date").reset_index(drop=True)
    return prices


def _get_close_series(prices: pd.DataFrame) -> pd.Series:
    """
    Robustly extract a 1D Close price series even if columns are multi-indexed.
    """
    # Case 1: simple 'Close' column exists
    if "Close" in prices.columns:
        obj = prices["Close"]
    else:
        # Case 2: multi-index or weird columns: find anything whose last level/name is 'Close'
        close_col = None
        for col in prices.columns:
            if isinstance(col, tuple):
                if col[-1] == "Close":
                    close_col = col
                    break
            else:
                if str(col).lower() == "close":
                    close_col = col
                    break
        if close_col is None:
            raise KeyError("Could not find a 'Close' column in price data.")
        obj = prices[close_col]

    # If it's a DataFrame with one column, squeeze to Series
    if isinstance(obj, pd.DataFrame):
        if obj.shape[1] == 1:
            obj = obj.iloc[:, 0]
        else:
            raise ValueError("Close data has more than one column; cannot reduce to a single series.")

    return pd.to_numeric(obj, errors="coerce")


def compute_before_after_returns(prices: pd.DataFrame, event_time) -> dict:
    """
    Compute simple returns before and after the event date.

    - 'before_return': from first available date to event date
    - 'after_return': from event date to last available date
    """
    # Ensure 'date' is datetime
    prices["date"] = pd.to_datetime(prices["date"])

    # Get a clean 1D Close series
    close = _get_close_series(prices)

    event_date = event_time.date()

    # Find the row for the event's calendar date
    event_rows = prices.loc[prices["date"].dt.date == event_date]
    if event_rows.empty:
        raise ValueError(f"No price data found for event date {event_date}.")

    event_idx = event_rows.index[0]

    # Extract scalar floats (no warnings)
    first_close = float(close.iloc[0])
    event_close = float(close.iloc[event_idx])
    last_close = float(close.iloc[-1])

    before_return = (event_close / first_close) - 1.0
    after_return = (last_close / event_close) - 1.0

    # Dates for pretty printing
    first_date = prices["date"].iloc[0]
    last_date = prices["date"].iloc[-1]

    return {
        "event_date": event_date,
        "first_date": first_date.date(),
        "last_date": last_date.date(),
        "before_return": before_return,
        "after_return": after_return,
    }


if __name__ == "__main__":
    # Manual test: run a single event window
    events = load_cpi_events()
    first_event = events.iloc[0]
    event_time = first_event["timestamp"]

    symbol = "SPY"

    print(f"Using event: {first_event['event']} at {event_time}")

    prices = get_event_window_prices(symbol, event_time, days_before=5, days_after=5)
    print(f"\nPrice window for {symbol}:")
    print(prices[["date"] + [col for col in prices.columns if 'Close' in str(col)]])

    stats = compute_before_after_returns(prices, event_time)

    print("\n=== Return Summary ===")
    print(f"Symbol: {symbol}")
    print(f"Window: {stats['first_date']} → {stats['last_date']}")
    print(f"Event date: {stats['event_date']}")
    print(f"Return before event: {stats['before_return'] * 100:.2f}%")
    print(f"Return after event:  {stats['after_return'] * 100:.2f}%")
