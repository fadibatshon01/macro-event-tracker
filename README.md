# Macro Event Impact Tracker
A Python pipeline that tracks how US macroeconomic releases (starting with CPI) move the equity market. It pulls historical CPI events, downloads price data for a chosen symbol (e.g. SPY), and computes before/after returns around each release, including surprise vs. market reaction. Results are saved as a clean CSV and a chart for quick analysis or reporting.

## Features
- Loads CPI YoY releases from data/raw/us_cpi_events.csv and parses timestamps, actual values, and consensus forecasts.
- Downloads daily price history via yfinance and cleans close prices (handles multi-index formats).
- Builds event windows around CPI releases (±5 days) and computes before/after returns.
- Computes CPI “surprise” = actual − consensus and relates it to market reaction.
- Saves a full CPI reaction table to data/processed/cpi_reactions_spy.csv.
- Produces PNG charts showing after-event returns vs CPI surprise at data/processed/cpi_surprise_vs_return_spy.png.
- Includes a one-command pipeline using: python -m src.main.

## Project Structure
macro-event-tracker/
├── config.yml  
├── data/  
│   ├── raw/  
│   │   └── us_cpi_events.csv  
│   └── processed/  
│       ├── cpi_reactions_spy.csv  
│       └── cpi_surprise_vs_return_spy.png  
├── src/  
│   ├── config.py  
│   ├── macro_events.py  
│   ├── market_data.py  
│   ├── event_window.py  
│   ├── cpi_reactions.py  
│   ├── visualize.py  
│   └── main.py  
├── requirements.txt  
└── README.md

## Setup
git clone https://github.com/fadibatshon01/macro-event-tracker.git  
cd macro-event-tracker  
python -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  

Example config.yml:
data:
  cpi_events_path: "data/raw/us_cpi_events.csv"
market:
  symbols:
    - "SPY"
window:
  days_before: 5
  days_after: 5

## Usage
Run the entire pipeline:
python -m src.main

This generates:
- data/processed/cpi_reactions_spy.csv
- data/processed/cpi_surprise_vs_return_spy.png

Or run components individually:
python -m src.cpi_reactions  
python -m src.visualize  
python -m src.event_window  

## Tech Stack
Python, pandas, yfinance, matplotlib, PyYAML, GitHub.