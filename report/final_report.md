# FE5108 Midterm Group Project

**From the Mutual-Fund Theorem to the Security Market Line: Does the Theory Survive Real Data?**

**October 2026 · Investment Committee Report**

---

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

---

# Stage 1 — Portfolio Choice: Tangency Weights and Robustness

## Setup and full-sample allocation

We examine 25 stocks using 119 monthly observations from September 2016 to July 2026. Appendix Table A1 summarizes their raw total returns. Expected excess returns, $\mu_e$, are estimated by subtracting the same-month monthly risk-free rate from each stock return and taking sample means. The covariance matrix, $\Sigma$, uses raw risky-asset returns and the sample denominator $n-1$. Both inputs retain monthly decimal units. Appendix Table A1 annualizes arithmetic means by multiplying by 12 and sample standard deviations by multiplying by $\sqrt{12}$. The unconstrained tangency portfolio, $w_F=\Sigma^{-1}\mu_e/(\mathbf{1}'\Sigma^{-1}\mu_e)$, maximizes estimated excess return per unit of portfolio volatility. Its weights sum to one, but short positions and leveraged long positions are allowed. It is an in-sample optimum conditional on estimated inputs, not a forecast of realized performance. These inputs are estimates from a finite historical sample, not known population parameters; sampling uncertainty means they may differ from the underlying expected returns and covariances.

The full-sample allocation contains substantial offsetting positions: JPM receives +59.70%, while BAC is shorted at −53.84%. Figure 1 shows that these are part of a broader pattern of positive and negative allocations. Table 1 reports gross exposure, the sum of absolute weights, alongside the robustness results. Although net exposure is 100%, gross exposure is much larger because the budget constraint does not limit offsetting positions. These allocations are permitted by the unconstrained formulation and are not, by themselves, evidence of a computational error.

The value-weighted comparison illustrates different construction rules rather than determining which strategy is “better.” Value weights reflect company market capitalizations within the 25-stock universe; tangency weights depend on estimated expected excess returns and covariance through Sharpe optimization. A second, related distinction is that estimation error in these inputs can affect tangency allocations, particularly without constraints; capitalization weighting does not optimize these estimated moments. The benchmark uses the October 8, 2026 market-cap snapshot, after the July 2026 return-sample end. It is therefore a snapshot benchmark, not a historically rebalanced value-weighted portfolio. Figure 1 compares allocations, not realized investment performance. Appendix Table A2 provides all five allocation estimates, allowing the selected examples to be checked against the complete results.

![Tangency and value-weighted portfolio weights](output/figures/fig_1b_weights.png)

**Figure 1. Full-sample tangency and value-weighted snapshot allocations.** Tangency weights use September 2016–July 2026 returns; value weights use October 8, 2026 market capitalizations within the 25-stock universe. **Takeaway: sample Sharpe optimization produces substantial long/short positions that differ markedly from the capitalization-based allocation.** The value-weighted portfolio is a snapshot benchmark, not a historically rebalanced portfolio; the comparison does not establish either allocation’s superiority.

## Subsample stability

We assess sample sensitivity by independently re-estimating excess means and raw-return covariance for H1 (September 2016–July 2021, 59 observations) and H2 (August 2021–July 2026, 60 observations). The optimization method remains unchanged. AAPL switches from −10.57% to +79.37%, while KO switches from −26.51% to +204.30%. These examples demonstrate changes in both the direction and magnitude of positions. Table 1, Panel A, shows the accompanying increase in gross exposure and reports the aggregate absolute weight change, $D$. This measure summarizes allocation differences across all stocks; it is not a return. Complete subsample weights appear in Appendix Table A2.

The unconstrained optimizer treats estimated means and covariances as its inputs, without distinguishing persistent opportunities from sampling noise. It can exploit relatively small estimated differences across securities through large offsetting long and short positions when estimated covariance makes their combined risk appear limited. Small input changes can therefore be amplified into large weight changes. The two halves directly demonstrate sample sensitivity through sign reversals and much higher gross exposure under different estimation periods. This is consistent with the practical importance of estimation error, but does not identify how much reflects sampling uncertainty versus genuine changes in market conditions. The exercise is not an out-of-sample performance test.

**Table 1 — Tangency Portfolio Exposure and Robustness**

**Panel A — Exposure and sample sensitivity**

| Metric | Full-sample unconstrained | H1 unconstrained | H2 unconstrained | Full-sample no-short |
|---|---:|---:|---:|---:|
| Gross exposure (%) | 449.23 | 555.02 | 1,547.22 | 100.00 |

H1–H2 aggregate absolute weight change = **1,658.77 percentage points** ($D=16.5877$). This is the sum of absolute changes in portfolio weights across stocks, **not a return**.

**Panel B — Cost of the no-short constraint**

| Metric | Unconstrained tangency | No-short tangency |
|---|---:|---:|
| Monthly fitted Sharpe | 0.548 | 0.441 |

*Full sample: September 2016–July 2026, 119 months; H1: September 2016–July 2021, 59 months; H2: August 2021–July 2026, 60 months. Gross exposure is the sum of absolute weights; all portfolios have 100% net exposure. Sharpe ratios are monthly and unitless.*

## No-short constraint and interpretation

The no-short check retains the full-sample inputs and adds non-negative weights, still summing to one. This eliminates short-financed long exposure and substantially moderates positions. It restricts the optimizer’s ability to express estimated opportunities through extreme offsetting trades. Lower fitted Sharpe is expected because the feasible set is restricted; it does not imply that the unconstrained portfolio will perform better out of sample. The solution assigns positive weights to 13 stocks; WMT is the largest holding at 19.98%. Table 1 shows the reduction in gross exposure and fitted Sharpe. Expected monthly excess return falls from 2.93% to 2.13%, while monthly volatility falls from 5.34% to 4.82%. Thus, lower volatility accompanies lower estimated excess return, rather than establishing superiority. Unlike the capitalization-based VW benchmark, the no-short portfolio remains Sharpe-optimized. The restriction does not require equal weights or eliminate concentration. It reduces extreme exposure at a cost in fitted efficiency, but this full-sample check does not establish greater stability or better expected out-of-sample performance.

The tangency portfolio can be computed successfully, yet its sample implementation produces extreme and highly period-sensitive allocations. A no-short constraint moderates this behavior at the cost of lower fitted in-sample Sharpe. Optimization identifies the estimated optimal allocation conditional on its inputs; the reliability and economic implications of that allocation require separate scrutiny. This distinction connects the empirical findings to the practical implementation of mean–variance theory.

---

# Stage 2: Does beta explain average returns? Testing the CAPM

**Bottom line.** From September 2016 to July 2026, the claim of CAPM shows that alphas are zero is not rejected. Its claim about the *slope* of the Security Market Line (SML) rejected at first (the fitted line is much steeper than theory) given by the result. But this result relies almost entirely one stock, NVIDIA, and disappears when it is removed. We therefore treat the CAPM as "not convincingly rejected, with one fragile exception".

## 2a. Security characteristic regressions

For each of the 25 stocks we ran, there are total 119 monthly observations,

R<sub>i,t</sub> − R<sub>f,t</sub> = α<sub>i</sub> + β<sub>i</sub> (R<sub>M,t</sub> − R<sub>f,t</sub>) + ε<sub>i,t</sub>,

where the market excess return is the Ken French U.S. market factor and R<sub>f</sub> is the one-month T-bill rate of the same month.

![Table 2a](output/figures/tab_2a_capm.png)

For Figure 2a, the Betas run from 0.28 (Duke Energy) to 1.75 (NVIDIA), ordered as theory suggests. For industries like utilities, staples and health care which demands are stable sit below 0.7, while NVIDIA, Bank of America, Amazon and Caterpillar whose demands are changing cyclically sit above 1.2. But only NVIDIA has a significant alpha. Alphas are monthly and annualised.

The market explains that on average, only 28% of a single stock's variance. The R² ranges from 0.07 for Verizon to 0.55 for Bank of America. The rest is firm-specific risk, which the CAPM says earns no premium.

## 2b. The empirical SML

For each stock we plot its average excess return against its estimated beta. The CAPM line passes through the origin with a slope equal to the average market excess return with 13.0% per year. The fitted line is an ordinary least squares regression of the 25 average excess returns on the 25 betas.

![Empirical SML](output/figures/fig_2b_sml.png)

For Figure 2b, the fitted SML (orange) is steeper than the CAPM line (grey dashed). This implies that high-beta stocks earned more, and low-beta stocks earn less than their betas justify. NVIDIA pulls the fitted line up strongly to the top right.

## 2c. Are all alphas zero?

After testing 25 alphas at the 5% level, we would expect about 25 × 4.8% = 1.2 significant results by chance alone even if the CAPM were exactly true. We found one, which is NVIDIA with t = 2.93. The probability of seeing at least one by chance is 71%, so this count is not unusual.

A joint test is more reliable than counting, because it uses the correlation between residuals of stocks. The Gibbons-Ross-Shanken (GRS) test of "all 25 alphas are zero" gives F(25, 93) = 1.33 with p = 0.167, so we do not reject.

![Alpha tests](output/figures/tab_2c_alpha_tests.png)

For Figure 2c, one significant alpha out of 25 is what luck alone would produce, expected to be 1.2, and the joint GRS test does not reject zero alphas (p = 0.17).

But "not rejected" is not "confirmed". With 119 months and 25 assets the test has limited power, and small alphas would go undetected.

## 2d. Fitted SML versus theory

| | Intercept (per year) | Slope (per year) |
|---|---|---|
| CAPM prediction | 0.0% | 13.0% (average market excess return) |
| Fitted (25 stocks) | −3.1% (t = −0.97) | 23.6% (s.e. 3.6%) |
| Difference | not significant | +10.6 points, t = 2.91 |

Cross-sectional R² is 0.65.

Normally, the finding in the literature is a line that is too flat with an intercept too high. The low-beta stocks earn more than the CAPM predicts and high-beta stocks earn less. But We find the opposite. The intercept is slightly negative and statistically indistinguishable from zero, and the slope is too steep.

There are possible three reasons that may explain why our sample differs:

1. **One dominant stock.** NVIDIA has the highest beta (1.75) and the highest average excess return (58.6% per year). With only 25 points, a single point this far from the others strongly tilts the line (see the robustness check below).
2. **Survivorship bias.** The 25 stocks were chosen from today's S&P 500 and followed back ten years. Firms that fell out of the index are missing. This overstates the returns of high-beta winners such as NVIDIA and Apple, which steepens the line (see `data_notes.md`, section 6).
3. **An unusual decade.** 2016 to 2026 was a strong period for technology stocks, which are also high-beta. A different ten years could give a different slope.

But one effect works against our result. The estimation error in beta usually biases the fitted slope downwards, which towards a flatter line, so measurement error cannot explain why our line is steeper. It also means that the standard error above is only a rough guide. It does not correct the beta estimation error or for correlation across residuals of stocks.

## Robustness check:

Because the steep slope is our one apparent rejection of the CAPM, we want to know whether it survives after two reasonable changes. The first one is removing NVIDIA. The second change is splitting the sample into two halves of about five years. Within each half, betas and the CAPM slope are re-estimated from that half only.

![Robustness](output/figures/tab_2e_robustness.png)

For figure 2e, the steep slope does not survive. We can see from the figure, without NVIDIA the fitted slope falls from 23.6% to 15.9%, and closer to the CAPM's 13.0% (t = 1.0). And the two sub-periods point in opposite directions, it is flatter in the first half, and steeper in the second.

This changes how we read the evidence:

- Without NVIDIA the fitted slope (15.9%) is no longer significantly different from theory, and no stock has a significant alpha. The conclusion of previous test "the SML is too steep" is therefore driven by one observation.
- Across periods, the slope is unstable. In 2016 to 2021 the fitted line was flatter than the CAPM line (9.4% versus 17.2%) with a high intercept (13.0% per year), which is same as the textbook pattern, and five stocks had significant alphas (GRS p = 0.08, borderline). In 2021 to 2026 it was steeper (16.8% versus 8.9%). With about 60 months per half the estimates are noisy, so neither half is conclusive on its own. The sign flip itself suggest that the slope depends on the period.

## Conclusion for Stage 2

Alphas are jointly consistent with zero, and the apparent failure of the SML slope is fragile. It depends on NVIDIA and on the choice of period. We do not claim the CAPM holds. We can only say the data cannot reject it firmly.

---

# Stage 3 · Adding Size and Value Factors

## 3.1 Factor setup

Stage 2 used the CAPM, where the market excess return was the only systematic risk factor. In Stage 3, we add SMB and HML to test whether the CAPM alphas can be explained by size and value effects. The model becomes:

$$
R_{i,t}-R_{f,t}
= \alpha_i
+\beta_{M,i}(R_{M,t}-R_{f,t})
+\beta_{SMB,i}SMB_t
+\beta_{HML,i}HML_t
+\varepsilon_{i,t}.
$$

We use the same sample as in Stage 2, from September 2016 to July 2026, with 119 monthly observations. All returns are monthly decimals. The market factor, SMB, HML and the risk-free rate come from the same Ken French file, so the data are consistent across the two stages. SMB stands for Small Minus Big and is a long-short factor that captures the return difference between portfolios of small and large firms. A positive SMB loading suggests stronger exposure to small-firm returns, while a negative loading is more consistent with large-cap behaviour. HML stands for High Minus Low and is a long-short factor based on the return difference between high and low book-to-market portfolios. A positive HML loading suggests stronger value exposure, while a negative loading is more consistent with growth stocks.

The estimated factor loadings show several clear patterns. NVDA, MSFT and AMZN all have negative HML loadings, with NVDA close to -1.00, which is consistent with their growth characteristics. In contrast, JPM, BAC, XOM and CVX have strong positive HML loadings, which is more in line with value exposure.

## 3.2 Changes in alpha and model fit

Figure 3b compares annualised alphas under the CAPM and the Fama-French three-factor model. After SMB and HML are added, the mean absolute annualised alpha falls only slightly, from 6.00% to 5.64%. The change is also not uniform across stocks: some alphas become smaller, while others become slightly larger. This suggests that size and value exposure explain only a limited part of the average abnormal returns left by the CAPM.

The stronger improvement appears in model fit. Average $R^2$ rises from 0.282 under the CAPM to 0.379 under the three-factor model. This means that SMB and HML explain a larger share of the month-to-month return variation, even though they do not reduce average alpha by the same amount.

$R^2$ measures how well the model explains return variation over time, while alpha measures the average return that remains unexplained after controlling for the factors. A model can therefore fit monthly return movements better without removing the intercept. Financial and energy stocks provide a clear example. JPM's $R^2$ rises from 0.498 to 0.712, while its annualised alpha changes only from 6.12% to 6.05%. The same pattern appears for XOM and CVX. Their $R^2$ values increase from 0.175 to 0.454 and from 0.231 to 0.467, while their annualised alphas change only from 2.16% to 1.94% and from 1.44% to 1.22%.

![Figure 3b. CAPM versus Fama-French three-factor alphas](output/figures/fig_3b_alpha_comparison.png)

**Figure 3b.** Adding SMB and HML changes the CAPM alphas only modestly across most stocks, suggesting that size and value factors explain only a limited part of the abnormal returns left by the CAPM. NVDA remains the only statistically significant anomaly.

## 3.3 Which Stage 2 anomalies remain?

NVDA was the only stock with a significant CAPM alpha using the $|t|>2$ rule. Its CAPM alpha was about 2.99% per month, or 35.9% per year, with a t-statistic of 2.93. After adding SMB and HML, its alpha remains about 2.94% per month, or 35.2% per year, while the t-statistic rises slightly to 3.04. This means that the NVDA anomaly is not absorbed by the size and value factors. At the same time, the three-factor model explains more of NVDA's return variation: its $R^2$ rises from 0.357 to 0.447, and its HML loading is close to -1.00, showing strong growth exposure. SMB and HML therefore explain more of how NVDA moves from month to month, but they do not explain away its unusually high average return.

Overall, Stage 3 shows that SMB and HML improve the explanation of return movements more than they improve the explanation of abnormal average returns. The factor loadings are economically sensible and the regressions fit the data better, especially for stocks with strong value or growth exposure. However, the significance pattern remains almost unchanged, and NVDA is still the only significant anomaly after the additional factors are included.

---

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

![Stage 4 SML robustness: excluding NVIDIA narrows slope gaps under both proxies](output/figures/fig_4_sml_proxy_robustness.png)

**Figure 4.** Removing NVIDIA substantially narrows the fitted-versus-theoretical SML slope gap under both market proxies. The comparison is descriptive and does not constitute a definitive CAPM test.

---
\newpage

# Appendix — Supporting Tables

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

---

## Contribution Statement

All five members contributed to the FE5108 Midterm Group Project. Responsibilities were allocated as follows:

| Member | Contribution |
|---|---|
| **A — Zhou Mo** | Data collection and cleaning; shared configuration; preparation of reproducible datasets; integration and testing of the complete code pipeline; README documentation. |
| **B — Yuki Sato** | Stage 1: portfolio summary statistics, tangency and value-weighted allocations, subsample stability analysis, no-short-selling robustness check, and corresponding report section. |
| **C — Zhang Yin** | Stage 2: CAPM regressions, empirical and theoretical SML comparison, alpha significance and joint testing, robustness analysis, and corresponding report section. |
| **D — Zhang Jiaxin** | Stage 3: Fama-French three-factor regressions, comparison of CAPM and FF3 alphas, model evaluation, and corresponding report section. |
| **E — Wu Shuhan** | Stage 4: alternative market-proxy CAPM regressions, SML and NVIDIA robustness checks, investment committee memo, executive summary, appendix, and final report integration. |

The members confirm that the descriptions above accurately reflect their contributions to the project.

## Electronic Signatures


## Electronic Signatures

| Member | Electronic Signature | Date |
|---|---|---|
| A — Zhou Mo | ![](report/Signature1.jpg){width=2.5cm} | 16 October 2026 |
| B — Yuki Sato | ![](report/Signature2.png){width=2.5cm} | 16 October 2026 |
| C — Zhang Yin | ![](report/Signature3.jpg){width=2.5cm} | 16 October 2026 |
| D — Zhang Jiaxin | ![](report/Signature4.jpg){width=2.5cm} | 16 October 2026 |
| E — Wu Shuhan | ![](report/Signature5.png){width=2.5cm} | 16 October 2026 |


## AI Tools Disclosure

ChatGPT was used for coding assistance, editing, and research exploration. The group members remain responsible for the accuracy of all calculations, results, and interpretations.
