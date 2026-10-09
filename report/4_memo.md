# Investment Committee Memo

**To:** Investment Committee  
**From:** FE5108 Research Zhou Mo Team  
**Subject:** Portfolio Choice, CAPM Robustness, and Investment Implications  
**Date:** October 2026  
**Status:** Working Draft — Stage 4 Completed; Final Recommendation Pending

## 1. Investment Recommendation: Index or Tangency Portfolio?

Our preliminary recommendation is to favor a diversified value-weighted portfolio over an unconstrained estimated tangency portfolio, while remaining open to constrained or blended allocations if supported by the final empirical evidence.

Under mean-variance theory, the tangency portfolio maximizes the estimated Sharpe ratio. However, its practical reliability depends heavily on estimates of expected returns and the covariance matrix. Small estimation errors can generate extreme portfolio weights and unstable allocations, potentially undermining the benefits of theoretical optimization.

A value-weighted portfolio provides a simpler and more transparent alternative that does not depend on estimated optimal weights. Nevertheless, it is not necessarily mean-variance efficient within our selected universe of 25 U.S. stocks.

**Evidence pending from Stage 1:** We will evaluate the differences between tangency and value weights, the stability of optimized allocations across subsamples, and the effects of imposing no-short-selling constraints. Our final recommendation will depend on whether the estimated efficiency gains remain sufficiently robust to justify the additional estimation and implementation risks.

## 2. Roll's Critique: Sensitivity to the Market Proxy

Roll's critique highlights a fundamental limitation of empirical CAPM testing: the theoretical market portfolio includes all risky assets but cannot be directly observed. Consequently, CAPM tests rely on imperfect market proxies, and estimated pricing relationships may depend on the benchmark selected.

We re-estimated CAPM regressions for 25 large-cap U.S. stocks using 119 monthly observations from September 2016 to July 2026. The original benchmark is the Ken French U.S. value-weighted market excess return, while the alternative is MSCI World, proxied by the iShares MSCI World ETF (URTH). Both specifications use identical stock returns, risk-free rates, and regression methodology.

**Key empirical findings:**

- The mean absolute change in estimated beta is **0.0732**.
- The mean absolute change in monthly alpha is **0.00080**, equivalent to approximately **0.080 percentage points per month**.
- The number of stocks with |t(alpha)| > 2 increases from **1 under the U.S. market proxy to 3 under MSCI World**.
- NVIDIA exhibits a significant positive alpha under both specifications. Apple and Microsoft cross the |t| > 2 threshold only under MSCI World.

Overall, the estimated betas and alphas remain relatively stable, but the statistical significance of certain pricing errors changes with the market proxy. This demonstrates that conclusions about individual CAPM pricing errors can be sensitive to benchmark selection.

However, the two market proxies are highly correlated (approximately 0.98), partly because MSCI World has substantial exposure to U.S. equities. Furthermore, the URTH ETF is itself an imperfect representation of MSCI World due to fees and tracking differences. Therefore, the limited changes observed here should not be interpreted as proof that the true market portfolio would produce similar results.

These findings support the practical relevance of Roll's critique without constituting a definitive rejection of CAPM. The increase from one to three significant alphas also warrants caution because multiple individual hypothesis tests can produce significant results by chance.

## 3. Intellectual Honesty: Which Result Do We Trust Least?

At this stage, we are most cautious about the estimated tangency portfolio weights.

The tangency portfolio is highly sensitive to estimated expected returns and the inverse covariance matrix. With only 119 monthly observations for 25 stocks, sampling uncertainty may be amplified through portfolio optimization, potentially producing extreme or unstable allocations.

**Evidence pending from Stage 1:** We will examine whether tangency weights change substantially across subsamples and whether no-short-selling constraints produce more stable allocations. If the results demonstrate significant instability, our concerns about the reliability of optimized weights will be strengthened.

Other limitations also deserve attention. Our investment universe consists of current S&P 500 constituents, introducing survivorship bias that may overstate historical performance. In addition, the high correlation between our two market proxies limits the independence of the Stage 4 robustness check.

## Preliminary Conclusion

Our current recommendation is to use a diversified value-weighted portfolio as the starting point for investment allocation rather than relying directly on unconstrained estimated tangency weights.

The Stage 4 evidence suggests that CAPM estimates are broadly stable across two closely related market proxies, although the statistical significance of individual alphas is somewhat sensitive to benchmark selection.

Ultimately, the investment committee should prioritize diversification, estimation stability, and robustness over purely theoretical optimality. The final recommendation will be revised after incorporating the completed portfolio-choice and multifactor results.

---

*Working draft. Stage 4 results have been calculated using the shared Stage 2 CAPM regression function. The final recommendation remains subject to the empirical findings from Stages 1 and 3.*