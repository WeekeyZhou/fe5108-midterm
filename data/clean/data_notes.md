# Data Notes

How every file in `data/clean/` was built from `data/raw/`, and every cleaning decision we made.
All steps are coded in `src/data_prep.py`; settings are in `src/config.py`.

Owner: A. Last updated: 8 October 2026.

---

## 1. Summary

| Item | Choice |
|---|---|
| Universe | 25 large-cap U.S. stocks from the S&P 500, 2 to 3 per sector, all 11 GICS sectors |
| Frequency | Monthly |
| Sample | September 2016 to July 2026, **119 months** (handout minimum: 96) |
| Returns | Simple total returns (dividends and splits included), in decimals |
| Riskless rate | 1-month U.S. Treasury bill rate (`RF`, Ken French) |
| Main market proxy | U.S. value-weighted market excess return (`Mkt-RF`, Ken French) |
| Second market proxy | MSCI World, proxied by the iShares MSCI World ETF (URTH) |
| Extra factors | Size (`SMB`) and value (`HML`), Ken French |
| Currency | U.S. dollars throughout |

**Why this sample period.** The course-provided factor file covers 2016-09 to 2026-07. We matched the
stock data to it exactly so that every row of every file refers to the same month.

**Why these proxies.** Ken French's market return and T-bill rate are the standard choices for U.S.
equities, are already total returns, and come from the same file as the size and value factors, so all
three stages use one consistent source. MSCI World covers 23 developed markets, so it is a broader
(but still incomplete) stand-in for the "true" market portfolio, which is what Stage 4 needs.

---

## 2. Raw files (`data/raw/`, never edited)

| File | Source | Downloaded | Shape | Content |
|---|---|---|---|---|
| `ff3_monthly.csv` | Ken French Data Library, provided by the course | provided | 119 rows x 5 cols | `Date`, `Mkt-RF`, `SMB`, `HML`, `RF`; monthly, **already in decimals** |
| `stock_prices.csv` | Yahoo Finance via `yfinance` | 2026-10-08 | 2,514 trading days x 25 stocks | Daily adjusted close, 2016-08-01 to 2026-07-31 |
| `urth_prices.csv` | Yahoo Finance via `yfinance` | 2026-10-08 | 2,514 trading days x 1 | Daily adjusted close of URTH, same dates |
| `stock_shares.csv` | Yahoo Finance via `yfinance` | 2026-10-08 | 25 rows | Market cap and shares outstanding per stock, as of the download date |

Prices start in August 2016, one month before the sample, because the first monthly return
(September 2016) needs the August month-end price.

The raw files are committed to the repository, so the code never needs the internet again:
`download()` skips any file that already exists.

---

## 3. From raw to clean, step by step

### 3.1 `stock_returns.csv` (from `stock_prices.csv`)

1. **Use adjusted prices.** Downloaded with `auto_adjust=True`, so Yahoo has already adjusted every
   past price for cash dividends and stock splits. A return computed from these prices is therefore a
   **total return** (price change plus reinvested dividends). This is the handout's
   "dividend / total-return adjustment".
2. **Daily to month-end.** For each stock and each calendar month, keep the price on the **last trading
   day** of that month. Result: 120 month-end prices (2016-08 to 2026-07).
3. **Monthly simple return.** `r_t = P_t / P_{t-1} - 1`, where `P_t` is the month-end price of month t.
   The first month (2016-08) has no previous price and is dropped, leaving 119 returns.
4. **Date format.** Index rewritten as `YYYY-MM` (e.g. `2016-09`) to match the factor file exactly.
5. **Trim to sample.** Keep 2016-09 to 2026-07.

Output: **119 rows x 25 columns**, one column per ticker, decimals (0.012 = 1.2%).

### 3.2 `factors.csv` (from `ff3_monthly.csv` and `urth_prices.csv`)

1. **Read the course file as is.** Values are already decimals (e.g. `RF` ranges from 0.0000 to 0.0048
   per month), so **no division by 100**. Dividing again would be a factor-of-100 error.
2. **Rename columns** to lower case for code: `Mkt-RF` -> `mkt_rf`, `SMB` -> `smb`, `HML` -> `hml`,
   `RF` -> `rf`, `Date` -> `date`.
3. **URTH monthly return.** Same procedure as 3.1 (adjusted daily price -> month-end price -> simple
   return -> `YYYY-MM`), stored as column `msci_world`.
4. **Join on `date`.** The two sources are merged month by month.

Output: **119 rows x 5 columns**.

| Column | Meaning | Is RF already subtracted? |
|---|---|---|
| `mkt_rf` | U.S. market excess return (main proxy) | **Yes** |
| `smb` | Small minus big (size factor) | Not applicable (long-short return) |
| `hml` | High minus low book-to-market (value factor) | Not applicable (long-short return) |
| `rf` | 1-month T-bill return | n/a |
| `msci_world` | MSCI World return via URTH (second proxy) | **No**. Use `msci_world - rf` |

### 3.3 `market_caps.csv` (from `stock_shares.csv`)

1. Take each stock's market cap (`marketCap` field from Yahoo).
2. Add the sector label from `config.py`.
3. **Value weight** = stock's market cap / sum of the 25 market caps. Weights sum to 1 and are
   **within our 25 stocks only**, not their weight in the S&P 500.

Output: **25 rows**: `ticker`, `sector`, `market_cap`, `value_weight`, `download_date`.

Why market cap and not shares x price: Alphabet has several share classes. Yahoo's
`sharesOutstanding` for GOOGL counts only Class A shares, which would understate the company's size by
about half; Yahoo's `marketCap` covers the whole company. We checked this: GOOGL's `marketCap` is about
twice its Class A shares times price, while for the other 24 stocks the two are close.

---

## 4. Conventions for everyone

- All returns are **monthly decimals**. Never mix in percentages.
- Excess return of a stock = stock return - `rf` (compute it in your own script).
- Raw U.S. market return = `mkt_rf + rf`.
- Annualise only for display: mean x 12, standard deviation x sqrt(12).
- Read data only from `data/clean/`, using the paths in `config.py`.

---

## 5. Quality checks (run automatically by `clean()`)

| Check | Result |
|---|---|
| Months in each file | 119, identical dates in all files |
| Missing values | 0 in raw prices, 0 in clean files |
| `rf` in decimals | Yes, 0.0000 to 0.0048 per month |
| Monthly returns above 50% in absolute value | None. Largest: NVDA +38.5% (2017-05), UNH +36.9% (2026-04), NVDA +36.3% (2023-05). Moves of this size are plausible for these stocks and are kept |
| Correlation of each stock with the market | All positive, 0.26 to 0.74 |
| Correlation of `msci_world` with U.S. market | 0.98 |
| Value weights | Sum to 1.0000 |

---

## 6. Approximations and limitations

1. **Survivorship bias.** The 25 stocks are chosen from **today's** S&P 500 and followed back ten
   years. Firms that shrank, failed or left the index over the period cannot appear in the sample.
   Direction of the bias: average returns are **overstated**, and the universe looks more successful
   than an investor in 2016 could have known. For Stage 1 this inflates estimated means and the
   tangency portfolio's Sharpe ratio; for Stage 2 it can raise average returns and alphas, making the
   SML look better (or worse, if it lifts low-beta winners) than with a point-in-time universe. We did
   not have historical index constituents, so we acknowledge rather than correct the bias.
2. **Market caps are dated 2026-10-08**, about ten weeks after the sample ends (2026-07). Value weights
   therefore reflect October 2026 prices, not July 2026. Relative sizes move little over ten weeks, so
   the effect on Stage 1 is small.
3. **URTH is a fund, not the index.** Its return equals MSCI World's minus a small expense ratio
   (0.24% per year) and tracking error. URTH also holds about 70% U.S. stocks, which is why its
   correlation with the U.S. market is 0.98. This matters for interpreting Stage 4.
4. **Yahoo adjustments are taken as given.** Splits and dividends are adjusted by Yahoo. Other corporate
   actions (for example spin-offs) are adjusted less reliably. No monthly return looked suspicious
   (see section 5), so we made no manual corrections.
5. **Month-end prices** use the last trading day of each month, which may differ from the exact dates
   Ken French uses by a day. The effect on monthly returns is negligible.

---

## 7. Items checked and not applicable

| Handout item | Status |
|---|---|
| **Currency** | Not applicable: all stocks, URTH and the factor data are in U.S. dollars |
| **Delistings** | Not applicable: all 25 stocks traded for the whole sample (a consequence of the survivorship bias in 6.1) |
| **Dividends / total return** | Handled by adjusted prices (3.1) |
| **Weekly data** | Not used. Monthly only, as recommended by the handout |
