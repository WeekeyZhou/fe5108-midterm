"""
Stage 2: test the CAPM.

Writes output/tables/tab_2a_capm.csv      (beta, alpha, t(alpha), R2 for 25 stocks)
       output/tables/tab_2c_alpha_tests.csv (|t|>2 count, GRS test)
       output/tables/tab_2d_sml.csv        (fitted vs theoretical SML)
       output/figures/fig_2b_sml.png       (empirical SML scatter)

Note for D (Stage 3): alphas before factors are in output/tables/tab_2a_capm.csv, column 'alpha' (monthly decimals). Compare against these.

Note for E (Stage 4): reuse run_capm(stocks, mkt_excess, rf) from src/stage2_capm.py. For MSCI World pass mkt_excess = factors['msci_world'] - factors['rf']."
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

from config import (
    STOCK_RETURNS, FACTORS, UNIVERSE, FIG_DIR, TAB_DIR,
    COLORS, MONTHS_PER_YEAR, apply_plot_style,
)


# ---------------------------------------------------------------------------
# Core functions (no file I/O, so Stage 4 can reuse)
# ---------------------------------------------------------------------------
def run_capm(stocks, mkt_excess, rf):
    """25 time-series regressions: R_i - rf = alpha + beta (R_m - rf) + e.
    """
    excess = stocks.sub(rf, axis=0)
    X = sm.add_constant(mkt_excess.rename("mkt"))
    rows, resid = [], {}
    for t in excess.columns:
        res = sm.OLS(excess[t], X).fit()
        rows.append({
            "ticker": t,
            "sector": UNIVERSE.get(t, ""),
            "alpha": res.params["const"],
            "t_alpha": res.tvalues["const"],
            "beta": res.params["mkt"],
            "t_beta": res.tvalues["mkt"],
            "r2": res.rsquared,
            "mean_excess": excess[t].mean(),
        })
        resid[t] = res.resid
    table = pd.DataFrame(rows).set_index("ticker")
    table["alpha_ann"] = table["alpha"] * MONTHS_PER_YEAR
    table["mean_excess_ann"] = table["mean_excess"] * MONTHS_PER_YEAR
    return table, pd.DataFrame(resid)


def count_significant(t_alpha, n_obs, crit=2.0):
    """How many |t|>crit vs. what luck alone would give."""
    n = len(t_alpha)
    k = int((t_alpha.abs() > crit).sum())
    p_two_sided = 2 * stats.t.sf(crit, n_obs - 2)       # P(|t|>2) under the null
    expected = n * p_two_sided
    p_value = stats.binom.sf(k - 1, n, p_two_sided)      # P(X >= k)
    return {"n_sig": k, "n_stocks": n, "p_single": p_two_sided,
            "expected_by_luck": expected, "binom_p_value": p_value}


def grs_test(alpha, resid, mkt_excess):
    """H0: all alphas = 0 (one factor)."""
    T, N = resid.shape
    K = 1
    sigma = resid.T.values @ resid.values / T            # MLE residual covariance
    mu_m = mkt_excess.mean()
    var_m = mkt_excess.var(ddof=0)
    a = alpha.values
    stat = (T - N - K) / N * (a @ np.linalg.solve(sigma, a)) / (1 + mu_m**2 / var_m)
    p = stats.f.sf(stat, N, T - N - K)
    return {"GRS_F": stat, "df1": N, "df2": T - N - K, "GRS_p_value": p}


def fit_sml(table, mkt_excess):
    """Cross-sectional line: mean excess return on beta, vs the CAPM line."""
    ols = sm.OLS(table["mean_excess"], sm.add_constant(table["beta"])).fit()
    return {
        "fitted_intercept_m": ols.params["const"],
        "fitted_intercept_se": ols.bse["const"],
        "fitted_slope_m": ols.params["beta"],
        "fitted_slope_se": ols.bse["beta"],
        "theory_intercept_m": 0.0,
        "theory_slope_m": mkt_excess.mean(),
        "fitted_intercept_ann": ols.params["const"] * MONTHS_PER_YEAR,
        "fitted_slope_ann": ols.params["beta"] * MONTHS_PER_YEAR,
        "theory_slope_ann": mkt_excess.mean() * MONTHS_PER_YEAR,
        "cs_r2": ols.rsquared,
        "t_slope_vs_theory": (ols.params["beta"] - mkt_excess.mean()) / ols.bse["beta"],
        "t_intercept_vs_zero": ols.params["const"] / ols.bse["const"],
    }


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
def plot_sml(table, sml, path, title=None):
    import matplotlib.pyplot as plt
    apply_plot_style()
    fig, ax = plt.subplots()
    x = table["beta"]
    y = table["mean_excess_ann"]
    ax.scatter(x, y, color=COLORS["main"], zorder=3)
    for t in table.index:
        ax.annotate(t, (x[t], y[t]), fontsize=7, xytext=(3, 3),
                    textcoords="offset points")

    xs = np.linspace(min(0, x.min()) - 0.05, x.max() + 0.1, 50)
    ax.plot(xs, sml["fitted_intercept_ann"] + sml["fitted_slope_ann"] * xs,
            color=COLORS["second"],
            label=f"Fitted line (intercept {sml['fitted_intercept_ann']:.1%}, "
                  f"slope {sml['fitted_slope_ann']:.1%})")
    ax.plot(xs, sml["theory_slope_ann"] * xs, color=COLORS["neutral"], ls="--",
            label=f"CAPM line (intercept 0, slope {sml['theory_slope_ann']:.1%})")
    ax.axhline(0, color="black", lw=0.5)
    ax.set_xlabel("Beta (market model)")
    ax.set_ylabel("Average excess return (annualised)")
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    if title is None:
        flatter = sml["fitted_slope_ann"] < sml["theory_slope_ann"]
        title = ("Fitted SML is " + ("flatter" if flatter else "steeper")
                 + " than the CAPM line")
    ax.set_title(title)
    ax.legend(fontsize=8, loc="upper left")
    fig.savefig(path)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Tables as pictures (for the report)
# ---------------------------------------------------------------------------
def _draw_table(cell_text, col_labels, path, col_widths=None, title=None,
                bold_rows=(), fig_w=7, row_h=0.26):
    import matplotlib.pyplot as plt
    n = len(cell_text)
    fig, ax = plt.subplots(figsize=(fig_w, row_h * (n + 2) + (0.4 if title else 0)))
    ax.axis("off")
    tb = ax.table(cellText=cell_text, colLabels=col_labels, loc="center",
                  cellLoc="center", colWidths=col_widths)
    tb.auto_set_font_size(False)
    tb.set_fontsize(8.5)
    tb.scale(1, 1.25)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor("#d9d9d9")
        if r == 0:
            cell.set_facecolor(COLORS["main"])
            cell.set_text_props(color="white", weight="bold")
        elif r in bold_rows:
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#fbe5d6")
        elif r % 2 == 0:
            cell.set_facecolor("#f2f2f2")
        if c == 0:
            cell._loc = "left"
    if title:
        ax.set_title(title, fontsize=10, pad=6)
    fig.savefig(path)
    plt.close(fig)


def table_2a_image(table, path, crit=2.0):
    """25 rows: beta, alpha (monthly %, annualised %), t(alpha), R2. |t|>2 in bold."""
    rows, bold = [], []
    for i, (t, r) in enumerate(table.iterrows(), start=1):
        rows.append([t, r["sector"], f"{r['beta']:.2f}", f"{r['alpha']*100:.2f}",
                     f"{r['alpha_ann']*100:.1f}", f"{r['t_alpha']:.2f}",
                     f"{r['r2']:.2f}"])
        if abs(r["t_alpha"]) > crit:
            bold.append(i)
    cols = ["Ticker", "Sector", "Beta", "Alpha (%/mo)", "Alpha (%/yr)",
            "t(alpha)", "R²"]
    _draw_table(rows, cols, path, col_widths=[0.09, 0.27, 0.09, 0.14, 0.14, 0.12, 0.09],
                bold_rows=bold, fig_w=7.5)


def table_2c_image(sig, grs, path):
    rows = [
        ["Number of stocks tested", f"{sig['n_stocks']}"],
        ["Stocks with |t(alpha)| > 2", f"{sig['n_sig']}"],
        ["Expected by luck alone (5% level)", f"{sig['expected_by_luck']:.2f}"],
        ["P(at least this many by luck)", f"{sig['binom_p_value']:.3f}"],
        [f"GRS F-statistic  F({grs['df1']}, {grs['df2']})", f"{grs['GRS_F']:.2f}"],
        ["GRS p-value (H0: all alphas = 0)", f"{grs['GRS_p_value']:.3f}"],
    ]
    _draw_table(rows, ["Test", "Result"], path, col_widths=[0.7, 0.3],
                bold_rows=(6,), fig_w=5.5, row_h=0.3)

# ---------------------------------------------------------------------------
# Robustness check
# ---------------------------------------------------------------------------
def robustness(stocks, mkt_excess, rf):
    half = len(stocks) // 2
    scenarios = {
        "Baseline (25 stocks, 2016-09 to 2026-07)": (stocks.columns, stocks.index),
        "Drop NVDA (24 stocks)": ([c for c in stocks.columns if c != "NVDA"], stocks.index),
        f"First half ({stocks.index[0]} to {stocks.index[half-1]})": (stocks.columns, stocks.index[:half]),
        f"Second half ({stocks.index[half]} to {stocks.index[-1]})": (stocks.columns, stocks.index[half:]),
    }
    rows = []
    for name, (cols, idx) in scenarios.items():
        st, m, r = stocks.loc[idx, list(cols)], mkt_excess.loc[idx], rf.loc[idx]
        tab, res = run_capm(st, m, r)
        sml = fit_sml(tab, m)
        sig = count_significant(tab["t_alpha"], len(st))
        grs = grs_test(tab["alpha"], res, m)
        rows.append({
            "scenario": name,
            "fitted_slope_ann": sml["fitted_slope_ann"],
            "theory_slope_ann": sml["theory_slope_ann"],
            "slope_se_ann": sml["fitted_slope_se"] * MONTHS_PER_YEAR,
            "t_slope_vs_theory": sml["t_slope_vs_theory"],
            "intercept_ann": sml["fitted_intercept_ann"],
            "n_sig_alpha": sig["n_sig"],
            "GRS_p": grs["GRS_p_value"],
        })
    return pd.DataFrame(rows).set_index("scenario")


def table_2e_image(rob, path):
    rows = []
    for name, r in rob.iterrows():
        rows.append([name, f"{r['fitted_slope_ann']*100:.1f}%", f"{r['theory_slope_ann']*100:.1f}%",
                     f"{r['t_slope_vs_theory']:.2f}", f"{r['intercept_ann']*100:.1f}%",
                     f"{int(r['n_sig_alpha'])}", f"{r['GRS_p']:.2f}"])
    cols = ["Scenario", "Fitted slope", "CAPM slope", "t vs CAPM",
            "Intercept", "# |t(a)|>2", "GRS p"]
    _draw_table(rows, cols, path, col_widths=[0.36, 0.11, 0.11, 0.1, 0.1, 0.11, 0.08], fig_w=9, row_h=0.32)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TAB_DIR.mkdir(parents=True, exist_ok=True)

    stocks = pd.read_csv(STOCK_RETURNS, index_col="date")
    factors = pd.read_csv(FACTORS, index_col="date")
    assert list(stocks.index) == list(factors.index), "Dates do not line up"

    mkt_excess = factors["mkt_rf"]           # already an excess return
    rf = factors["rf"]

    # (2a) 25 regressions
    table, resid = run_capm(stocks, mkt_excess, rf)
    cols = ["sector", "beta", "alpha", "alpha_ann", "t_alpha", "r2",
            "t_beta", "mean_excess", "mean_excess_ann"]
    table[cols].round(4).to_csv(TAB_DIR / "tab_2a_capm.csv")

    # (2c) joint assessment of alphas
    n_obs = len(stocks)
    sig = count_significant(table["t_alpha"], n_obs)
    grs = grs_test(table["alpha"], resid, mkt_excess)
    tests = pd.Series({**sig, **grs})
    tests.to_csv(TAB_DIR / "tab_2c_alpha_tests.csv", header=["value"])
    apply_plot_style()
    table_2a_image(table, FIG_DIR / "tab_2a_capm.png")
    table_2c_image(sig, grs, FIG_DIR / "tab_2c_alpha_tests.png")

    # (2b, 2d) empirical SML
    sml = fit_sml(table, mkt_excess)
    pd.Series(sml).to_csv(TAB_DIR / "tab_2d_sml.csv", header=["value"])
    plot_sml(table, sml, FIG_DIR / "fig_2b_sml.png")

    # (robustness) NVDA deleted
    rob = robustness(stocks, mkt_excess, rf)
    rob.round(4).to_csv(TAB_DIR / "tab_2e_robustness.csv")
    table_2e_image(rob, FIG_DIR / "tab_2e_robustness.png")
    print("\nRobustness:")
    print(rob.round(3).to_string())

    # Console summary for the write-up
    print(f"Observations: {n_obs} months, {len(table)} stocks")
    print(f"Beta range: {table['beta'].min():.2f} to {table['beta'].max():.2f}; "
          f"mean R2 {table['r2'].mean():.2f}")
    print(f"|t(alpha)|>2: {sig['n_sig']} of {sig['n_stocks']} "
          f"(luck alone: {sig['expected_by_luck']:.2f}; "
          f"P(>= {sig['n_sig']}) = {sig['binom_p_value']:.3f})")
    print(f"GRS F({grs['df1']},{grs['df2']}) = {grs['GRS_F']:.2f}, "
          f"p = {grs['GRS_p_value']:.3f}")
    print(f"Fitted SML: intercept {sml['fitted_intercept_ann']:.2%}/yr "
          f"(t={sml['t_intercept_vs_zero']:.2f}), "
          f"slope {sml['fitted_slope_ann']:.2%}/yr vs theory "
          f"{sml['theory_slope_ann']:.2%}/yr (t vs theory={sml['t_slope_vs_theory']:.2f}), "
          f"cross-section R2 {sml['cs_r2']:.2f}")


if __name__ == "__main__":
    main()
