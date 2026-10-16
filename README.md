# FE5108 Midterm Group Project

**From the Mutual-Fund Theorem to the Security Market Line: does the theory survive real data?**

NUS Risk Management Institute · FE5108 Portfolio Theory and Investments · October 2026

We test the theory chain from Weeks 1–6 (mean-variance choice, the mutual-fund theorem, CAPM, factor
models) on 25 large-cap U.S. stocks, using 119 monthly returns from September 2016 to July 2026.
The full write-up is [`report/FE5108_final_report.pdf`](report/FE5108_final_report.pdf).

---

## Quick start

Requires Python 3.10 or later. From the project folder:

```bash
pip install -r requirements.txt
python run_all.py
```

`run_all.py` runs the five scripts below in order and stops at the first error. It takes about
15 seconds and **needs no internet**: the raw data are included in `data/raw/`, so the download step
is skipped automatically. When it finishes it checks that all 16 report tables and figures exist.

| Step | Script | What it does | Writes to |
|---|---|---|---|
| 1 | `src/data_prep.py` | Raw prices and factors → clean monthly returns | `data/clean/` |
| 2 | `src/stage1_portfolio.py` | Stage 1: tangency vs value-weighted portfolio | `output/` |
| 3 | `src/stage2_capm.py` | Stage 2: CAPM regressions, SML, GRS test | `output/` |
| 4 | `src/stage3_factors.py` | Stage 3: Fama-French three-factor regressions | `output/` |
| 5 | `src/stage4_roll.py` | Stage 4: Roll's critique with MSCI World as market proxy | `output/` |

Each script can also be run on its own, e.g. `python src/stage2_capm.py`, as long as
`data/clean/` exists.

---

## Directory structure

```
fe5108-midterm/
│
├── README.md                          This file
├── requirements.txt                   Python packages
├── run_all.py                         Single entry point: reproduces every table and figure
│
├── data/
│   ├── raw/                           Original downloads. Never edited.
│   │   ├── ff3_monthly.csv              Ken French 3 factors + RF (course-provided)
│   │   ├── stock_prices.csv             Daily adjusted close, 25 stocks
│   │   ├── stock_shares.csv             Market cap and shares outstanding, 25 stocks
│   │   └── urth_prices.csv              Daily adjusted close, iShares MSCI World ETF
│   └── clean/                         Built by data_prep.py. All analysis reads from here.
│       ├── stock_returns.csv            119 months × 25 stocks, monthly total returns
│       ├── factors.csv                  mkt_rf, smb, hml, rf, msci_world
│       ├── market_caps.csv              Market caps and value weights
│       └── data_notes.md                Every cleaning decision, checks, limitations
│
├── src/
│   ├── config.py                      Shared settings: tickers, sample period, paths, chart style
│   ├── data_prep.py                   Download (once) and clean the data
│   ├── stage1_portfolio.py            Stage 1 · Portfolio choice
│   ├── stage2_capm.py                 Stage 2 · CAPM
│   ├── stage3_factors.py              Stage 3 · Factors
│   └── stage4_roll.py                 Stage 4 · Roll's critique
│
├── output/                            Built by the stage scripts
│   ├── figures/                       Charts, plus tables rendered as images for the report
│   └── tables/                        Tables as .csv / .html
│
├── report/
│   ├── FE5108_final_report.pdf        ★ Submitted report
│   ├── final_report.md                Source of the PDF
│   ├── 0_exec_summary.md              Section drafts, merged into final_report.md
│   ├── 1_stage1.md · 1_stage1_appendix.md
│   ├── 2_stage2.md
│   ├── 3_stage3.md
│   ├── 4_memo.md
│   ├── appendix.md                    Contribution statement
│   └── Signature1–5                   Member signatures
│
└── Read it first before you do!/      Project brief and internal task plan
    ├── midterm_project_handout.pdf
    └── FE5108_Midterm_Who_Does_What.pdf
```

---

## Where each report exhibit comes from

| Exhibit | File(s) | Script |
|---|---|---|
| 1a Summary statistics | `output/tables/tab_1a_summary_statistics.html` | `stage1_portfolio.py` |
| 1b Tangency vs value weights | `output/figures/fig_1b_weights.png`, `output/tables/tab_1b_portfolio_weights.html` | `stage1_portfolio.py` |
| 1c Subsample and no-short checks | `output/tables/tab_1c_portfolio_diagnostics.html`, `tab_1_main_diagnostics.html` | `stage1_portfolio.py` |
| 2a CAPM regressions | `output/figures/tab_2a_capm.png`, `output/tables/tab_2a_capm.csv` | `stage2_capm.py` |
| 2b Empirical SML | `output/figures/fig_2b_sml.png` | `stage2_capm.py` |
| 2c Joint alpha tests (GRS) | `output/figures/tab_2c_alpha_tests.png`, `output/tables/tab_2c_alpha_tests.csv` | `stage2_capm.py` |
| 2d Fitted vs theoretical SML | `output/tables/tab_2d_sml.csv` | `stage2_capm.py` |
| 2e Robustness (no NVDA, half-samples) | `output/figures/tab_2e_robustness.png`, `output/tables/tab_2e_robustness.csv` | `stage2_capm.py` |
| 3a Three-factor loadings | `output/tables/tab_3a_ff3.csv` | `stage3_factors.py` |
| 3b Alphas before vs after factors | `output/figures/fig_3b_alpha_comparison.png`, `output/tables/tab_3b_alpha_comparison.csv` | `stage3_factors.py` |
| 4 Market-proxy comparison | `output/figures/fig_4_sml_proxy_robustness.png`, `output/tables/stage4_proxy_comparison.csv`, `stage4_sml_robustness.csv` | `stage4_roll.py` |

---

## Data

| Item | Choice | Source |
|---|---|---|
| Universe | 25 S&P 500 stocks, 2–3 per sector, all 11 GICS sectors (list in `src/config.py`) | Yahoo Finance via `yfinance`, downloaded 8 Oct 2026 |
| Sample | Sep 2016 – Jul 2026, 119 monthly returns | Matched to the course-provided factor file |
| Returns | Simple monthly total returns from dividend- and split-adjusted prices | Yahoo Finance |
| Riskless rate | 1-month U.S. T-bill (`RF`) | Ken French Data Library |
| Market proxy | U.S. value-weighted market excess return (`Mkt-RF`) | Ken French Data Library |
| Second market proxy | MSCI World, via the iShares MSCI World ETF (URTH) | Yahoo Finance |
| Factors | Size (`SMB`), value (`HML`) | Ken French Data Library |

**Conventions.** All returns are monthly decimals (0.012 = 1.2%). `mkt_rf` already has `rf`
subtracted; `msci_world` does not. Dates are `YYYY-MM`.

**Known limitations.** The universe is today's S&P 500 constituents followed back ten years, so it
has survivorship bias (average returns are overstated). Market caps are dated 8 Oct 2026, after the
sample ends. Full details in [`data/clean/data_notes.md`](data/clean/data_notes.md).

---

## Package versions

Minimum versions are in `requirements.txt`. The full pipeline was last tested end to end on
16 Oct 2026 with:

| Package | Version |
|---|---|
| Python | 3.13 |
| pandas | 3.0.5 |
| numpy | 2.5.3 |
| scipy | 1.18.1 |
| statsmodels | 0.15.0 |
| matplotlib | 3.11.2 |
| yfinance | 1.7.0 (only needed if `data/raw/` is deleted and the data are re-downloaded) |

---

## Team

| Member | Role |
|---|---|
| A · Zhou Mo | Project coordination (GitHub, task plan, meetings); data pipeline; `run_all.py`; README |
| B · Yuki Sato | Stage 1: portfolio choice |
| C · Zhang Yin | Stage 2: CAPM tests |
| D · Zhang Jiaxin | Stage 3: factor models |
| E · Wu Shuhan | Stage 4: Roll's critique, investment committee memo, final report |

The signed contribution statement and the AI-use disclosure are in the report appendix.
