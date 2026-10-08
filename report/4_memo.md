# Investment Committee Memo

**To:** Investment Committee  
**From:** FE5108 Research Zhou Mo Team  
**Subject:** Evaluating Portfolio Theory and Asset Pricing Models Using Market Data  
**Date:** October 2026  
**Status:** Working Draft — Stage 4 Results Available; Stages 1–3 Pending

## 1. Investment Question

Modern portfolio theory suggests that investors can improve portfolio efficiency through diversification, while the Capital Asset Pricing Model (CAPM) predicts that expected returns are determined by exposure to systematic market risk.

However, the practical relevance of these theoretical predictions depends on their consistency with observed market data.

Using 25 large-cap U.S. stocks across all 11 GICS sectors and 119 monthly observations from September 2016 to July 2026, this project evaluates portfolio optimization, CAPM pricing predictions, and the explanatory power of additional risk factors.

Our central question is: **To what extent should an investment committee rely on classical portfolio theory and CAPM when making real-world portfolio allocation decisions?**

## 2. Evidence from Portfolio Construction

The first stage compares the theoretically optimal tangency portfolio with a value-weighted portfolio constructed from the same 25 stocks.

Under mean-variance theory, the tangency portfolio maximizes the estimated Sharpe ratio. In practice, however, estimation errors in expected returns and the covariance matrix may produce extreme and unstable portfolio weights.

**Empirical findings to be inserted:**

- Tangency portfolio Sharpe ratio: [TBD]
- Value-weighted portfolio Sharpe ratio: [TBD]
- Differences in portfolio allocations and subsample stability: [TBD]
- Effect of no-short-selling constraints: [TBD]

**Preliminary interpretation:** A higher estimated Sharpe ratio does not necessarily imply a more reliable investment strategy. The key consideration is whether the optimized portfolio remains sufficiently stable across different samples and reasonable portfolio constraints.

## 3. Does CAPM Explain Expected Returns?

The second stage examines the relationship between systematic market risk and stock returns through CAPM regressions and the Security Market Line (SML).

CAPM predicts that securities with higher market beta should earn higher expected excess returns. However, deviations from the theoretical SML may indicate pricing errors, estimation uncertainty, or limitations of the market proxy.

**Empirical findings to be inserted:**

- Estimated CAPM coefficients and model fit: [TBD]
- Empirical versus theoretical SML: [TBD]
- Evidence of statistically significant pricing errors: [TBD]

The analysis will assess whether beta alone adequately explains average excess returns and whether observed deviations from CAPM are economically and statistically meaningful.

## 4. Do Additional Factors Improve the Model?

The third stage extends CAPM by incorporating the size (SMB) and value (HML) factors from the Fama-French three-factor framework.

These factors may capture systematic return patterns that market beta alone cannot explain.

**Empirical findings to be inserted:**

- Changes in estimated alphas after adding factors: [TBD]
- Improvement in model explanatory power: [TBD]
- Evidence of remaining abnormal returns: [TBD]

The key issue is whether additional factors meaningfully reduce pricing errors or whether important anomalies remain unexplained.

## 5. Robustness to the Market Benchmark: Roll's Critique

The fourth stage evaluates the sensitivity of CAPM results to the choice of market proxy, following Roll's critique that the true market portfolio is unobservable and cannot be perfectly represented by a stock index.

We re-estimated the CAPM regressions for all 25 stocks using two market proxies: the Ken French U.S. value-weighted market excess return and MSCI World, approximated by the iShares MSCI World ETF (URTH). Both specifications use the same 119 monthly observations and the same risk-free rate.

**Empirical findings:**

- Mean absolute change in estimated beta: **0.0732**
- Mean absolute change in monthly alpha: **0.00080 (approximately 0.080 percentage points)**
- Stocks with significant alphas (|t| > 2): **1 under the U.S. market proxy versus 3 under MSCI World**
- NVIDIA remains significant under both proxies, while Apple and Microsoft become significant under MSCI World.

These findings indicate that most CAPM estimates remain relatively stable, although the choice of market proxy affects the statistical significance of certain pricing errors.

Importantly, the two market proxies are highly correlated (approximately 0.98), partly because MSCI World has substantial U.S. equity exposure. Their similarity limits the strength of this robustness check.

**Interpretation:** Our findings illustrate Roll's critique: empirical conclusions about CAPM depend partly on the market portfolio proxy used in the regression. However, the observed changes do not constitute definitive evidence against CAPM, particularly given the similarity between the two benchmarks and the possibility of false positives across multiple significance tests.

## 6. Investment Implications and Recommendation

Our preliminary recommendation is to favor a diversified value-weighted portfolio over an unconstrained estimated tangency portfolio, while considering constrained or blended allocations if supported by the final empirical evidence.

This recommendation reflects three considerations:

1. **Portfolio Efficiency:** Although the tangency portfolio is theoretically optimal under estimated inputs, its practical reliability depends on the stability of expected-return and covariance estimates. A value-weighted portfolio provides a simpler benchmark with less dependence on optimization.

2. **Asset Pricing Reliability:** CAPM offers a useful framework for understanding systematic risk, but significant alphas and potential improvements from multifactor models must be evaluated before relying on beta as a sufficient measure of expected returns.

3. **Model Robustness:** Our Stage 4 results show that changing the market proxy alters estimated betas and the number of statistically significant alphas. Investment decisions should therefore not rely excessively on a single market benchmark or model specification.

**Intellectual Honesty — Which Result Do We Trust Least?**

At this stage, we are most cautious about the estimated tangency portfolio weights. Portfolio optimization can amplify small estimation errors into large allocation changes, especially when expected returns are estimated from a limited historical sample.

We will evaluate this concern using the subsample stability and no-short-selling analyses from Stage 1. We also acknowledge survivorship bias from selecting current S&P 500 constituents and the limited independence of our two highly correlated market proxies.

**Preliminary Conclusion:** Classical portfolio theory and CAPM remain valuable analytical benchmarks, but their investment implications should be assessed through estimation stability, robustness checks, and practical implementation considerations. Unless the final evidence demonstrates reliable benefits from optimization, a diversified value-weighted strategy appears to be the more defensible starting point.

---

*Working draft. Stage 4 results are preliminary and will be cross-checked against the final Stage 2 regression methodology. Sections 2–4 and the final investment recommendation will be updated after the remaining empirical analyses are completed.*