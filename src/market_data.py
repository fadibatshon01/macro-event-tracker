from datetime import timedelta
import pandas as pd
import yfinance as yf

from .macro_events import load_cpi_events


def get_daily_history(symbol: str, start, end) -> pd.DataFrame:
    """
    Download daily price history for a given symbol between start and end dates.
    Uses yfinance with auto-adjusted prices.
    """
    data = yf.download(
        symbol,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    # Put the date index into a normal column
    data = data.rename_axis("date").reset_index()
    return data


if __name__ == "__main__":
    # 1) Load CPI events
    events = load_cpi_events()
    first_event = events.iloc[0]

    event_time = first_event["timestamp"]

    # 2) Define a window around the event (5 days before and after)
    start = event_time - timedelta(days=5)
    end = event_time + timedelta(days=5)

    # 3) Fetch SPY prices in that window
    symbol = "SPY"
    prices = get_daily_history(symbol, start, end)

    print(f"Event: {first_event['event']} at {event_time}")
    print(f"\nDaily prices for {symbol} from {start.date()} to {end.date()}:\n")
    print(prices)
