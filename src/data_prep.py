"""
Download and clean all data for the project.

Run from the project folder:
    python src/data_prep.py

Step 1  download()  needs internet. Saves Data 1-3 to data/raw/.
                    Skips any file that already exists, so it only downloads once.
Step 2  clean()     no internet. Reads data/raw/, writes data/clean/.

Owner: A
"""
import time
from datetime import date

import pandas as pd
import yfinance as yf

from config import (
    TICKERS, UNIVERSE, SECOND_PROXY,
    DOWNLOAD_START, DOWNLOAD_END, SAMPLE_START, SAMPLE_END,
    RAW_DIR, CLEAN_DIR,
    RAW_FF3, RAW_STOCK_PRICES, RAW_STOCK_SHARES, RAW_URTH_PRICES,
    STOCK_RETURNS, FACTORS, MARKET_CAPS,
)


# ===========================================================================
# Step 1: download
# ===========================================================================
def _download_prices(tickers, retries=3):
    """Daily adjusted close prices (dividends and splits included)."""
    for attempt in range(1, retries + 1):
        data = yf.download(
            tickers, start=DOWNLOAD_START, end=DOWNLOAD_END,
            auto_adjust=True, progress=False, threads=False,
        )
        if not data.empty:
            prices = data["Close"]
            if isinstance(prices, pd.Series):          # single ticker
                prices = prices.to_frame(tickers[0])
            prices.index.name = "date"
            return prices[tickers]                     # keep config order
        print(f"  Empty result (attempt {attempt}/{retries}), waiting 30 s...")
        time.sleep(30)
    raise RuntimeError("Yahoo returned no data. Wait a few minutes and run again.")


def _download_market_caps():
    """Current market cap for each stock (as of today)."""
    rows = []
    for t in TICKERS:
        info = yf.Ticker(t).info
        rows.append({
            "ticker": t,
            "market_cap": info.get("marketCap"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "download_date": date.today().isoformat(),
        })
        print(f"  {t}: market cap = {info.get('marketCap')}")
        time.sleep(1)                                   # be gentle with Yahoo
    return pd.DataFrame(rows)


def download():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # Data 1: 25 stock prices
    if RAW_STOCK_PRICES.exists():
        print(f"[skip] {RAW_STOCK_PRICES.name} already exists")
    else:
        print("Downloading Data 1: stock prices...")
        _download_prices(TICKERS).to_csv(RAW_STOCK_PRICES)
        print(f"  saved {RAW_STOCK_PRICES.name}")

    # Data 2: 25 market caps
    if RAW_STOCK_SHARES.exists():
        print(f"[skip] {RAW_STOCK_SHARES.name} already exists")
    else:
        print("Downloading Data 2: market caps...")
        _download_market_caps().to_csv(RAW_STOCK_SHARES, index=False)
        print(f"  saved {RAW_STOCK_SHARES.name}")

    # Data 3: URTH prices
    if RAW_URTH_PRICES.exists():
        print(f"[skip] {RAW_URTH_PRICES.name} already exists")
    else:
        print("Downloading Data 3: URTH prices...")
        _download_prices([SECOND_PROXY]).to_csv(RAW_URTH_PRICES)
        print(f"  saved {RAW_URTH_PRICES.name}")


# ===========================================================================
# Step 2: clean
# ===========================================================================
def _monthly_returns(path):
    """Daily prices -> month-end prices -> monthly simple returns, index 'YYYY-MM'."""
    prices = pd.read_csv(path, index_col="date", parse_dates=True)
    month_end = prices.groupby(prices.index.to_period("M")).last()
    returns = month_end.pct_change().iloc[1:]           # first month has no return
    returns.index = returns.index.strftime("%Y-%m")
    returns.index.name = "date"
    return returns.loc[SAMPLE_START:SAMPLE_END]


def clean():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    if not RAW_FF3.exists():
        raise FileNotFoundError(f"Put the course file ff3_monthly.csv in {RAW_DIR}")

    # Stock returns (from Data 1)
    stocks = _monthly_returns(RAW_STOCK_PRICES)[TICKERS]

    # Factors (course file, already in decimals) + URTH returns (from Data 3)
    ff = pd.read_csv(RAW_FF3, dtype={"Date": str})
    ff = ff.rename(columns={"Date": "date", "Mkt-RF": "mkt_rf",
                            "SMB": "smb", "HML": "hml", "RF": "rf"})
    ff = ff.set_index("date").loc[SAMPLE_START:SAMPLE_END]
    urth = _monthly_returns(RAW_URTH_PRICES)[SECOND_PROXY].rename("msci_world")
    factors = ff.join(urth, how="left")

    # Market caps and value weights (from Data 2)
    caps = pd.read_csv(RAW_STOCK_SHARES)
    caps.insert(1, "sector", caps["ticker"].map(UNIVERSE))
    caps["value_weight"] = caps["market_cap"] / caps["market_cap"].sum()
    caps = caps[["ticker", "sector", "market_cap", "value_weight", "download_date"]]

    _check(stocks, factors, caps)

    stocks.to_csv(STOCK_RETURNS)
    factors.to_csv(FACTORS)
    caps.to_csv(MARKET_CAPS, index=False)
    print(f"\nSaved to {CLEAN_DIR}:")
    print(f"  {STOCK_RETURNS.name}  {stocks.shape}")
    print(f"  {FACTORS.name}        {factors.shape}")
    print(f"  {MARKET_CAPS.name}    {caps.shape}")


def _check(stocks, factors, caps):
    """Stop with a clear message if anything looks wrong."""
    print("\nChecks:")
    n = len(pd.period_range(SAMPLE_START, SAMPLE_END, freq="M"))

    assert len(stocks) == n, f"stock_returns has {len(stocks)} rows, expected {n}"
    assert len(factors) == n, f"factors has {len(factors)} rows, expected {n}"
    assert list(stocks.index) == list(factors.index), "Dates do not line up"
    print(f"  OK  {n} months, dates aligned ({SAMPLE_START} to {SAMPLE_END})")

    missing = stocks.isna().sum().sum() + factors.isna().sum().sum()
    if missing:
        print("  !!  Missing values:")
        print(stocks.isna().sum()[lambda s: s > 0])
        print(factors.isna().sum()[lambda s: s > 0])
        raise ValueError("Fix missing values before continuing")
    print("  OK  no missing values")

    assert factors["rf"].between(0, 0.01).all(), "rf out of range: check units"
    print("  OK  rf is in decimals (monthly, between 0 and 1%)")

    long = stocks.stack()
    big = long[long.abs() > 0.5]
    if len(big):
        print("  !!  Monthly returns above 50% (check by hand, record in data_notes.md):")
        print(big.to_string())
    else:
        print("  OK  no monthly return above 50%")

    corr = stocks.corrwith(factors["mkt_rf"] + factors["rf"])
    print(f"  OK  correlation with market: min {corr.min():.2f}, max {corr.max():.2f}")

    assert caps["market_cap"].notna().all(), "Some market caps are missing"
    print(f"  OK  25 market caps, value weights sum to {caps['value_weight'].sum():.4f}")


if __name__ == "__main__":
    download()
    clean()
