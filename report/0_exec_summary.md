# Executive Summary

**FE5108 Midterm Group Project**  
**From the Mutual-Fund Theorem to the Security Market Line: Does the Theory Survive Real Data?**

## Overall Finding

Our analysis suggests that classical portfolio theory and the Capital Asset Pricing Model (CAPM) remain useful analytical frameworks, but their practical implications depend critically on estimation stability, market-proxy selection, and influential observations. We find no robust evidence against CAPM in our sample, while the estimated unconstrained tangency portfolio exhibits substantial instability.

Our recommendation is to favor a diversified value-weighted allocation over directly implementing the estimated unconstrained tangency portfolio, subject to the important limitation that we have not established the value-weighted portfolio's superior out-of-sample performance.

## Key Empirical Findings

**1. Portfolio optimization produces extreme and unstable allocations.**

Using 25 large-cap U.S. stocks and 119 monthly observations from September 2016 to July 2026, the unconstrained tangency portfolio produces gross exposure of 449.23%, despite net weights summing to 100%. Gross exposure rises to 1,547.22% when the portfolio is estimated using the second half of the sample. Imposing a no-short-selling constraint reduces gross exposure to 100%, but lowers the fitted monthly Sharpe ratio from 0.548 to 0.441.

These findings demonstrate substantial sample sensitivity and caution against interpreting in-sample optimization as reliable future investment performance.

**2. CAPM is not robustly rejected by our evidence.**

Stage 2 finds that the estimated alphas are jointly consistent with zero. Although the empirical Security Market Line (SML) is steeper than the theoretical CAPM line, the apparent slope anomaly depends heavily on NVIDIA and the sample period. Therefore, the evidence does not support a robust rejection of CAPM, although the tests have limited statistical power.

**3. Additional factors improve model fit but do not eliminate abnormal returns.**

Adding the Fama-French size (SMB) and value (HML) factors increases average regression R² from 0.282 to 0.379. However, NVIDIA retains a statistically significant alpha. The additional factors improve the explanation of return movements without fully explaining abnormal average returns.

**4. Market-proxy choice affects CAPM estimates, but NVIDIA drives much of the SML discrepancy.**

Replacing the Ken French U.S. market factor with MSCI World (proxied by URTH) produces a mean absolute beta change of 0.0732 and a mean absolute monthly alpha change of 0.00080. The number of stocks with |t(alpha)| > 2 increases from one to three.

Under the U.S. market proxy, the annualized fitted SML slope is 23.60%, compared with the theoretical slope of 13.02%. Under MSCI World, the corresponding slopes are 23.84% and 11.06%.

Excluding NVIDIA reduces the fitted slopes to 15.94% and 15.80%, respectively, substantially narrowing the discrepancies under both proxies. This reinforces the conclusion that the apparent SML anomaly is sensitive to one influential stock.

## Investment Recommendation

We recommend using a diversified value-weighted portfolio as the starting point for investment allocation rather than implementing the unconstrained estimated tangency portfolio.

The tangency portfolio's extreme leverage and substantial subsample instability raise concerns about estimation error and practical implementation. A no-short-selling constraint offers a more implementable alternative, although its superior out-of-sample performance has not been demonstrated.

Our conclusions are subject to survivorship bias, a post-sample market-capitalization benchmark, limited statistical power, and the high correlation between the two market proxies.

**Bottom line:** Portfolio theory provides valuable guidance, but robust and implementable allocations deserve greater confidence than highly sensitive in-sample optima. CAPM remains a useful benchmark, and our evidence does not justify its definitive rejection.