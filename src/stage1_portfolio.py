"""Stage 1, Steps 2 through 8: portfolio estimates and subsample stability."""

import numpy as np
import pandas as pd

from config import (
    FACTORS,
    COLORS,
    FIG_DIR,
    TAB_DIR,
    apply_plot_style,
    MARKET_CAPS,
    MONTHS_PER_YEAR,
    SAMPLE_END,
    SAMPLE_START,
    STOCK_RETURNS,
    TICKERS,
)

# Stage 1 methodology:
# Expected excess returns use stock returns minus the same month's rf.
# The covariance matrix uses raw risky-asset stock returns, not excess returns.
# Step 3A estimates mean excess returns; Step 3B estimates raw-return covariance.
# Step 2 summary statistics continue to use raw stock returns.
# Step 3C solves Sigma z = mu_e and normalizes z, without forming an inverse.
# Both optimization inputs retain monthly decimal units; shorting is allowed.


def load_stock_returns():
    """Read the shared data without silently dropping or filling observations."""
    data = pd.read_csv(STOCK_RETURNS, dtype={"date": str})
    expected_columns = {"date", *TICKERS}
    if set(data.columns) != expected_columns:
        raise ValueError("Stock-return columns do not match the configured universe.")

    expected_dates = pd.period_range(SAMPLE_START, SAMPLE_END, freq="M").astype(str)
    if data["date"].tolist() != expected_dates.tolist():
        raise ValueError(
            "Dates must match the complete configured monthly sample in order, "
            "without duplicates or extra observations."
        )

    returns = data.set_index("date").loc[:, TICKERS]
    returns = returns.apply(pd.to_numeric, errors="raise")
    if not np.isfinite(returns.to_numpy(dtype=float)).all():
        raise ValueError("Stock returns contain missing or non-finite values.")
    if len(returns) < 2:
        raise ValueError("Sample standard deviation requires at least two observations.")
    return returns


def summary_statistics(returns):
    """Calculate arithmetic means and sample volatility; retain decimal units."""
    monthly_mean = returns.mean()
    monthly_std = returns.std(ddof=1)
    return pd.DataFrame(
        {
            "Monthly mean": monthly_mean,
            "Monthly volatility": monthly_std,
            "Annualized mean": monthly_mean * MONTHS_PER_YEAR,
            "Annualized volatility": monthly_std * np.sqrt(MONTHS_PER_YEAR),
        }
    ).rename_axis("Ticker")


def load_risk_free_rate(returns):
    """Require exact date alignment before subtracting the monthly risk-free rate."""
    factors = pd.read_csv(FACTORS, dtype={"date": str})
    if not {"date", "rf"}.issubset(factors.columns):
        raise ValueError("Factors must contain date and rf columns.")
    if factors["date"].isna().any() or factors["date"].duplicated().any():
        raise ValueError("Risk-free dates must be non-missing and unique.")
    if factors["date"].tolist() != returns.index.tolist():
        raise ValueError("Risk-free dates must exactly match stock-return dates in order.")
    rf = pd.to_numeric(factors.set_index("date")["rf"], errors="raise")
    if not np.isfinite(rf.to_numpy(dtype=float)).all():
        raise ValueError("Risk-free returns contain missing or non-finite values.")
    return rf


def mean_excess_returns(returns, rf=None):
    """Return the 25-entry monthly mu_e vector in configured ticker order."""
    if rf is None:
        rf = load_risk_free_rate(returns)
    if (not rf.index.is_unique or rf.index.hasnans
            or rf.index.tolist() != returns.index.tolist()):
        raise ValueError("Risk-free dates must exactly match stock-return dates in order.")
    rf = pd.to_numeric(rf, errors="raise")
    if not np.isfinite(rf.to_numpy(dtype=float)).all():
        raise ValueError("Risk-free returns contain missing or non-finite values.")
    # Subtract by month, so every stock uses the same month's rf in decimal units.
    excess_returns = returns.sub(rf, axis="index")
    mu_e = excess_returns.mean(axis=0).reindex(TICKERS)
    return mu_e.rename("Monthly mean excess return")


def estimate_covariance(returns):
    """Estimate sample covariance in monthly decimal-return-squared units."""
    # Use raw risky-asset returns, not excess returns, with the n - 1 denominator.
    # Preserve monthly units for later optimization; do not annualize sigma.
    sigma = returns.loc[:, TICKERS].cov(ddof=1)
    sigma = sigma.loc[TICKERS, TICKERS]
    if sigma.shape != (len(TICKERS), len(TICKERS)):
        raise ValueError("Covariance matrix has an unexpected shape.")
    if sigma.index.tolist() != TICKERS or sigma.columns.tolist() != TICKERS:
        raise ValueError("Covariance labels do not match configured ticker order.")
    values = sigma.to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Covariance matrix contains missing or non-finite entries.")
    if not np.allclose(values, values.T, rtol=1e-12, atol=1e-14):
        raise ValueError("Covariance matrix is not symmetric within tolerance.")
    return sigma


def tangency_portfolio(mu_e, sigma):
    """Solve for unconstrained risky-asset weights and return numerical diagnostics."""
    count = len(TICKERS)
    if mu_e.shape != (count,) or sigma.shape != (count, count):
        raise ValueError("Tangency inputs have unexpected dimensions.")
    if (mu_e.index.tolist() != TICKERS or sigma.index.tolist() != TICKERS
            or sigma.columns.tolist() != TICKERS):
        raise ValueError("Tangency inputs must follow configured ticker order.")
    mu_values = mu_e.to_numpy(dtype=float)
    sigma_values = sigma.to_numpy(dtype=float)
    if not (np.isfinite(mu_values).all() and np.isfinite(sigma_values).all()):
        raise ValueError("Tangency inputs must be finite and non-missing.")
    if not np.allclose(sigma_values, sigma_values.T, rtol=1e-12, atol=1e-14):
        raise ValueError("Tangency covariance must be symmetric.")

    condition_number = np.linalg.cond(sigma_values)
    if not np.isfinite(condition_number):
        raise ValueError("Covariance condition number is non-finite; review inputs.")
    try:
        np.linalg.cholesky(sigma_values)
        # Equivalent to inverse(Sigma) @ mu_e, without constructing the inverse.
        z = np.linalg.solve(sigma_values, mu_values)
    except np.linalg.LinAlgError as error:
        raise ValueError(
            "Covariance must be positive definite and solvable; no adjustments applied."
        ) from error
    if not np.isfinite(z).all():
        raise ValueError("Linear-system solution contains non-finite values.")
    residual = np.linalg.norm(sigma_values @ z - mu_values, ord=np.inf)
    residual_scale = (np.linalg.norm(sigma_values, ord=np.inf)
                      * np.linalg.norm(z, ord=np.inf)
                      + np.linalg.norm(mu_values, ord=np.inf))
    if residual_scale == 0 or residual > 1e-12 * residual_scale:
        raise ValueError("Linear-system residual check failed or solution is zero.")

    # A near-zero sum indicates unstable normalization from cancelling positions.
    denominator = float(z.sum())
    if not np.isfinite(denominator) or abs(denominator) <= 1e-12 * np.abs(z).sum():
        raise ValueError("Normalization denominator is non-finite or effectively zero.")
    if denominator < 0:
        raise ValueError(
            "Negative normalization denominator: review before interpreting the "
            "result as a positive-excess-return tangency portfolio."
        )
    weights = pd.Series(z / denominator, index=TICKERS, name="Tangency weight")
    if not np.isfinite(weights.to_numpy()).all():
        raise ValueError("Normalized weights contain non-finite values.")
    if not np.isclose(weights.sum(), 1.0, rtol=0, atol=1e-10):
        raise ValueError("Normalized weights do not sum to one within tolerance.")
    diagnostics = {
        "denominator": denominator,
        "condition_number": condition_number,
        "relative_residual": residual / residual_scale,
        "gross_exposure": float(weights.abs().sum()),
        "net_exposure": float(weights.sum()),
    }
    return weights, diagnostics


def value_weighted_portfolio():
    """Calculate market-cap weights and verify the independently supplied weights."""
    data = pd.read_csv(MARKET_CAPS, dtype={"ticker": str, "download_date": str})
    required = {"ticker", "market_cap", "value_weight", "download_date"}
    if not required.issubset(data.columns):
        raise ValueError("Market-cap data lack required columns.")
    if (data["ticker"].isna().any() or data["ticker"].duplicated().any()
            or len(data) != len(TICKERS) or set(data["ticker"]) != set(TICKERS)):
        raise ValueError("Market-cap data must contain each configured ticker exactly once.")
    data = data.set_index("ticker").loc[TICKERS]
    caps = pd.to_numeric(data["market_cap"], errors="raise")
    supplied = pd.to_numeric(data["value_weight"], errors="raise")
    if not np.isfinite(caps.to_numpy(dtype=float)).all() or (caps <= 0).any():
        raise ValueError("Market caps must be positive, finite, and non-missing.")
    if not np.isfinite(supplied.to_numpy(dtype=float)).all():
        raise ValueError("Supplied value weights must be finite and non-missing.")
    date_text = data["download_date"]
    if date_text.isna().any() or not date_text.str.fullmatch(r"\d{4}-\d{2}-\d{2}").all():
        raise ValueError("Snapshot dates must be present in YYYY-MM-DD format.")
    dates = pd.to_datetime(date_text, format="%Y-%m-%d", errors="raise")
    if dates.nunique() != 1:
        raise ValueError("Market-cap snapshot dates must be identical across stocks.")

    # Derive weights from capitalization; the supplied column is only a cross-check.
    total_cap = caps.astype(float).sum()
    if not np.isfinite(total_cap) or total_cap <= 0:
        raise ValueError("Total market capitalization must be finite and positive.")
    weights = (caps / total_cap).rename("Value weight")
    if not np.isfinite(weights.to_numpy()).all():
        raise ValueError("Calculated value weights must be finite.")
    if not np.isclose(weights.sum(), 1.0, rtol=0, atol=1e-10):
        raise ValueError("Calculated value weights do not sum to one.")
    max_difference = float((weights - supplied).abs().max())
    if not np.allclose(weights, supplied, rtol=1e-10, atol=1e-12):
        raise ValueError(
            f"Calculated and supplied value weights disagree; max difference {max_difference:.3e}."
        )
    return weights, dates.iloc[0].strftime("%Y-%m-%d"), max_difference


def subsample_stability(returns, full_weights):
    """Re-estimate each chronological half independently using the same methodology."""
    rf = load_risk_free_rate(returns)
    split = len(returns) // 2
    halves = [returns.iloc[:split], returns.iloc[split:]]
    rf_halves = [rf.iloc[:split], rf.iloc[split:]]
    if (halves[0].index.intersection(halves[1].index).size
            or halves[0].index.append(halves[1].index).tolist() != returns.index.tolist()):
        raise ValueError("Subsamples must be non-overlapping and cover the full sample.")

    comparison = pd.DataFrame({"Full sample": full_weights}).loc[TICKERS]
    diagnostics_by_half = {}
    for label, sample, sample_rf in zip(
            ["First half", "Second half"], halves, rf_halves):
        try:
            # Both means and raw-return covariance use only this half's observations.
            mu_e = mean_excess_returns(sample, rf=sample_rf)
            sigma = estimate_covariance(sample)
            weights, diagnostics = tangency_portfolio(mu_e, sigma)
        except (ValueError, np.linalg.LinAlgError) as error:
            raise ValueError(
                f"{label} ({sample.index[0]} through {sample.index[-1]}, "
                f"n={len(sample)}) validation failed: {error}"
            ) from error
        comparison[label] = weights
        diagnostics_by_half[label] = {
            **diagnostics,
            "start": sample.index[0],
            "end": sample.index[-1],
            "observations": len(sample),
        }
    # Sum absolute allocation changes; this is not a return or relative percentage change.
    instability = float((comparison["First half"] - comparison["Second half"]).abs().sum())
    return comparison.rename_axis("Ticker"), diagnostics_by_half, instability


def portfolio_metrics(weights, mu_e, sigma):
    """Evaluate portfolios consistently using full-sample monthly decimal inputs."""
    w = weights.loc[TICKERS].to_numpy(dtype=float)
    mean = float(w @ mu_e.loc[TICKERS].to_numpy(dtype=float))
    variance = float(w @ sigma.loc[TICKERS, TICKERS].to_numpy(dtype=float) @ w)
    if not np.isfinite(w).all() or not np.isfinite(mean) or not np.isfinite(variance) or variance <= 0:
        raise ValueError("Portfolio metrics require finite inputs and positive variance.")
    volatility = np.sqrt(variance)
    return pd.Series({
        "Expected monthly excess return": mean,
        "Monthly volatility": volatility,
        "Monthly Sharpe ratio": mean / volatility,
        "Gross exposure": np.abs(w).sum(),
        "Net exposure": w.sum(),
    })


def no_short_tangency(mu_e, sigma):
    """Solve the equivalent convex problem; independently check its KKT conditions."""
    from scipy.optimize import minimize

    if (mu_e.index.tolist() != TICKERS or sigma.index.tolist() != TICKERS
            or sigma.columns.tolist() != TICKERS):
        raise ValueError("No-short inputs must follow configured ticker order.")
    mu = mu_e.to_numpy(dtype=float)
    cov = sigma.to_numpy(dtype=float)
    if not np.isfinite(mu).all() or not np.isfinite(cov).all():
        raise ValueError("No-short inputs must be finite.")
    if not np.allclose(cov, cov.T, rtol=1e-12, atol=1e-14):
        raise ValueError("No-short covariance must be symmetric.")
    np.linalg.cholesky(cov)
    initial = np.ones(len(TICKERS)) / len(TICKERS)
    if mu @ initial <= 0:
        raise ValueError("Equal-weight starting portfolio must have positive excess mean.")
    initial = initial / (mu @ initial)
    # Sharpe is scale invariant: fix mu'y=1, minimize variance, then normalize.
    # This adds no final-weight constraints beyond non-negativity and sum to one.
    result = minimize(
        lambda y: 0.5 * y @ cov @ y,
        initial,
        jac=lambda y: cov @ y,
        method="SLSQP",
        bounds=[(0, None)] * len(TICKERS),
        constraints=[{"type": "eq", "fun": lambda y: mu @ y - 1,
                      "jac": lambda y: mu}],
        options={"ftol": 1e-12, "maxiter": 2000},
    )
    print(f"Optimizer success={result.success}; status={result.status}; iterations={result.nit}")
    print(f"Optimizer message: {result.message}")
    if not result.success:
        raise ValueError("No-short optimizer failed; no workaround applied.")
    y = result.x
    if not np.isfinite(y).all() or y.min() < -1e-10 or abs(mu @ y - 1) > 1e-10:
        raise ValueError("No-short auxiliary feasibility check failed.")
    total = y.sum()
    if not np.isfinite(total) or total <= 0:
        raise ValueError("No-short normalization is invalid.")
    w = y / total
    if not np.isfinite(w).all() or w.min() < -1e-10 or abs(w.sum() - 1) > 1e-10:
        raise ValueError("No-short final-weight feasibility check failed.")

    # KKT: cov@y - lambda*mu >= 0, with equality for positive holdings.
    # Recover lambda independently via y'cov@y / (mu'y), not solver multipliers.
    gradient = cov @ y
    multiplier = float(y @ gradient / (mu @ y))
    reduced = gradient - multiplier * mu
    scale = max(np.linalg.norm(gradient, np.inf), np.linalg.norm(multiplier * mu, np.inf),
                np.finfo(float).tiny)
    active = w > 1e-8
    stationarity = float(np.max(np.abs(reduced[active])) / scale)
    dual_violation = float(max(0.0, -reduced.min()) / scale)
    complementarity = float(np.max(np.abs(y * reduced)) / (scale * max(1.0, np.max(np.abs(y)))))
    # Scaled KKT tolerances are fixed before running; never loosen on failure.
    print(f"Independent KKT residuals: stationarity={stationarity:.3e}, "
          f"dual violation={dual_violation:.3e}, complementarity={complementarity:.3e}; tolerance=1e-6")
    if max(stationarity, dual_violation, complementarity) > 1e-6:
        raise ValueError("Independent no-short optimality check failed; no workaround applied.")
    return pd.Series(w, index=TICKERS, name="No-short tangency weight")


def plot_portfolio_weights(weights, value_weights, snapshot_date):
    """Plot existing full-precision allocations without modifying either portfolio."""
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter

    for series in (weights, value_weights):
        if series.index.tolist() != TICKERS or not np.isfinite(series.to_numpy()).all():
            raise ValueError("Plot inputs must be finite and follow TICKERS exactly.")
    apply_plot_style()
    fig, ax = plt.subplots()
    positions = np.arange(len(TICKERS))
    width = 0.4
    tangency_bars = ax.bar(positions - width / 2, weights.to_numpy(), width,
                           color=COLORS["main"], label="Unconstrained Tangency")
    value_bars = ax.bar(positions + width / 2, value_weights.to_numpy(), width,
                       color=COLORS["second"], label="Value-weighted")
    # Verify actual artist heights against the input values before saving.
    for bars, series in ((tangency_bars, weights), (value_bars, value_weights)):
        if len(bars) != len(TICKERS) or not np.array_equal(
                np.array([bar.get_height() for bar in bars]), series.to_numpy()):
            plt.close(fig)
            raise ValueError("Bar heights do not exactly match portfolio weights.")
    ax.axhline(0, color=COLORS["neutral"], linewidth=1.1)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.set_xticks(positions, TICKERS, rotation=90, fontsize=8)
    ax.set_xlabel("Stock")
    ax.set_ylabel("Portfolio weight (%)")
    ax.set_title("Tangency vs Value-weighted Portfolio")
    ax.legend(fontsize=8, loc="upper right")
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)
    fig.text(0.5, 0.02,
             f"Returns: {SAMPLE_START} to {SAMPLE_END} | Market caps: {snapshot_date} snapshot",
             ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / "fig_1b_weights.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"Step 7: all 50 bar heights exactly match input weights. Saved {path}")


def save_report_tables(summary, weights, value_weights, stability, no_short,
                       metrics, half_diagnostics, instability, snapshot_date):
    """Export only presentation copies; retain all analytical values at full precision."""
    from html import escape

    TAB_DIR.mkdir(parents=True, exist_ok=True)

    # HTML keeps headings, units, and methodological notes together for report use.
    style = """<style>
    body{font-family:Arial,sans-serif;color:#182b3a;margin:24px;max-width:900px}
    h1{font-size:18px;color:#1f4e79} h2{font-size:14px;margin-top:18px}
    table{border-collapse:collapse;width:100%;font-size:11px;font-variant-numeric:tabular-nums}
    th,td{padding:5px 8px;text-align:right;border-bottom:1px solid #e0e5e9}
    thead th{background:#edf2f6;border-top:2px solid #1f4e79;border-bottom:1px solid #1f4e79}
    tbody th{text-align:left;font-weight:normal} thead th:first-child{text-align:left}
    p{font-size:10px;line-height:1.4} tr{break-inside:avoid}
    @media print{body{margin:0;max-width:none}thead{display:table-header-group}}
    </style>"""

    def table_html(frame, formatter):
        return frame.to_html(border=0, float_format=formatter, escape=True)

    def write_table(filename, title, body):
        path = TAB_DIR / filename
        document = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width, initial-scale=1">'
                    f'<title>{escape(title)}</title>{style}</head><body>'
                    f'<h1>{escape(title)}</h1>{body}</body></html>')
        path.write_text(document, encoding="utf-8")
        print(f"Step 8: saved {path}")

    summary_display = (summary.loc[TICKERS, ["Annualized mean", "Annualized volatility"]]
                       .rename(columns={"Annualized mean": "Annualized mean return (%)",
                                        "Annualized volatility": "Annualized volatility (%)"}) * 100)
    summary_note = (f"{SAMPLE_START}–{SAMPLE_END}; {sum(d['observations'] for d in half_diagnostics.values())} monthly observations. "
                    "Raw stock total returns (dividend-adjusted). Annualized arithmetic mean = monthly mean × 12; "
                    "annualized volatility = monthly sample standard deviation × √12 (ddof=1). "
                    "Annualized mean is not CAGR. Values are rounded only for presentation.")
    write_table("tab_1a_summary_statistics.html", "Appendix Table A1 — Stock Summary Statistics",
                table_html(summary_display, lambda x: f"{x:.2f}") + f"<p>{escape(summary_note)}</p>")

    weight_display = pd.DataFrame({
        "VW snapshot": value_weights,
        "Tangency: Full": weights,
        "Tangency: H1": stability["First half"],
        "Tangency: H2": stability["Second half"],
        "Tangency: No-short": no_short,
    }).loc[TICKERS].rename_axis("Ticker") * 100
    zero_names = ", ".join(no_short.index[no_short.abs() <= 1e-8])
    ranges = "; ".join(f"{label}: {d['start']}–{d['end']}, n={d['observations']}"
                       for label, d in half_diagnostics.items())
    notes = [
        "All weights are percentages; each portfolio sums to 100% within numerical tolerance. Display rounding may affect column totals.",
        f"VW snapshot: {snapshot_date} market capitalizations normalized across these 25 stocks. "
        f"This postdates the {SAMPLE_END} return-sample end: a snapshot benchmark, not a historically rebalanced value-weighted portfolio.",
        f"Full: {SAMPLE_START}–{SAMPLE_END}; {ranges}. H1 is the first half; H2 is the second half.",
        "No-short is full-sample Sharpe optimization with non-negative weights summing to one. "
        "VW is also long-only but is capitalization-based, not Sharpe-optimized.",
        "Tangency estimates use monthly stock returns minus same-month rf for excess means, "
        "and raw-return sample covariance (ddof=1). No-short effectively zero holdings (|weight| ≤ 1e-8): " + zero_names + ". Stored weights are unchanged.",
    ]
    write_table("tab_1b_portfolio_weights.html", "Appendix Table A2 — Portfolio Weights and Robustness",
                table_html(weight_display, lambda x: f"{x:.2f}")
                + "".join(f"<p>{escape(note)}</p>" for note in notes))

    rows = ["Expected monthly excess return", "Monthly volatility", "Monthly Sharpe ratio", "Gross exposure"]
    panel_a = metrics.loc[rows].copy().astype(object)
    for metric in rows:
        panel_a.loc[metric] = metrics.loc[metric].map(
            lambda x: f"{x:.3f}" if metric == "Monthly Sharpe ratio" else f"{100*x:.2f}")
    panel_a.index = [name if name == "Monthly Sharpe ratio" else name + " (%)" for name in rows]
    panel_a.columns = ["Unconstrained tangency", "No-short tangency"]
    panel_b = pd.DataFrame({
        "Full sample": [metrics.loc["Gross exposure", "Unconstrained"] * 100],
        "First half": [half_diagnostics["First half"]["gross_exposure"] * 100],
        "Second half": [half_diagnostics["Second half"]["gross_exposure"] * 100],
    }, index=["Gross exposure (%)"])
    instability_note = (f"H1–H2 weight instability: D = Σ|wᵢ,H1 − wᵢ,H2| = {instability:.4f}, "
                        f"equivalent to {instability*100:,.2f} aggregate percentage points. "
                        "This measures aggregate absolute changes in portfolio weights, not a return. "
                        "Zero means identical allocations.")
    write_table("tab_1c_portfolio_diagnostics.html", "Supporting Table — Portfolio Diagnostics",
                "<h2>Panel A — Full-sample effect of the no-short constraint</h2>"
                + panel_a.to_html(border=0, escape=True)
                + "<h2>Panel B — Subsample exposure</h2>"
                + table_html(panel_b, lambda x: f"{x:.2f}")
                + f"<p>{escape(instability_note)}</p>"
                + "<p>Net exposure is 100% for every portfolio within numerical tolerance. "
                "Gross exposure is the sum of absolute weights. Sharpe ratios are monthly and unitless. "
                "Panel A uses identical full-sample monthly inputs for both portfolios.</p>")


    # Compact main-report presentation, derived solely from existing results.
    main_exposure = pd.DataFrame({
        "Full-sample unconstrained": [metrics.loc["Gross exposure", "Unconstrained"] * 100],
        "H1 unconstrained": [half_diagnostics["First half"]["gross_exposure"] * 100],
        "H2 unconstrained": [half_diagnostics["Second half"]["gross_exposure"] * 100],
        "Full-sample no-short": [metrics.loc["Gross exposure", "No-short"] * 100],
    }, index=["Gross exposure (%)"])
    main_sharpe = pd.DataFrame({
        "Unconstrained tangency": [metrics.loc["Monthly Sharpe ratio", "Unconstrained"]],
        "No-short tangency": [metrics.loc["Monthly Sharpe ratio", "No-short"]],
    }, index=["Monthly fitted Sharpe"])
    main_instability_note = (
        f"H1–H2 aggregate absolute weight change = {instability * 100:,.2f} percentage points "
        f"(D={instability:.4f}). This is the sum of absolute changes in portfolio weights "
        "across stocks, not a return."
    )
    h1, h2 = half_diagnostics["First half"], half_diagnostics["Second half"]
    main_sample_note = (
        f"Full sample: {SAMPLE_START}–{SAMPLE_END}, {h1['observations'] + h2['observations']} months; "
        f"H1: {h1['start']}–{h1['end']}, {h1['observations']} months; "
        f"H2: {h2['start']}–{h2['end']}, {h2['observations']} months. "
        "Gross exposure is the sum of absolute weights; all portfolios have 100% net exposure. "
        "Sharpe ratios are monthly and unitless."
    )
    write_table("tab_1_main_diagnostics.html", "Table 1 — Tangency Portfolio Exposure and Robustness",
                "<h2>Panel A — Exposure and sample sensitivity</h2>"
                + table_html(main_exposure, lambda x: f"{x:,.2f}")
                + f"<p>{escape(main_instability_note)}</p>"
                + "<h2>Panel B — Cost of the no-short constraint</h2>"
                + table_html(main_sharpe, lambda x: f"{x:.3f}")
                + f"<p>{escape(main_sample_note)}</p>")


def main(create_figure=True):
    # Step 1: Validate shared monthly inputs so all stocks use the same sample.
    returns = load_stock_returns()

    # Step 2: Summarize raw returns using sample standard deviation (n - 1).
    # Annualization follows config.py; annualized mean is not compounded growth.
    summary = summary_statistics(returns)

    # Display percentages only here; no output files are written at this stage.
    print(f"Observations per stock: {len(returns)}; stocks: {len(returns.columns)}")
    print(f"Sample dates: {returns.index[0]} through {returns.index[-1]} (monthly)")
    print("Validation passed: complete dates, configured tickers, finite returns.")
    print("Volatility: sample standard deviation (ddof=1). All values below are percentages.")
    print(summary.to_string(float_format=lambda value: f"{value:.2%}"))

    # Step 3A: Estimate expected excess returns after validating exact rf alignment.
    # The monthly decimal vector is retained; annualization is for display only.
    mu_e = mean_excess_returns(returns)
    excess_summary = pd.DataFrame(
        {
            "Monthly mean excess return": mu_e,
            "Annualized mean excess return": mu_e * MONTHS_PER_YEAR,
        }
    ).rename_axis("Ticker")
    print("\nStep 3A: rf dates match all stock-return dates exactly; rf values are finite.")
    print(f"mu_e: {len(mu_e)} entries, each averaged over {len(returns)} monthly excess returns.")
    print(excess_summary.to_string(float_format=lambda value: f"{value:.2%}"))

    # Step 3B: Estimate raw-return sample covariance and display only a small block.
    sigma = estimate_covariance(returns)
    example_tickers = ["AAPL", "MSFT", "NVDA"]
    example = sigma.loc[example_tickers, example_tickers]
    print(f"\nStep 3B: covariance shape {sigma.shape}; ticker order validated.")
    print("Validation passed: symmetric, finite, and no missing entries.")
    print("Monthly decimal-return-squared units; diagonal = variances, off-diagonal = covariances.")
    print(example.to_string(float_format=lambda value: f"{value:.10f}"))

    # Recover volatility from variance to check consistency with Step 2.
    aapl_annualized_vol = np.sqrt(sigma.loc["AAPL", "AAPL"]) * np.sqrt(MONTHS_PER_YEAR)
    step2_vol = summary.loc["AAPL", "Annualized volatility"]
    if not np.isclose(aapl_annualized_vol, step2_vol, rtol=1e-12, atol=1e-14):
        raise ValueError("AAPL covariance-derived volatility does not match Step 2.")
    print(f"AAPL annualized volatility from covariance: {aapl_annualized_vol:.10%}")
    print(f"AAPL annualized volatility from Step 2:    {step2_vol:.10%}")
    print("AAPL volatility consistency check passed at full numerical precision.")

    # Step 3C: Solve and normalize monthly inputs; do not constrain or clip weights.
    weights, diagnostics = tangency_portfolio(mu_e, sigma)
    print("\nStep 3C: unconstrained tangency weights (shorting allowed).")
    print(weights.to_string(float_format=lambda value: f"{value:.4%}"))
    print(f"Normalization denominator (sum z): {diagnostics['denominator']:.12g}")
    print(f"Covariance condition number (2-norm): {diagnostics['condition_number']:.12g}")
    print(f"Scaled linear-system residual: {diagnostics['relative_residual']:.3e}")
    long_ticker = weights.idxmax()
    print(f"Largest long position: {long_ticker} {weights[long_ticker]:.4%}")
    shorts = weights[weights < 0]
    if shorts.empty:
        print("Largest short position: none.")
    else:
        short_ticker = shorts.idxmin()
        print(f"Largest short position: {short_ticker} {shorts[short_ticker]:.4%}")
    print(f"Gross exposure: {diagnostics['gross_exposure']:.4%}")
    print(f"Net exposure: {diagnostics['net_exposure']:.10%}")
    print("Validation passed: positive definite covariance, solve residual, finite weights, sum = 1.")

    # Step 4: Compare with weights from one market-cap snapshot, not historical rebalancing.
    # The 2026-10-08 snapshot postdates the July 2026 return-sample end.
    value_weights, snapshot_date, max_difference = value_weighted_portfolio()
    comparison = pd.DataFrame(
        {
            "Tangency weight": weights,
            "Value weight": value_weights,
            "Difference (pp)": weights - value_weights,
        }
    ).loc[TICKERS].rename_axis("Ticker")
    print("\nStep 4: tangency versus snapshot value weights.")
    print(comparison.to_string(formatters={
        "Tangency weight": lambda value: f"{value:.4%}",
        "Value weight": lambda value: f"{value:.4%}",
        "Difference (pp)": lambda value: f"{value * 100:+.4f}",
    }))
    print("Validation passed: all configured tickers occur once; market caps positive and finite.")
    print(f"Supplied value_weight comparison passed; max absolute difference: {max_difference:.3e}")
    print("Comparison tolerance: rtol=1e-10, atol=1e-12 (decimal weights).")
    print(f"Calculated value-weight sum: {value_weights.sum():.12f}")
    largest = value_weights.idxmax()
    print(f"Largest value-weighted holding: {largest} {value_weights[largest]:.4%}")
    print(f"Market-cap snapshot: {snapshot_date}; return sample ends: {SAMPLE_END}.")
    print("This is a snapshot benchmark comparison, not a historically rebalanced value-weighted portfolio.")

    # Step 5: Assess sensitivity to estimation period without changing the estimator.
    stability, half_diagnostics, instability = subsample_stability(returns, weights)
    print("\nStep 5: independently re-estimated subsample tangency portfolios.")
    print(stability.to_string(float_format=lambda value: f"{value:.4%}"))
    for label, detail in half_diagnostics.items():
        print(f"\n{label}: {detail['start']} through {detail['end']}; n={detail['observations']}")
        half_weights = stability[label]
        long_ticker = half_weights.idxmax()
        print(f"Largest long: {long_ticker} {half_weights[long_ticker]:.4%}")
        shorts = half_weights[half_weights < 0]
        if shorts.empty:
            print("Largest short: none.")
        else:
            short_ticker = shorts.idxmin()
            print(f"Largest short: {short_ticker} {shorts[short_ticker]:.4%}")
        print(f"Gross exposure: {detail['gross_exposure']:.4%}")
        print(f"Net exposure: {detail['net_exposure']:.10%}")
        print(f"Covariance condition number: {detail['condition_number']:.12g}")
        print(f"Normalization denominator: {detail['denominator']:.12g}")
        print(f"Scaled solve residual: {detail['relative_residual']:.3e}")
        print("All date alignment, covariance, solve, and weight validation checks passed.")
    print(f"Weight instability (sum absolute differences): {instability:.10f} decimal-weight units")
    print(f"Equivalent aggregate allocation change: {instability * 100:.4f} percentage points")
    print("Zero means identical weights; larger values indicate greater weight instability, not returns.")

    # Step 6: Reuse full-sample estimates; impose only no shorting and full investment.
    print("\nStep 6: no-short full-sample tangency optimization.")
    no_short = no_short_tangency(mu_e, sigma)
    metrics = pd.DataFrame({
        "Unconstrained": portfolio_metrics(weights, mu_e, sigma),
        "No-short": portfolio_metrics(no_short, mu_e, sigma),
    })
    if metrics.loc["Monthly Sharpe ratio", "No-short"] > metrics.loc["Monthly Sharpe ratio", "Unconstrained"] + 1e-10:
        raise ValueError("No-short Sharpe exceeds unconstrained maximum beyond tolerance.")
    comparison = pd.DataFrame({
        "Unconstrained tangency weight": weights,
        "No-short tangency weight": no_short,
        "No-short − Unconstrained (pp)": no_short - weights,
    }).loc[TICKERS].rename_axis("Ticker")
    print(comparison.to_string(formatters={
        "Unconstrained tangency weight": lambda x: f"{x:.4%}",
        "No-short tangency weight": lambda x: f"{x:.4%}",
        "No-short − Unconstrained (pp)": lambda x: f"{100*x:+.4f}",
    }))
    print("Monthly metrics (percentages except unitless Sharpe):")
    display_metrics = metrics.copy().astype(object)
    for metric in metrics.index:
        display_metrics.loc[metric] = metrics.loc[metric].map(
            lambda x: f"{x:.10f}" if metric == "Monthly Sharpe ratio" else f"{x:.4%}"
        )
    print(display_metrics.to_string())
    print("Effectively zero holdings (absolute weight <= 1e-8): " + ", ".join(no_short.index[no_short.abs() <= 1e-8]))
    largest = no_short.idxmax()
    print(f"Largest no-short holding: {largest} {no_short[largest]:.4%}")
    print("All feasibility, independent optimality, and Sharpe comparison checks passed.")

    # Step 7: Visualize the existing full-sample allocations; no re-estimation here.
    if create_figure:
        plot_portfolio_weights(weights, value_weights, snapshot_date)

    # Step 8: Save report tables from existing results, with presentation-only rounding.
    save_report_tables(summary, weights, value_weights, stability, no_short,
                       metrics, half_diagnostics, instability, snapshot_date)


if __name__ == "__main__":
    main()
