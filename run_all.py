"""
Reproduce every table and figure in the report with one command.

    python run_all.py

Runs the scripts below in order, from the project folder, and stops at the
first error. Raw data are already in data/raw/, so no internet is needed:
data_prep.py skips any download whose file already exists.

Owner: A
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STEPS = [
    ("src/data_prep.py",        "Data: raw -> clean (A)"),
    ("src/stage1_portfolio.py", "Stage 1: portfolio choice (B)"),
    ("src/stage2_capm.py",      "Stage 2: CAPM tests (C)"),
    ("src/stage3_factors.py",   "Stage 3: Fama-French factors (D)"),
    ("src/stage4_roll.py",      "Stage 4: Roll's critique (E)"),
]

# Files the report relies on; checked after all steps have run.
EXPECTED = [
    "data/clean/stock_returns.csv",
    "data/clean/factors.csv",
    "data/clean/market_caps.csv",
    "output/figures/fig_1b_weights.png",
    "output/tables/tab_1a_summary_statistics.html",
    "output/tables/tab_1b_portfolio_weights.html",
    "output/tables/tab_1c_portfolio_diagnostics.html",
    "output/figures/tab_2a_capm.png",
    "output/figures/fig_2b_sml.png",
    "output/figures/tab_2c_alpha_tests.png",
    "output/tables/tab_2d_sml.csv",
    "output/figures/tab_2e_robustness.png",
    "output/tables/tab_3a_ff3.csv",
    "output/figures/fig_3b_alpha_comparison.png",
    "output/tables/stage4_proxy_comparison.csv",
    "output/figures/fig_4_sml_proxy_robustness.png",
]


def main():
    start_all = time.time()
    for i, (script, label) in enumerate(STEPS, start=1):
        print(f"\n[{i}/{len(STEPS)}] {label}  ->  python {script}")
        print("-" * 70, flush=True)
        start = time.time()
        result = subprocess.run([sys.executable, script], cwd=ROOT)
        if result.returncode != 0:
            print(f"\nFAILED at step {i}: {script} (exit code {result.returncode}).")
            print("Fix this script and run run_all.py again.")
            sys.exit(result.returncode)
        print(f"-- done in {time.time() - start:.1f} s")

    missing = [f for f in EXPECTED if not (ROOT / f).exists()]
    print("\n" + "=" * 70)
    if missing:
        print("All scripts ran, but these expected outputs are missing:")
        for f in missing:
            print(f"  - {f}")
        sys.exit(1)
    print(f"All {len(STEPS)} steps finished in {time.time() - start_all:.1f} s.")
    print(f"All {len(EXPECTED)} report tables and figures are in data/clean/ and output/.")


if __name__ == "__main__":
    main()
