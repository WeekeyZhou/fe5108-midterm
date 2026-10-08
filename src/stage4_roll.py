
"""Stage 4: Roll's critique — alternative market proxy.

Owner: E
Compare CAPM estimates using the Ken French US market
factor and MSCI World (proxied by URTH).
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

from config import (
    TICKERS,
    STOCK_RETURNS,
    FACTORS,
    TAB_DIR,
)


def run_capm(y, market_excess):
    """Estimate CAPM using OLS with an intercept."""
    X = sm.add_constant(market_excess, has_constant="add")
    model = sm.OLS(y, X).fit()

    return {
        "alpha": model.params.iloc[0],
        "beta": model.params.iloc[1],
        "alpha_t": model.tvalues.iloc[0],
        "r_squared": model.rsquared,
    }


def main():
    TAB_DIR.mkdir(parents=True, exist_ok=True)

    stocks = pd.read_csv(STOCK_RETURNS).set_index("date")
    factors = pd.read_csv(FACTORS).set_index("date")

    # Align observations by month.
    data = stocks.join(factors, how="inner")

    if len(data) != 119:
        raise ValueError(
            f"Expected 119 months, found {len(data)}"
        )

    if data.isna().any().any():
        raise ValueError("Missing values detected.")

    # Both market variables must be excess returns.
    us_market = data["mkt_rf"]
    world_market = data["msci_world"] - data["rf"]

    results = []

    for ticker in TICKERS:
        stock_excess = data[ticker] - data["rf"]

        us = run_capm(stock_excess, us_market)
        world = run_capm(stock_excess, world_market)

        results.append({
            "ticker": ticker,
            "alpha_us": us["alpha"],
            "alpha_world": world["alpha"],
            "delta_alpha": world["alpha"] - us["alpha"],
            "beta_us": us["beta"],
            "beta_world": world["beta"],
            "delta_beta": world["beta"] - us["beta"],
            "alpha_t_us": us["alpha_t"],
            "alpha_t_world": world["alpha_t"],
            "r2_us": us["r_squared"],
            "r2_world": world["r_squared"],
        })

    result = pd.DataFrame(results)

    output_path = TAB_DIR / "stage4_proxy_comparison.csv"
    result.to_csv(output_path, index=False)

    print("Stage 4 results saved to:", output_path)
    print(result.round(4).to_string(index=False))

    print("\nSummary:")
    print(
        "Mean absolute beta change:",
        result["delta_beta"].abs().mean()
    )
    print(
        "Mean absolute alpha change (monthly):",
        result["delta_alpha"].abs().mean()
    )
    print(
        "Significant alphas (US, |t| > 2):",
        (result["alpha_t_us"].abs() > 2).sum()
    )
    print(
        "Significant alphas (World, |t| > 2):",
        (result["alpha_t_world"].abs() > 2).sum()
    )


if __name__ == "__main__":
    main()
