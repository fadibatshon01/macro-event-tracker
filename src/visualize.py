from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .cpi_reactions import build_cpi_reaction_table


def plot_cpi_surprise_vs_return(symbol: str = "SPY") -> Path:
    """
    Build CPI reaction table and plot surprise (actual - consensus)
    vs after-event return (%) for the given symbol.
    Saves the figure to data/processed and returns the path.
    """
    # Build the reaction table
    table = build_cpi_reaction_table(symbol=symbol)

    # Drop any rows without surprise or after_return
    table = table.dropna(subset=["surprise", "after_return_pct"])

    # Sort by event timestamp for nicer x-axis
    table = table.sort_values("event_timestamp").reset_index(drop=True)

    # x-axis labels (dates)
    x_labels = table["event_timestamp"].dt.date.astype(str)
    x = range(len(table))

    y = table["after_return_pct"]
    surprises = table["surprise"]

    # Create output directory
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"cpi_surprise_vs_return_{symbol.lower()}.png"

    # Plot
    plt.figure(figsize=(10, 5))
    plt.bar(x, y)  # simple bar chart of after-return %

    plt.axhline(0, linestyle="--", linewidth=1)  # zero line

    plt.title(f"{symbol} After-Event Return vs CPI Surprise")
    plt.xlabel("CPI Release Date")
    plt.ylabel("After-event return (%)")

    # Put event dates on x-axis
    plt.xticks(ticks=x, labels=x_labels, rotation=45, ha="right")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    print(f"Saved CPI surprise vs return chart to: {output_path}")
    return output_path


if __name__ == "__main__":
    plot_cpi_surprise_vs_return(symbol="SPY")
