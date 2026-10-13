"""Stage 4: Roll's critique and market-proxy robustness.

Owner: E (Smart)

Reuses Stage 2's run_capm and fit_sml functions, with identical data and
regression conventions. Run from the repository root with:
    python src/stage4_roll.py

Outputs:
    output/tables/stage4_proxy_comparison.csv
    output/tables/stage4_sml_robustness.csv
    output/figures/fig_4_sml_proxy_robustness.png
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from config import (
    STOCK_RETURNS, FACTORS, FIG_DIR, TAB_DIR, COLORS,
    MONTHS_PER_YEAR, apply_plot_style,
)
from stage2_capm import run_capm, fit_sml


def load_data():
    """Read only the shared cleaned files, and verify their alignment."""
    stocks = pd.read_csv(STOCK_RETURNS, index_col="date")
    factors = pd.read_csv(FACTORS, index_col="date")

    if not stocks.index.equals(factors.index):
        raise ValueError("Stock and factor dates do not match exactly.")
    if stocks.index.has_duplicates or factors.index.has_duplicates:
        raise ValueError("Duplicate monthly dates detected.")
    if len(stocks) != 119:
        raise ValueError(f"Expected 119 months; found {len(stocks)}.")
    required = {"mkt_rf", "msci_world", "rf"}
    missing = required.difference(factors.columns)
    if missing:
        raise ValueError(f"Missing factor columns: {sorted(missing)}")
    if stocks.isna().any().any() or factors[list(required)].isna().any().any():
        raise ValueError("Missing values in cleaned regression inputs.")
    return stocks, factors


def make_proxy_comparison(us_table, world_table):
    """Compare each stock's CAPM estimates under the two proxies."""
    if not us_table.index.equals(world_table.index):
        raise ValueError("Stock ordering differs between the two CAPM results.")

    out = pd.DataFrame(index=us_table.index)
    out.index.name = "ticker"
    for name, column in (
        ("alpha", "alpha"), ("beta", "beta"),
        ("alpha_t", "t_alpha"), ("r2", "r2"),
    ):
        out[f"{name}_us"] = us_table[column]
        out[f"{name}_world"] = world_table[column]
    out["delta_alpha"] = out["alpha_world"] - out["alpha_us"]
    out["delta_beta"] = out["beta_world"] - out["beta_us"]
    return out[[
        "alpha_us", "alpha_world", "delta_alpha",
        "beta_us", "beta_world", "delta_beta",
        "alpha_t_us", "alpha_t_world", "r2_us", "r2_world",
    ]]


def make_sml_robustness(us_table, world_table, us_market, world_market):
    """Fit cross-sectional SML with/without NVDA under each proxy."""
    rows = []
    for proxy, table, market in (
        ("US Market", us_table, us_market),
        ("MSCI World (URTH)", world_table, world_market),
    ):
        for exclude_nvda in (False, True):
            subset = table.drop(index="NVDA") if exclude_nvda else table
            sml = fit_sml(subset, market)
            rows.append({
                "proxy": proxy,
                "exclude_nvda": exclude_nvda,
                "n_stocks": len(subset),
                "fitted_slope_ann": sml["fitted_slope_ann"],
                "theory_slope_ann": sml["theory_slope_ann"],
                "slope_gap_ann": sml["fitted_slope_ann"] - sml["theory_slope_ann"],
                "fitted_intercept_ann": sml["fitted_intercept_ann"],
                "t_slope_vs_theory": sml["t_slope_vs_theory"],
                "t_intercept_vs_zero": sml["t_intercept_vs_zero"],
                "cs_r2": sml["cs_r2"],
            })
    return pd.DataFrame(rows)


def plot_sml_comparison(us_table, world_table, robustness, path):
    """Plot four fitted SMLs and their respective CAPM theoretical lines."""
    apply_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, (proxy, table, main_color) in zip(axes, (
        ("US Market", us_table, COLORS["main"]),
        ("MSCI World (URTH)", world_table, COLORS["second"]),
    )):
        x = table["beta"].to_numpy()
        y = table["mean_excess_ann"].to_numpy()
        nvda = table.index == "NVDA"
        ax.scatter(x[~nvda], y[~nvda], color=main_color, s=24, alpha=0.8)
        ax.scatter(x[nvda], y[nvda], color=main_color, marker="*", s=125,
                   edgecolors="black", linewidths=0.5, zorder=5, label="NVDA")
        if nvda.any():
            ax.annotate("NVDA", (x[nvda][0], y[nvda][0]),
                        xytext=(4, 4), textcoords="offset points", fontsize=8)
        xs = np.linspace(min(0, x.min()) - 0.05, x.max() + 0.1, 100)
        rows = robustness.loc[robustness["proxy"] == proxy]
        full = rows.loc[~rows["exclude_nvda"]].iloc[0]
        drop = rows.loc[rows["exclude_nvda"]].iloc[0]
        ax.plot(xs, full["fitted_intercept_ann"] + full["fitted_slope_ann"] * xs,
                color=main_color, linewidth=2, label="Fitted: all 25")
        ax.plot(xs, drop["fitted_intercept_ann"] + drop["fitted_slope_ann"] * xs,
                color=main_color, linestyle=":", linewidth=2,
                label="Fitted: excluding NVDA")
        ax.plot(xs, full["theory_slope_ann"] * xs, color=COLORS["neutral"],
                linestyle="--", label="CAPM theoretical")
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_title(proxy)
        ax.set_xlabel("Estimated beta")
        ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
        ax.legend(fontsize=7)
    axes[0].set_ylabel("Average excess return (annualized)")
    fig.suptitle("SML slope comparison: market proxy and NVDA affect the fitted line",
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main():
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    stocks, factors = load_data()
    rf = factors["rf"]
    us_market = factors["mkt_rf"]  # Already excess return.
    world_market = factors["msci_world"] - rf  # Raw URTH return -> excess.

    us_table, _ = run_capm(stocks, us_market, rf)
    world_table, _ = run_capm(stocks, world_market, rf)

    comparison = make_proxy_comparison(us_table, world_table)
    comparison_path = TAB_DIR / "stage4_proxy_comparison.csv"
    comparison.round(6).to_csv(comparison_path)

    robustness = make_sml_robustness(
        us_table, world_table, us_market, world_market
    )
    robustness_path = TAB_DIR / "stage4_sml_robustness.csv"
    robustness.round(6).to_csv(robustness_path, index=False)

    figure_path = FIG_DIR / "fig_4_sml_proxy_robustness.png"
    plot_sml_comparison(us_table, world_table, robustness, figure_path)

    n_us = int((comparison["alpha_t_us"].abs() > 2).sum())
    n_world = int((comparison["alpha_t_world"].abs() > 2).sum())
    print(f"Observations: {len(stocks)} months; stocks: {len(stocks.columns)}")
    print(f"Mean absolute beta change: {comparison['delta_beta'].abs().mean():.6f}")
    print(f"Mean absolute monthly alpha change: {comparison['delta_alpha'].abs().mean():.6f}")
    print(f"Significant alphas (|t| > 2): US={n_us}, World={n_world}")
    print("\nSML robustness (annualized slopes and intercepts are decimals):")
    print(robustness.round(4).to_string(index=False))
    print("\nSaved outputs:")
    for path in (comparison_path, robustness_path, figure_path):
        print(f"  {path}")
    print("\nNote: SML t-statistics are descriptive cross-sectional OLS statistics; "
          "they are not a fully corrected CAPM joint test.")


if __name__ == "__main__":
    main()
