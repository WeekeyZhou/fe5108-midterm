# Stage 1 Appendix

## Appendix Table A1 — Stock Summary Statistics

| Ticker | Annualized mean return (%) | Annualized volatility (%) |
|---|---:|---:|
| AAPL | 29.55 | 27.26 |
| MSFT | 24.98 | 22.75 |
| NVDA | 60.91 | 46.67 |
| JPM | 22.37 | 24.30 |
| BAC | 19.92 | 28.64 |
| JNJ | 11.91 | 17.27 |
| UNH | 17.06 | 28.88 |
| PFE | 4.24 | 22.55 |
| AMZN | 24.58 | 31.22 |
| HD | 14.18 | 22.94 |
| MCD | 12.41 | 17.13 |
| PG | 9.28 | 17.01 |
| KO | 11.61 | 16.39 |
| WMT | 19.14 | 19.10 |
| XOM | 14.14 | 28.50 |
| CVX | 14.92 | 28.45 |
| CAT | 30.79 | 32.56 |
| HON | 12.48 | 22.26 |
| UNP | 16.18 | 23.40 |
| GOOGL | 25.97 | 26.89 |
| VZ | 6.07 | 18.88 |
| NEE | 15.54 | 21.56 |
| DUK | 9.93 | 16.25 |
| SHW | 17.30 | 26.18 |
| AMT | 9.49 | 22.91 |

2016-09–2026-07; 119 monthly observations. Raw stock total returns (dividend-adjusted). Annualized arithmetic mean = monthly mean × 12; annualized volatility = monthly sample standard deviation × √12 (ddof=1). Annualized mean is not CAGR. Values are rounded only for presentation.

## Appendix Table A2 — Portfolio Weights and Robustness

| Ticker | VW snapshot | Tangency: Full | Tangency: H1 | Tangency: H2 | Tangency: No-short |
|---|---:|---:|---:|---:|---:|
| AAPL | 17.34 | 20.20 | -10.57 | 79.37 | 6.28 |
| MSFT | 13.88 | 35.20 | 65.26 | 10.91 | 10.74 |
| NVDA | 20.23 | 18.54 | 12.79 | 42.75 | 19.76 |
| JPM | 3.09 | 59.70 | 58.96 | 171.32 | 3.62 |
| BAC | 1.32 | -53.84 | -35.12 | -172.00 | 0.00 |
| JNJ | 2.20 | 3.02 | -41.13 | 27.04 | 2.54 |
| UNH | 1.19 | 16.15 | 16.10 | 11.74 | 6.89 |
| PFE | 0.56 | -20.73 | 12.62 | -82.38 | 0.00 |
| AMZN | 9.89 | -14.14 | -11.93 | -51.52 | 0.00 |
| HD | 1.01 | -8.62 | -10.32 | 81.09 | 0.00 |
| MCD | 0.58 | 11.64 | 17.41 | -115.85 | 0.00 |
| PG | 1.21 | -4.26 | 32.49 | -111.17 | 0.00 |
| KO | 1.30 | 20.57 | -26.51 | 204.30 | 8.56 |
| WMT | 3.04 | 25.28 | 5.41 | 57.09 | 19.98 |
| XOM | 2.38 | 1.62 | -23.15 | 47.69 | 0.79 |
| CVX | 1.42 | 15.51 | 10.08 | 22.41 | 0.00 |
| CAT | 1.32 | 17.58 | 16.26 | 8.86 | 8.31 |
| HON | 0.23 | -37.34 | -31.25 | -47.97 | 0.00 |
| UNP | 0.58 | -14.50 | 25.47 | -58.63 | 0.00 |
| GOOGL | 15.13 | 1.90 | -7.98 | 20.44 | 0.21 |
| VZ | 0.67 | -4.40 | -19.17 | 24.29 | 0.00 |
| NEE | 0.57 | 7.50 | 20.82 | 14.31 | 3.71 |
| DUK | 0.32 | 17.55 | 6.24 | -13.47 | 8.61 |
| SHW | 0.27 | 2.67 | -10.36 | -29.11 | 0.00 |
| AMT | 0.27 | -16.79 | 27.60 | -41.50 | 0.00 |

All weights are percentages; each portfolio sums to 100% within numerical tolerance. Display rounding may affect column totals.

VW snapshot: 2026-10-08 (October 8, 2026) market capitalizations normalized across these 25 stocks. This postdates the 2026-07 return-sample end: a snapshot benchmark, not a historically rebalanced value-weighted portfolio.

Full: 2016-09–2026-07; First half: 2016-09–2021-07, n=59; Second half: 2021-08–2026-07, n=60. H1 is the first half; H2 is the second half.

No-short is full-sample Sharpe optimization with non-negative weights summing to one. VW is also long-only but is capitalization-based, not Sharpe-optimized.

Tangency estimates use monthly stock returns minus same-month rf for excess means, and raw-return sample covariance (ddof=1). No-short effectively zero holdings (|weight| ≤ 1e-8): BAC, PFE, AMZN, HD, MCD, PG, CVX, HON, UNP, VZ, SHW, AMT. Stored weights are unchanged.
