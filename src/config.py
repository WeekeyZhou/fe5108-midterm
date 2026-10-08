"""
Shared settings for the whole project.

Everyone imports from this file, e.g.
    from config import TICKERS, CLEAN_DIR, apply_plot_style

To change the sample period or the stock list, edit it HERE only.
Owner: A
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Folder paths (work on any computer, no need to edit)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]      # the fe5108-midterm folder
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "clean"
FIG_DIR = ROOT / "output" / "figures"
TAB_DIR = ROOT / "output" / "tables"

# ---------------------------------------------------------------------------
# 2. Sample period
#    Set by the course-provided Ken French file: 2016-09 to 2026-07 (119 months)
# ---------------------------------------------------------------------------
SAMPLE_START = "2016-09"        # first monthly return
SAMPLE_END = "2026-07"          # last monthly return

# Price download window: start one month early (to compute the first return);
# yfinance treats `end` as exclusive, so use the first day after the sample.
DOWNLOAD_START = "2016-08-01"
DOWNLOAD_END = "2026-08-01"

# ---------------------------------------------------------------------------
# 3. Investment universe: 25 S&P 500 stocks, covering all 11 sectors
# ---------------------------------------------------------------------------
UNIVERSE = {
    "AAPL": "Information Technology",
    "MSFT": "Information Technology",
    "NVDA": "Information Technology",
    "JPM": "Financials",
    "BAC": "Financials",
    "JNJ": "Health Care",
    "UNH": "Health Care",
    "PFE": "Health Care",
    "AMZN": "Consumer Discretionary",
    "HD": "Consumer Discretionary",
    "MCD": "Consumer Discretionary",
    "PG": "Consumer Staples",
    "KO": "Consumer Staples",
    "WMT": "Consumer Staples",
    "XOM": "Energy",
    "CVX": "Energy",
    "CAT": "Industrials",
    "HON": "Industrials",
    "UNP": "Industrials",
    "GOOGL": "Communication Services",
    "VZ": "Communication Services",
    "NEE": "Utilities",
    "DUK": "Utilities",
    "SHW": "Materials",
    "AMT": "Real Estate",
}
TICKERS = list(UNIVERSE.keys())

# Second market proxy for Stage 4 (Roll's critique): MSCI World via its ETF
SECOND_PROXY = "URTH"

# ---------------------------------------------------------------------------
# 4. File names
# ---------------------------------------------------------------------------
# Raw (downloaded once, never edited)
RAW_FF3 = RAW_DIR / "ff3_monthly.csv"           # provided by the course
RAW_STOCK_PRICES = RAW_DIR / "stock_prices.csv" # Data 1
RAW_STOCK_SHARES = RAW_DIR / "stock_shares.csv" # Data 2
RAW_URTH_PRICES = RAW_DIR / "urth_prices.csv"   # Data 3

# Clean (everyone reads these)
STOCK_RETURNS = CLEAN_DIR / "stock_returns.csv" # 119 rows x 25 stocks
FACTORS = CLEAN_DIR / "factors.csv"             # mkt_rf, smb, hml, rf, msci_world
MARKET_CAPS = CLEAN_DIR / "market_caps.csv"     # 25 rows, incl. value_weight

# ---------------------------------------------------------------------------
# 5. Conventions (read before you write code)
#   - All returns are DECIMALS (0.012 = 1.2%) and MONTHLY. Never use percent.
#   - Dates are "YYYY-MM" strings, e.g. "2016-09".
#   - Excess return = stock return - rf. Compute it yourself.
#   - mkt_rf is ALREADY an excess return. Raw market return = mkt_rf + rf.
#   - msci_world is a RAW return. Subtract rf before using it in a regression.
#   - Annualise only for display: mean x 12, std x sqrt(12).
# ---------------------------------------------------------------------------
MONTHS_PER_YEAR = 12

# ---------------------------------------------------------------------------
# 6. One chart style for the whole report
# ---------------------------------------------------------------------------
COLORS = {
    "main": "#1f4e79",      # dark blue: main series
    "second": "#c55a11",    # orange: comparison series
    "neutral": "#7f7f7f",   # grey: theory lines, reference lines
}
FIG_SIZE = (7, 4.5)
FIG_DPI = 200


def apply_plot_style():
    """Call once at the top of your script, before plotting."""
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.figsize": FIG_SIZE,
        "savefig.dpi": FIG_DPI,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
    })
