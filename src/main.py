from pathlib import Path

from .cpi_reactions import save_cpi_reaction_table
from .visualize import plot_cpi_surprise_vs_return


def run_pipeline(symbol: str = "SPY") -> None:
    """
    End-to-end run:
    1) Build & save CPI reaction table
    2) Build & save CPI surprise vs after-return chart
    """
    print(f"Running macro event pipeline for symbol: {symbol}")

    csv_path = save_cpi_reaction_table(symbol=symbol, days_before=5, days_after=5)
    png_path = plot_cpi_surprise_vs_return(symbol=symbol)

    print("\n=== Pipeline Outputs ===")
    print(f"- Reaction table CSV:  {csv_path}")
    print(f"- Reaction chart PNG:  {png_path}")
    print("\nDone.")


if __name__ == "__main__":
    # For now we hardcode SPY. Later we can parse CLI args.
    run_pipeline(symbol="SPY")
