# Stage 3 · Adding Size and Value Factors

## 3.1 Factor setup

Stage 2 used the CAPM, where the market excess return was the only systematic risk factor. In Stage 3, we add two more factors, SMB and HML, to see whether the CAPM results change after controlling for size and value effects.

The three-factor model is

$$
R_{i,t}-R_{f,t}
=
\alpha_i
+\beta_{M,i}(R_{M,t}-R_{f,t})
+\beta_{SMB,i}SMB_t
+\beta_{HML,i}HML_t
+\varepsilon_{i,t}
$$

We use the same sample as in Stage 2, covering September 2016 to July 2026 with 119 monthly observations. All returns are monthly decimals. The market factor, SMB, HML and the risk-free rate all come from the same Ken French file, so the data are consistent across the two stages.

SMB stands for Small Minus Big. It measures the return difference between small-cap and large-cap stocks. A positive SMB loading means that a stock has more exposure to small firms, while a negative loading suggests stronger large-cap characteristics.

HML stands for High Minus Low. It measures the return difference between high and low book-to-market stocks, and is commonly used as a value factor. A positive HML loading suggests stronger value exposure, while a negative loading is more consistent with growth stocks.

The estimated loadings show some clear patterns. NVDA, MSFT and AAPL all have negative HML loadings, with NVDA at about -1.00. This is consistent with their stronger growth characteristics. In contrast, JPM, BAC, XOM and CVX all have positive HML loadings, which is more in line with value exposure.

## 3.2 Alpha before and after adding factors

Figure 3b compares the annualised alphas from the CAPM with those from the Fama-French three-factor model.

After SMB and HML are added, the mean absolute annualised alpha falls from 6.00% to 5.64%. The reduction is modest, and the effect is not the same for every stock. Some alphas become smaller, while others become slightly larger.

The main improvement appears in model fit. The average $R^2$ increases from 0.282 under the CAPM to 0.379 under the three-factor model. This suggests that size and value factors help explain more of the monthly return variation across the 25 stocks.

The improvement is especially noticeable for some financial and energy stocks. For JPM, $R^2$ rises from 0.498 to 0.712, while for BAC it increases from 0.552 to 0.772. XOM and CVX also show clear increases, from 0.175 to 0.454 and from 0.231 to 0.467, respectively.

This pattern is also consistent with the factor loadings. JPM, BAC, XOM and CVX all have positive HML exposure, which helps explain why adding the value factor improves their model fit more clearly than for some other stocks.

However, a higher $R^2$ does not automatically mean that the abnormal returns found in Stage 2 disappear. The extra factors explain more return variation, but the main alpha result changes very little.

![Figure 3b. CAPM versus Fama-French three-factor alphas](../output/figures/fig_3b_alpha_comparison.png)

**Figure 3b.** Adding SMB and HML changes several CAPM alphas, but NVDA remains the only significant anomaly.

## 3.3 Which Stage 2 anomalies remain?

In Stage 2, NVDA was the only stock with a significant alpha using the $|t|>2$ rule. Its CAPM alpha was about 2.99% per month, or 35.9% per year, with a t-statistic of 2.93.

After adding SMB and HML, NVDA is still the only stock with a significant alpha. Its three-factor alpha is about 2.94% per month, or 35.2% per year, and its t-statistic is 3.04.

Therefore, the main Stage 2 anomaly is not absorbed by the size and value factors. No significant CAPM alpha becomes insignificant after the additional factors are included.

This result is especially useful for understanding NVDA. Its HML loading is around -1.00, so the model clearly captures its strong growth exposure. Even after controlling for this, however, its alpha changes very little. The annualised alpha falls only from 35.9% to 35.2%.

At the same time, the three-factor model does explain more of NVDA's return variation. Its $R^2$ increases from 0.357 under the CAPM to 0.447 under the three-factor model. This shows that the added factors improve the model, but they still leave a large unexplained alpha.

Overall, Stage 3 gives a more balanced view of the CAPM results. SMB and HML improve the fit of the regressions and help explain differences across stocks, especially for firms with clear value or growth exposure. However, they do not remove the main anomaly found in Stage 2. In this sample, the three-factor model improves explanatory power, but NVDA's abnormal return remains significant.