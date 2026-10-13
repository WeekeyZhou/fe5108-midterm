# Stage 4 — Investment Committee Memo

**To:** Investment Committee  
**From:** FE5108 Research Zhou Mo Team  
**Subject:** Portfolio Choice, CAPM Robustness, and Investment Implications  
**Date:** October 2026

## 1. Investment Recommendation: Index or Tangency Portfolio?

We recommend favoring a diversified value-weighted allocation over the unconstrained estimated tangency portfolio. A constrained portfolio may offer a reasonable compromise, but its investment performance requires further validation.

Under mean-variance theory, the tangency portfolio maximizes the estimated Sharpe ratio. However, this theoretical optimum depends on estimated expected returns and covariances, which are subject to sampling uncertainty.

Our Stage 1 results demonstrate substantial instability. The full-sample unconstrained tangency portfolio has gross exposure of 449.23%, including a +59.70% position in JPM and a −53.84% position in BAC. Gross exposure rises from 555.02% in the first subsample to 1,547.22% in the second, while the aggregate absolute weight change between subsamples reaches 1,658.77 percentage points.

Imposing a no-short-selling constraint reduces gross exposure to 100%, but lowers the fitted monthly Sharpe ratio from 0.548 to 0.441. This illustrates the trade-off between estimated in-sample efficiency and more implementable portfolio weights.

A value-weighted allocation avoids direct dependence on estimated optimal weights. Nevertheless, our value-weighted benchmark uses October 2026 market capitalizations rather than historical rebalancing weights. Consequently, our recommendation is based on estimation stability and implementation considerations, not demonstrated out-of-sample superiority.

## 2. Roll's Critique: Market-Proxy and NVIDIA Robustness

Roll's critique emphasizes that the true market portfolio is unobservable, making empirical CAPM tests dependent on imperfect market proxies.

We re-estimated CAPM regressions for 25 U.S. stocks over 119 monthly observations using two benchmarks: the Ken French U.S. market excess return and MSCI World, proxied by the iShares MSCI World ETF (URTH). Both specifications use identical stock returns, risk-free rates, and regression methodology.

The mean absolute change in estimated beta is **0.0732**, while the mean absolute change in monthly alpha is **0.00080**, approximately 0.080 percentage points. The number of stocks with |t(alpha)| > 2 increases from **one under the U.S. proxy to three under MSCI World**. NVIDIA remains significant under both specifications, while Apple and Microsoft cross the significance threshold only under MSCI World.

The empirical SML is steeper than the theoretical CAPM line under both market proxies:

| Market Proxy | Fitted Slope (Annualized) | Theoretical Slope | Fitted Slope Excluding NVDA |
|---|---:|---:|---:|
| U.S. Market | 23.60% | 13.02% | 15.94% |
| MSCI World (URTH) | 23.84% | 11.06% | 15.80% |

The corresponding slope-difference t-statistics fall from 2.91 to 1.01 under the U.S. proxy and from 3.28 to 1.52 under MSCI World when NVIDIA is excluded.

These findings show that the apparent SML slope anomaly is highly sensitive to one influential stock under both market proxies. Moreover, the two proxies have a correlation of approximately 0.98, limiting the independence of the robustness comparison.

Combined with Stage 2's finding that alphas are jointly consistent with zero and that the SML result is sample-period sensitive, our evidence provides no robust basis for rejecting CAPM. However, this does not establish that CAPM is correct, particularly given the limited power of the tests. The cross-sectional slope statistics should also be interpreted cautiously rather than as definitive asset-pricing tests.

Stage 3 further shows that adding the Fama-French size and value factors increases average R² from 0.282 to 0.379, but NVIDIA's significant alpha survives. Additional factors therefore improve the explanation of return variation without fully eliminating abnormal returns.

## 3. Intellectual Honesty: Which Result Do We Trust Least?

We place the least confidence in the estimated unconstrained tangency portfolio weights.

Portfolio optimization can amplify relatively small estimation errors in expected returns and covariance estimates into extreme allocations. Stage 1 provides direct evidence of sample sensitivity: AAPL's estimated weight changes from −10.57% in the first subsample to +79.37% in the second, while KO's weight changes from −26.51% to +204.30%.

These changes do not prove that the tangency portfolio will underperform out of sample, nor do they isolate sampling uncertainty from genuine changes in market conditions. Nevertheless, they make the estimated optimal weights difficult to regard as reliable future investment allocations.

Additional limitations include survivorship bias from selecting current S&P 500 constituents, the use of a post-sample market-capitalization snapshot, and the high correlation between our alternative market proxies.

## Final Recommendation

The investment committee should use a diversified value-weighted allocation as its starting point and avoid implementing the unconstrained estimated tangency portfolio without stronger out-of-sample evidence.

Our findings do not robustly reject CAPM, but they demonstrate that empirical asset-pricing conclusions are sensitive to market proxies, influential stocks, and modeling assumptions. The practical lesson is to prioritize diversification, implementation feasibility, and robustness over purely theoretical in-sample optimality.