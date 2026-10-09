"""
Stage 3: augment the CAPM with the Fama-French size and value factors.

For each of the 25 stocks, estimate:

    R_i - R_f
        = alpha
        + beta_mkt * (Mkt - RF)
        + beta_smb * SMB
        + beta_hml * HML
        + error

Then compare the FF3 alphas with the CAPM alphas from Stage 2.

Writes:
    output/tables/tab_3a_ff3.csv
    output/tables/tab_3b_alpha_comparison.csv
    output/figures/fig_3b_alpha_comparison.png
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

from config import (
    STOCK_RETURNS,
    FACTORS,
    FIG_DIR,
    TAB_DIR,
    UNIVERSE,
    COLORS,
    MONTHS_PER_YEAR,
    apply_plot_style,
)


# ---------------------------------------------------------------------------
# 1. Fama-French three-factor regressions
# ---------------------------------------------------------------------------
def run_ff3(stocks, factors):
    """
    Run one Fama-French three-factor regression for each stock.

    Dependent variable:
        stock excess return = stock return - rf

    Independent variables:
        mkt_rf, smb, hml

    All inputs are monthly returns in decimal form.
    """
    excess_returns = stocks.sub(factors["rf"], axis=0)

    X = factors[["mkt_rf", "smb", "hml"]]
    X = sm.add_constant(X)

    rows = []

    for ticker in excess_returns.columns:
        y = excess_returns[ticker]

        result = sm.OLS(y, X).fit()

        rows.append({
            "ticker": ticker,
            "sector": UNIVERSE.get(ticker, ""),
            "alpha_ff3": result.params["const"],
            "alpha_ff3_ann": result.params["const"] * MONTHS_PER_YEAR,
            "t_alpha_ff3": result.tvalues["const"],
            "beta_mkt": result.params["mkt_rf"],
            "beta_smb": result.params["smb"],
            "beta_hml": result.params["hml"],
            "r2_ff3": result.rsquared,
        })

    return pd.DataFrame(rows).set_index("ticker")


# ---------------------------------------------------------------------------
# 2. Compare CAPM alpha with FF3 alpha
# ---------------------------------------------------------------------------
def compare_alphas(ff3_table, capm_table):
    """
    Compare Stage-2 CAPM alphas with Stage-3 FF3 alphas.

    A Stage-2 anomaly is treated as:
        |t(alpha_CAPM)| > 2

    "Absorbed" means:
        significant under CAPM but no longer significant under FF3.

    "Survives" means:
        significant under both CAPM and FF3.
    """
    comparison = pd.DataFrame(index=ff3_table.index)

    comparison["sector"] = ff3_table["sector"]

    comparison["alpha_capm"] = capm_table.loc[
        comparison.index, "alpha"
    ]

    comparison["alpha_ff3"] = ff3_table["alpha_ff3"]

    comparison["alpha_capm_ann"] = (
        comparison["alpha_capm"] * MONTHS_PER_YEAR
    )

    comparison["alpha_ff3_ann"] = (
        comparison["alpha_ff3"] * MONTHS_PER_YEAR
    )

    comparison["t_alpha_capm"] = capm_table.loc[
        comparison.index, "t_alpha"
    ]

    comparison["t_alpha_ff3"] = ff3_table["t_alpha_ff3"]

    comparison["capm_significant"] = (
        comparison["t_alpha_capm"].abs() > 2
    )

    comparison["ff3_significant"] = (
        comparison["t_alpha_ff3"].abs() > 2
    )

    comparison["absorbed_by_factors"] = (
        comparison["capm_significant"]
        & ~comparison["ff3_significant"]
    )

    comparison["survives_after_factors"] = (
        comparison["capm_significant"]
        & comparison["ff3_significant"]
    )

    comparison["abs_alpha_reduction"] = (
        comparison["alpha_capm"].abs()
        - comparison["alpha_ff3"].abs()
    )

    return comparison


# ---------------------------------------------------------------------------
# 3. Plot: alpha before vs after factors
# ---------------------------------------------------------------------------
def plot_alpha_comparison(comparison, path):
    """
    Compare annualised CAPM and FF3 alphas for all 25 stocks.
    """
    apply_plot_style()

    tickers = comparison.index
    x = np.arange(len(tickers))
    width = 0.38

    fig, ax = plt.subplots()

    ax.bar(
        x - width / 2,
        comparison["alpha_capm_ann"],
        width,
        label="CAPM",
        color=COLORS["main"],
    )

    ax.bar(
        x + width / 2,
        comparison["alpha_ff3_ann"],
        width,
        label="Fama-French 3-factor",
        color=COLORS["second"],
    )

    ax.axhline(
        0,
        color=COLORS["neutral"],
        linewidth=0.8,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(
        tickers,
        rotation=60,
        ha="right",
        fontsize=7,
    )

    ax.set_ylabel("Alpha (annualised)")
    ax.yaxis.set_major_formatter(
        plt.matplotlib.ticker.PercentFormatter(1.0, decimals=0)
    )

    ax.set_title(
    "Size and value factors reduce some alphas but do not remove NVDA's anomaly"
)

    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Main
# ---------------------------------------------------------------------------
def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TAB_DIR.mkdir(parents=True, exist_ok=True)

    # Read the shared cleaned data prepared by Person A.
    stocks = pd.read_csv(
        STOCK_RETURNS,
        index_col="date",
    )

    factors = pd.read_csv(
        FACTORS,
        index_col="date",
    )

    # Confirm the two datasets refer to exactly the same 119 months.
    assert list(stocks.index) == list(factors.index), (
        "Stock and factor dates do not line up"
    )

    # Stage 3 uses the same sample as Stage 2.
    assert len(stocks) == 119, (
        f"Expected 119 months, found {len(stocks)}"
    )

    # Run Fama-French three-factor regressions.
    ff3_table = run_ff3(
        stocks,
        factors,
    )

    ff3_table.round(4).to_csv(
        TAB_DIR / "tab_3a_ff3.csv"
    )

    # Read Stage-2 CAPM results produced by Person C.
    capm_table = pd.read_csv(
        TAB_DIR / "tab_2a_capm.csv",
        index_col="ticker",
    )

    comparison = compare_alphas(
        ff3_table,
        capm_table,
    )

    comparison.round(4).to_csv(
        TAB_DIR / "tab_3b_alpha_comparison.csv"
    )

    plot_alpha_comparison(
        comparison,
        FIG_DIR / "fig_3b_alpha_comparison.png",
    )

    # -----------------------------------------------------------------------
    # Console summary for the report
    # -----------------------------------------------------------------------
    capm_sig = int(
        comparison["capm_significant"].sum()
    )

    ff3_sig = int(
        comparison["ff3_significant"].sum()
    )

    absorbed = comparison.index[
        comparison["absorbed_by_factors"]
    ].tolist()

    survived = comparison.index[
        comparison["survives_after_factors"]
    ].tolist()

    mean_abs_capm = (
        comparison["alpha_capm"].abs().mean()
        * MONTHS_PER_YEAR
    )

    mean_abs_ff3 = (
        comparison["alpha_ff3"].abs().mean()
        * MONTHS_PER_YEAR
    )

    print(
        f"Observations: {len(stocks)} months, "
        f"{len(stocks.columns)} stocks"
    )

    print(
        f"Significant alphas (|t| > 2): "
        f"CAPM {capm_sig}, FF3 {ff3_sig}"
    )

    print(
        "Stage-2 anomalies absorbed by SMB/HML:",
        absorbed if absorbed else "None",
    )

    print(
        "Stage-2 anomalies that survive:",
        survived if survived else "None",
    )

    print(
        f"Mean absolute annualised alpha: "
        f"CAPM {mean_abs_capm:.2%}, "
        f"FF3 {mean_abs_ff3:.2%}"
    )

    print(
        "Highest FF3 alpha:",
        ff3_table["alpha_ff3_ann"].idxmax(),
        f"{ff3_table['alpha_ff3_ann'].max():.2%}/yr",
    )

    print(
        "Lowest FF3 alpha:",
        ff3_table["alpha_ff3_ann"].idxmin(),
        f"{ff3_table['alpha_ff3_ann'].min():.2%}/yr",
    )


if __name__ == "__main__":
    main()