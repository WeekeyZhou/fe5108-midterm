
"""Stage 4: Roll's Critique — Market Proxy Robustness.

Owner: E

Compare CAPM results using:
1. Ken French U.S. market excess return
2. MSCI World (URTH) excess return

Reuses Stage 2's CAPM regression function.
"""

import pandas as pd

from config import (
    STOCK_RETURNS,
    FACTORS,
    TAB_DIR,
)

from stage2_capm import run_capm


def main():
    TAB_DIR.mkdir(parents=True, exist_ok=True)

    # Read the same cleaned data as Stage 2.
    stocks = pd.read_csv(
        STOCK_RETURNS, index_col="date"
    )
    factors = pd.read_csv(
        FACTORS, index_col="date"
    )

    assert list(stocks.index) == list(factors.index), (
        "Stock and factor dates do not match."
    )

    # Stage 2: U.S. market proxy
    us_table, _ = run_capm(
        stocks,
        factors["mkt_rf"],
        factors["rf"]
    )

    # Stage 4: MSCI World proxy
    # MSCI World is a raw return, so subtract RF.
    world_table, _ = run_capm(
        stocks,
        factors["msci_world"] - factors["rf"],
        factors["rf"]
    )

    # Compare regression results.
    result = pd.DataFrame(index=us_table.index)

    result["alpha_us"] = us_table["alpha"]
    result["alpha_world"] = world_table["alpha"]
    result["delta_alpha"] = (
        result["alpha_world"] - result["alpha_us"]
    )

    result["beta_us"] = us_table["beta"]
    result["beta_world"] = world_table["beta"]
    result["delta_beta"] = (
        result["beta_world"] - result["beta_us"]
    )

    result["alpha_t_us"] = us_table["t_alpha"]
    result["alpha_t_world"] = world_table["t_alpha"]

    result["r2_us"] = us_table["r2"]
    result["r2_world"] = world_table["r2"]

    # Save the comparison table.
    output_path = (
        TAB_DIR / "stage4_proxy_comparison.csv"
    )

    result.round(6).to_csv(output_path)

    # Print summary.
    print("Stage 4 results saved to:", output_path)

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
