# FE5108 Midterm Group Project

FE5108 Portfolio Theory and Investments · NUS Risk Management Institute · October 2026

**Report:** [`report/FE5108_final_report.pdf`](report/FE5108_final_report.pdf)

---

## 1. How to run

From the project folder:

```bash
pip install -r requirements.txt
python run_all.py
```

`run_all.py` is the single entry point. It runs the five scripts below in order and reproduces every
table and figure in the report (about 15 seconds). No internet connection is needed: the raw data
are included in `data/raw/`, so the download step is skipped.

## 2. Pipeline

```
data/raw/  ──►  src/data_prep.py  ──►  data/clean/  ──►  src/stage1_portfolio.py ─┐
                                                         src/stage2_capm.py ──────┤
                                                         src/stage3_factors.py ───┼──►  output/figures/
                                                         src/stage4_roll.py ──────┘     output/tables/
```

| Step | Script | Input | Output |
|---|---|---|---|
| 1 | `src/data_prep.py` | `data/raw/` | `data/clean/` |
| 2 | `src/stage1_portfolio.py` | `data/clean/` | Stage 1 exhibits (1a–1c) |
| 3 | `src/stage2_capm.py` | `data/clean/` | Stage 2 exhibits (2a–2e) |
| 4 | `src/stage3_factors.py` | `data/clean/`, Stage 2 results | Stage 3 exhibits (3a–3b) |
| 5 | `src/stage4_roll.py` | `data/clean/`, functions from `stage2_capm.py` | Stage 4 exhibits |

All scripts read their settings (tickers, sample period, file paths, chart style) from
`src/config.py`. Each script can also be run on its own, e.g. `python src/stage2_capm.py`.

## 3. Directory structure

```
fe5108-midterm/
├── README.md
├── requirements.txt
├── run_all.py                         Single entry point
│
├── data/
│   ├── raw/                           Original data, never edited
│   │   ├── ff3_monthly.csv              Ken French 3 factors and RF (course-provided)
│   │   ├── stock_prices.csv             Daily adjusted close prices, 25 stocks (Yahoo Finance)
│   │   ├── stock_shares.csv             Market caps, 25 stocks (Yahoo Finance)
│   │   └── urth_prices.csv              Daily adjusted close, iShares MSCI World ETF (Yahoo Finance)
│   └── clean/                         Created by data_prep.py
│       ├── stock_returns.csv            Monthly returns, 25 stocks
│       ├── factors.csv                  Market, SMB, HML, RF, MSCI World
│       ├── market_caps.csv              Market caps and value weights
│       └── data_notes.md                Data sources and cleaning decisions
│
├── src/
│   ├── config.py                      Shared settings
│   ├── data_prep.py                   Step 1 · Data download and cleaning
│   ├── stage1_portfolio.py            Step 2 · Stage 1
│   ├── stage2_capm.py                 Step 3 · Stage 2
│   ├── stage3_factors.py              Step 4 · Stage 3
│   └── stage4_roll.py                 Step 5 · Stage 4
│
├── output/                            Created by the stage scripts
│   ├── figures/                       Figures (.png)
│   └── tables/                        Tables (.csv, .html)
│
└── report/
    ├── FE5108_final_report.pdf        Final report
    ├── final_report.md                Source of the final report
    └── …                              Section drafts and signatures
```

## 4. Report exhibits and their source files

| Exhibit | Output file(s) | Script |
|---|---|---|
| 1a | `output/tables/tab_1a_summary_statistics.html` | `stage1_portfolio.py` |
| 1b | `output/figures/fig_1b_weights.png`, `output/tables/tab_1b_portfolio_weights.html` | `stage1_portfolio.py` |
| 1c | `output/tables/tab_1c_portfolio_diagnostics.html`, `output/tables/tab_1_main_diagnostics.html` | `stage1_portfolio.py` |
| 2a | `output/figures/tab_2a_capm.png`, `output/tables/tab_2a_capm.csv` | `stage2_capm.py` |
| 2b | `output/figures/fig_2b_sml.png` | `stage2_capm.py` |
| 2c | `output/figures/tab_2c_alpha_tests.png`, `output/tables/tab_2c_alpha_tests.csv` | `stage2_capm.py` |
| 2d | `output/tables/tab_2d_sml.csv` | `stage2_capm.py` |
| 2e | `output/figures/tab_2e_robustness.png`, `output/tables/tab_2e_robustness.csv` | `stage2_capm.py` |
| 3a | `output/tables/tab_3a_ff3.csv` | `stage3_factors.py` |
| 3b | `output/figures/fig_3b_alpha_comparison.png`, `output/tables/tab_3b_alpha_comparison.csv` | `stage3_factors.py` |
| 4 | `output/figures/fig_4_sml_proxy_robustness.png`, `output/tables/stage4_proxy_comparison.csv`, `output/tables/stage4_sml_robustness.csv` | `stage4_roll.py` |

## 5. Data files

| File | Source | Coverage |
|---|---|---|
| `data/raw/ff3_monthly.csv` | Ken French Data Library (course-provided) | 2016-09 to 2026-07, monthly |
| `data/raw/stock_prices.csv` | Yahoo Finance via `yfinance`, downloaded 8 Oct 2026 | 2016-08-01 to 2026-07-31, daily |
| `data/raw/stock_shares.csv` | Yahoo Finance via `yfinance`, downloaded 8 Oct 2026 | As of 8 Oct 2026 |
| `data/raw/urth_prices.csv` | Yahoo Finance via `yfinance`, downloaded 8 Oct 2026 | 2016-08-01 to 2026-07-31, daily |

Cleaning steps are documented in [`data/clean/data_notes.md`](data/clean/data_notes.md).

## 6. Package versions

Minimum versions are listed in `requirements.txt`. The full pipeline was tested on 16 Oct 2026 with:

| Package | Version |
|---|---|
| Python | 3.13 |
| pandas | 3.0.5 |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| statsmodels | 0.15.0 |
| matplotlib | 3.11.2 |
| yfinance | 1.7.0 (only used if `data/raw/` is deleted and the data are re-downloaded) |
